# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView

import json


class MapView(SectionView):
    """ """

    def data_geojson(self):
        """Return the context geolocation as GeoJSON string."""
        coordinates = self.context.geolocation
        if not coordinates:
            return
        geo_json = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [coordinates.longitude, coordinates.latitude],
            },
        }
        return json.dumps(geo_json)
