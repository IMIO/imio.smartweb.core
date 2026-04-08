import "./edit.less";
jQuery(document).ready(function ($) {
  // Hide / show editor's tools & messages when clicking on "Preview" in Plone toolbar
  $("#contentview-preview a").click(function (e) {
    $(".hide-in-preview, #section-byline, #global_statusmessage").toggle(
      "fast",
    );
    e.preventDefault();
  });

  // Uncheck checked icon
  $("#formfield-form-widgets-svg_icon input").click(function (e) {
    var $elm_clicked = $(this);
    if ($(this).attr("checked")) {
      $(this).prop("checked", false);
      $(this).removeAttr("checked");
      $(this).css("box-shadow", "none");
      $(this).css("border-color", "#DEE2ED");
    } else {
      $("#formfield-form-widgets-svg_icon input").each(function (index, elm) {
        if ($elm_clicked[0] === elm) {
          $(this).prop("checked", true);
          $(this).attr("checked", "checked");
          $(this).css("border-color", "#007a99");
          $(this).css("box-shadow", "0 0 0 0.25rem rgb(0 122 153 / 25%)");
        } else {
          $(this).prop("checked", false);
          $(this).removeAttr("checked");
          $(this).css("box-shadow", "none");
          $(this).css("border-color", "#DEE2ED");
        }
      });
    }
  });

  // Move statistics action menu entry as the first element in personaltools menu
  var $stat_link = $("li:has(a[href*='@@stats'])");
  $("#collapse-personaltools li:eq(0)").after($stat_link);
});

jQuery(window).on("load", function (e) {
  // Move authentic sources menu just before user/personaltools-menulink in Plone toolbar
  var auth_sources = $("#plone-authentic-sources-menu")
    .wrap("<ul class='plonetoolbar-authentic-sources-menu'>")
    .parent();
  $(".personaltools-wrapper").prepend(auth_sources);

  // Move smartweb help menu just before user/personaltools-menulink in Plone toolbar
  var smartweb_help = $("#plone-smartweb-help-menu")
    .wrap("<ul class='plonetoolbar-smartweb-help-menu'>")
    .parent();
  $(".personaltools-wrapper").prepend(smartweb_help);
});

// Show/hide image_scale field based on alignment value (SectionText form)
document.addEventListener("DOMContentLoaded", function () {
  const alignmentSelect = document.getElementById("form-widgets-alignment");
  if (!alignmentSelect) return;
  const imageScaleField = document.getElementById(
    "formfield-form-widgets-image_scale",
  );
  const imageScaleSelect = document.getElementById("form-widgets-image_scale");
  if (!imageScaleField || !imageScaleSelect) return;
  function toggleImageScale() {
    const show =
      alignmentSelect.value === "top" || alignmentSelect.value === "bottom";
    imageScaleField.style.display = show ? "" : "none";
    if (!show) {
      imageScaleSelect.value = "section_text";
    }
  }

  alignmentSelect.addEventListener("change", toggleImageScale);
  toggleImageScale();
});

// Show/hide "viewport" image_scale option based on section width (SectionText form)
document.addEventListener("DOMContentLoaded", function () {
  const bootstrapSelect = document.getElementById(
    "form-widgets-bootstrap_css_class",
  );
  const imageScaleSelect = document.getElementById("form-widgets-image_scale");
  if (!bootstrapSelect || !imageScaleSelect) return;

  const viewportOption = imageScaleSelect.querySelector(
    'option[value="section_text_viewport"]',
  );
  if (!viewportOption) return;

  function toggleViewportOption() {
    const isFullWidth =
      bootstrapSelect.value === "col-sm-12" ||
      bootstrapSelect.value === "--NOVALUE--";
    if (!isFullWidth) {
      if (imageScaleSelect.value === "section_text_viewport") {
        imageScaleSelect.value = "section_text";
      }
      viewportOption.disabled = true;
      viewportOption.hidden = true;
    } else {
      viewportOption.disabled = false;
      viewportOption.hidden = false;
    }
  }

  bootstrapSelect.addEventListener("change", toggleViewportOption);
  toggleViewportOption();
});
