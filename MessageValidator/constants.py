#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'


FIELDNAME_METADATA_NAME = 'name'
FIELDNAME_METADATA_TIMESPAN = 'time'
FIELDNAME_METADATA_BBOX = 'area'

FIELDNAME_DISCOVERY_URL = 'base_url'
FIELDNAME_DISCOVERY_BBOX = 'area'
FIELDNAME_DISCOVERY_TIMESPAN = 'time'
FIELDNAME_DISCOVERY_METADATA = 'metadata'


FIELDNAME_LISTING_DATA = 'data'
FIELDNAME_LISTING_ACKNOWLEDGE = 'acknowledge'
FIELDNAME_LISTING_ANOMALIES = 'anomalies'
FIELDNAME_LISTING_UPSERT = 'upsert'
FIELDNAME_LISTING_DELETE = 'delete'


FIELDNAME_GEOJSON_COORDINATES = 'coordinates'
FIELDNAME_GEOJSON_BBOX = 'bbox'
FIELDNAME_GEOJSON_CRS = 'crs'
FIELDNAME_GEOJSON_OBJECTTYPE = 'type'

FIELDNAME_GEOJSON_CRS_TYPE = 'type'
FIELDVALUE_GEOJSON_CRS_TYPE_LINKED = 'link'
FIELDVALUE_GEOJSON_CRS_TYPE_NAMED = 'name'

FIELDNAME_GEOJSON_CRS_PROPERTIES = 'properties'
FIELDNAME_GEOJSON_CRS_LINKED_LINK = 'href'
FIELDNAME_GEOJSON_CRS_LINKED_TYPE = 'type'
FIELDNAME_GEOJSON_CRS_NAMED_NAME = 'name'

FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRIES = 'geometries'
FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRY = 'geometry'
FIELDNAME_GEOJSON_COLLECTIONS_FEATURES = 'features'
FIELDNAME_GEOJSON_COLLECTIONS_FEATURE = 'feature'
FIELDNAME_GEOJSON_COLLECTIONS_PROPERTIES = 'properties'


TYPES_GEOJSON_ALL = [ "Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection", "Feature", "FeatureCollection" ]
TYPES_GEOJSON_GEOMETRY = ["Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"]


#The number of axes we use as coordinates for each point on the map
#should be 2 minimum, 3 maximum
# COORD_AXES_MODEL is the number of axes we expect to find in the GeoJSON data for each point (meaningful or not, a fixed 0 on the Z axys for example is acceptable), COORD_AXES_COMPARE is the number of axes we will use for validating positions (these are the actual meaningful values)
#The validation code will provide no fallback in case the data do not respect these settings

#TODO: consider moving to configuration file (though should NEVER be changed once the application is installed)?
COORD_AXES_MODEL = 2
COORD_AXES_COMPARE = 2