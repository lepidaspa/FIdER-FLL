#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'


ERROR_NO_DICT = "%s is not a valid dictionary"
ERROR_FIELDS_MISMATCH = "Different number of fields at %s"
ERROR_VALUE_NOT_IN_RANGE = "%s value not in range ('%s', allowed: %s)"
ERROR_VALUE_WRONG_TYPE = "%s value has the wrong type ('%s', required: %s)"
ERROR_INVALID_DATETIME = "Invalid datetime field: %s"

ERROR_JSON_PARSING = "Not a valid JSON object? %s "

ERROR_GEOJSON_MISSINGTYPE = "Missing object type at %s"
ERROR_GEOJSON_INVALIDTYPE = "Non valid object type ('%s', allowed: %s)"
ERROR_GEOJSON_GEOMETRY_MISSINGCOORDINATES = "Missing coordinates field for %s"
# non valid geometry for OBJECT_TYPE: GEOMETRY DATA, BBOX
ERROR_GEOJSON_GEOMETRY_NONCOMPLIANT = "Non valid JSON %s geometry object: %s, (bbox: %s)"
ERROR_GEOJSON_SUBVALIDATION = "Internal object validation error: %s"
ERROR_GEOJSON_BBOX_INVALID = "Non valid bounding box: %s"
ERROR_GEOJSON_BBOX_CONFLICT = "Bounding box conflict: %s not inside %s"
ERROR_GEOJSON_INVALID_COLLECTION = "Non valid JSON %s collection object"
ERROR_GEOJSON_INVALID_CRS = "Non valid CRS field: %s"
ERROR_GEOJSON_CRS_OVERRIDE = "CRS field must be on the top-level object"


ERROR_INVALID_ANOMALY = "Invalid anomaly description: %s"