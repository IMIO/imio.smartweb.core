# -*- coding: utf-8 -*-

import importlib
import os
import unittest
from unittest.mock import MagicMock, call, patch

import imio.smartweb.core as init_module


class TestInitMonkeyPatch(unittest.TestCase):
    """Tests for the NamedBlobImage monkeypatch conditional logic in __init__.py"""

    def setUp(self):
        from plone.namedfile.file import NamedBlobImage

        self._NamedBlobImage = NamedBlobImage
        self._original_setdata = NamedBlobImage._setData

    def tearDown(self):
        # Restore original _setData on NamedBlobImage
        self._NamedBlobImage._setData = self._original_setdata
        # Reload module back to non-liege state so we don't pollute other tests
        with patch.dict(os.environ, {"PROJECT_ID": ""}):
            importlib.reload(init_module)

    def _reload_with_project_id(self, project_id):
        with patch.dict(os.environ, {"PROJECT_ID": project_id}):
            importlib.reload(init_module)

    # --- Activation / deactivation ---

    def test_patch_not_applied_with_empty_project_id(self):
        """Patch should NOT be applied when PROJECT_ID is absent/empty"""
        self._reload_with_project_id("")
        self.assertIs(self._NamedBlobImage._setData, self._original_setdata)

    def test_patch_not_applied_with_other_project_id(self):
        """Patch should NOT be applied when PROJECT_ID is a different value"""
        self._reload_with_project_id("other_project")
        self.assertIs(self._NamedBlobImage._setData, self._original_setdata)

    def test_patch_applied_with_liege_smartweb(self):
        """Patch SHOULD be applied when PROJECT_ID == 'liege_smartweb'"""
        self._reload_with_project_id("liege_smartweb")
        self.assertIsNot(self._NamedBlobImage._setData, self._original_setdata)

    # --- Log messages ---

    def test_log_message_not_activated(self):
        """Should log info message containing 'NOT activated' when patch is skipped"""
        with patch.dict(os.environ, {"PROJECT_ID": ""}):
            with self.assertLogs("imio.smartweb.core", level="INFO") as cm:
                importlib.reload(init_module)
        self.assertTrue(any("NOT activated" in msg for msg in cm.output))

    def test_log_message_activated_on_call(self):
        """patched_setData should log an info message when called"""
        self._reload_with_project_id("liege_smartweb")

        mock_self = MagicMock()
        mock_self.filename = "test.jpg"
        mock_self.getFirstBytes.return_value = b"x" * 100

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(
                init_module, "getImageInfo", return_value=("image/jpeg", 100, 200)
            ):
                with self.assertLogs("imio.smartweb.core", level="INFO") as cm:
                    self._NamedBlobImage._setData(mock_self, b"data")

        self.assertTrue(any("test.jpg" in msg for msg in cm.output))

    # --- patched_setData behaviour ---

    def test_patched_setdata_calls_parent(self):
        """patched_setData should call NamedBlobFile._setData with (self, data)"""
        self._reload_with_project_id("liege_smartweb")

        mock_self = MagicMock()
        mock_self.filename = "test.png"
        mock_self.getFirstBytes.return_value = b"x" * 100
        fake_data = b"fake_image_data"

        with patch.object(init_module, "NamedBlobFile") as mock_blobfile_class:
            with patch.object(
                init_module, "getImageInfo", return_value=("image/png", 100, 200)
            ):
                self._NamedBlobImage._setData(mock_self, fake_data)

        mock_blobfile_class._setData.assert_called_once_with(mock_self, fake_data)

    def test_patched_setdata_sets_width_and_height(self):
        """patched_setData should set _width and _height from getImageInfo"""
        self._reload_with_project_id("liege_smartweb")

        mock_self = MagicMock()
        mock_self.filename = "test.png"
        mock_self.getFirstBytes.return_value = b"x" * 100

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(
                init_module, "getImageInfo", return_value=("image/png", 800, 600)
            ):
                self._NamedBlobImage._setData(mock_self, b"data")

        self.assertEqual(mock_self._width, 800)
        self.assertEqual(mock_self._height, 600)

    def test_patched_setdata_sets_content_type(self):
        """patched_setData should set contentType when getImageInfo returns a non-empty type"""
        self._reload_with_project_id("liege_smartweb")

        mock_self = MagicMock()
        mock_self.filename = "test.png"
        mock_self.getFirstBytes.return_value = b"x" * 100

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(
                init_module, "getImageInfo", return_value=("image/png", 800, 600)
            ):
                self._NamedBlobImage._setData(mock_self, b"data")

        self.assertEqual(mock_self.contentType, "image/png")

    def test_patched_setdata_skips_content_type_when_empty(self):
        """patched_setData should NOT set contentType when getImageInfo returns an empty type"""
        self._reload_with_project_id("liege_smartweb")

        # Track whether contentType was assigned via a property
        class TrackedImage:
            def __init__(self):
                self.filename = "test.bin"
                self._width = None
                self._height = None
                self._content_type_set = False
                self._content_type = "original"

            def getFirstBytes(self, *args, **kwargs):
                return b"data"

            @property
            def contentType(self):
                return self._content_type

            @contentType.setter
            def contentType(self, value):
                self._content_type = value
                self._content_type_set = True

        tracked = TrackedImage()

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(init_module, "getImageInfo", return_value=("", -1, -1)):
                self._NamedBlobImage._setData(tracked, b"data")

        self.assertFalse(tracked._content_type_set)
        self.assertEqual(tracked._content_type, "original")

    # --- Re-fetch logic for images with -1 dimensions ---

    def _assert_refetch_behaviour(self, initial_mimetype, resolved_mimetype):
        """Helper: verify that -1 dimensions trigger a second getFirstBytes call."""
        self._reload_with_project_id("liege_smartweb")

        first_bytes = b"x" * 10
        extra_bytes = b"extra"

        mock_self = MagicMock()
        mock_self.filename = f"test.{initial_mimetype.split('/')[-1]}"
        mock_self.getFirstBytes.side_effect = [first_bytes, extra_bytes]

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(init_module, "getImageInfo") as mock_getimageinfo:
                mock_getimageinfo.side_effect = [
                    (initial_mimetype, -1, -1),
                    (resolved_mimetype, 800, 600),
                ]
                self._NamedBlobImage._setData(mock_self, b"data")

        self.assertEqual(mock_self.getFirstBytes.call_count, 2)
        self.assertEqual(mock_self._width, 800)
        self.assertEqual(mock_self._height, 600)
        self.assertEqual(mock_self.contentType, resolved_mimetype)

    def test_jpeg_negative_dimensions_triggers_refetch(self):
        """JPEG with -1 dimensions should trigger a second byte fetch"""
        self._assert_refetch_behaviour("image/jpeg", "image/jpeg")

    def test_tiff_negative_dimensions_triggers_refetch(self):
        """TIFF with -1 dimensions should trigger a second byte fetch"""
        self._assert_refetch_behaviour("image/tiff", "image/tiff")

    def test_svg_negative_dimensions_triggers_refetch(self):
        """SVG with -1 dimensions should trigger a second byte fetch"""
        self._assert_refetch_behaviour("image/svg+xml", "image/svg+xml")

    def test_jpeg_valid_dimensions_no_refetch(self):
        """JPEG with valid dimensions should NOT trigger a second byte fetch"""
        self._reload_with_project_id("liege_smartweb")

        mock_self = MagicMock()
        mock_self.filename = "test.jpg"
        mock_self.getFirstBytes.return_value = b"x" * 100

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(
                init_module, "getImageInfo", return_value=("image/jpeg", 640, 480)
            ):
                self._NamedBlobImage._setData(mock_self, b"data")

        self.assertEqual(mock_self.getFirstBytes.call_count, 1)
        self.assertEqual(mock_self._width, 640)
        self.assertEqual(mock_self._height, 480)

    def test_png_negative_dimensions_no_refetch(self):
        """PNG with -1 dimensions should NOT trigger a refetch (only JPEG/TIFF/SVG do)"""
        self._reload_with_project_id("liege_smartweb")

        mock_self = MagicMock()
        mock_self.filename = "test.png"
        mock_self.getFirstBytes.return_value = b"x" * 100

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(
                init_module, "getImageInfo", return_value=("image/png", -1, -1)
            ):
                self._NamedBlobImage._setData(mock_self, b"data")

        self.assertEqual(mock_self.getFirstBytes.call_count, 1)

    def test_refetch_uses_correct_getfirstbytes_args(self):
        """Second getFirstBytes call should pass (start, length) derived from MAX_INFO_BYTES"""
        self._reload_with_project_id("liege_smartweb")

        MAX_INFO_BYTES = init_module.MAX_INFO_BYTES
        first_bytes = b"x" * 10
        expected_start = len(first_bytes)
        expected_length = max(0, MAX_INFO_BYTES - expected_start)

        mock_self = MagicMock()
        mock_self.filename = "test.jpg"
        mock_self.getFirstBytes.side_effect = [first_bytes, b"more"]

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(init_module, "getImageInfo") as mock_getimageinfo:
                mock_getimageinfo.side_effect = [
                    ("image/jpeg", -1, -1),
                    ("image/jpeg", 100, 200),
                ]
                self._NamedBlobImage._setData(mock_self, b"data")

        second_call = mock_self.getFirstBytes.call_args_list[1]
        self.assertEqual(second_call, call(expected_start, expected_length))

    def test_refetch_passes_combined_bytes_to_getimageinfo(self):
        """Second getImageInfo call should receive concatenated firstbytes"""
        self._reload_with_project_id("liege_smartweb")

        first_bytes = b"FIRST"
        extra_bytes = b"EXTRA"

        mock_self = MagicMock()
        mock_self.filename = "test.jpg"
        mock_self.getFirstBytes.side_effect = [first_bytes, extra_bytes]

        with patch.object(init_module, "NamedBlobFile"):
            with patch.object(init_module, "getImageInfo") as mock_getimageinfo:
                mock_getimageinfo.side_effect = [
                    ("image/jpeg", -1, -1),
                    ("image/jpeg", 100, 200),
                ]
                self._NamedBlobImage._setData(mock_self, b"data")

        # First call: original data; second call: combined firstbytes
        second_call_arg = mock_getimageinfo.call_args_list[1][0][0]
        self.assertEqual(second_call_arg, first_bytes + extra_bytes)
