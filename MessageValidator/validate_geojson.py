import json

from constants import *
from errors_msg import *

__author__ = 'Antonio Vaccarino'

def isBetween (value, limit_a, limit_b):

	if limit_b > limit_a:
		top = limit_b
		bottom = limit_a
	else:
		top = limit_a
		bottom = limit_b

	return bottom <= value <= top

def validatePointAsValidPosition (coordinates, bbox=None):
	#Validates a field as a GeoJSON Position according to the number of axes defined in the constants.py file and against a given validated Bounding Box, if applicable

	if not (isinstance(coordinates, list) and len(coordinates)==COORD_AXES):
		return False

	for item in coordinates:
		if not isinstance(item, float):
			return False

	#Note: the bounding box must have been validated BEFORE running this
	if bbox is not None:
		for i in range (0, COORD_AXES):
			if not isBetween(coordinates[i], bbox[i][0], bbox[i][1]):
				return False

	return True


def validateFieldAsGJPoint (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON Point and against a given validated bounding box, if applicable.

	# near duplicate from validateGeoJsonObject
	if not (isinstance (fielddata, list)):
		return False

	if not (validateFieldAsGJPoint(fielddata)):
		return False

	return True

def validateFieldAsGJMultiPoint (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON MultiPoint and against a given validated bounding box,if applicable.

	# near duplicate from validateGeoJsonObject
	if not (isinstance (fielddata, list)):
		return False

	for point in fielddata:
		if not validatePointAsValidPosition(point, bbox):
			return False

	return True

def validateFieldAsGJLineString (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON LineString and against a given validated bounding box, if applicable.

	# near duplicate from validateGeoJsonObject
	if not (isinstance (fielddata, list)):
		return False

	#LineString should contain at least TWO positions
	if len(fielddata) < 2:
		return False

	for point in fielddata:
		if not validatePointAsValidPosition(point, bbox):
			return False

	return True

def validateFieldAsGJMultiLineString (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON MultiLineString and against a given validated bounding box, if applicable.

	# near duplicate from validateGeoJsonObject
	if not (isinstance (fielddata, list)):
		return False

	for linestring in fielddata:
		if not validateFieldAsGJLineString(linestring, bbox):
			return False

	return True

def validateFieldAsGJLinearRing (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON LinearRing and against a given validated bounding box, if applicable. Note that LinearRing is not used in itself, it is a specific condition of a LineString that is needed to handle Polygons

	#Must be a valid line string
	if not (validateFieldAsGJLineString(fielddata, bbox)):
		return False

	#Must have at least 4 points
	if len(fielddata) < 4:
		return False

	#The first and the last point must be the same
	if fielddata[0] != fielddata[-1]:
		return False

	return True

def validateFieldAsGJPolygon (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON Polygon and against a given validated bounding box, if applicable.

	# near duplicate from validateGeoJsonObject
	if not (isinstance (fielddata, list)):
		return False

	# Polygon should be made of LinearRings
	for linearring in fielddata:
		if not validateFieldAsGJLinearRing(linearring, bbox):
			return False

	#TODO: add check that ensures every subsequent linearring is INSIDE the preceding one and all inside the bbox

	return True

def validateFieldAsGJMultiPolygon (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON Polygon and against a given validated bounding box, if applicable.

	# near duplicate from validateGeoJsonObject
	if not (isinstance (fielddata, list)):
		return False

	for polygon in fielddata:
		if not validateFieldAsGJPolygon(polygon, bbox):
			return False

	return True

#TODO: all geometry types done (NEARLY, see polygon), now it's features and collections


def validateMessageAsGeoJson (jsonmessage):

	#This function validates a json message as GeoJSON data according to:
	#http://geojson.org/geojson-spec.html

	# Parsing the json message into a dict
	try:
		jsondata = json.loads(jsonmessage)
	except Exception as current_error:
		return False, ("Not a JSON object? %s " % current_error.message)

	return validateGeoJsonObject (jsondata)

def validateGeoJsonObject (jsondata, sequence="/"):

	#This function validates a json object as GeoJSON data according to:
	#http://geojson.org/geojson-spec.html

	#1. Checking common fields: type (mandatory), crs (optional), bbox (optional)

	types_all = ( "Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection", "Feature", "FeatureCollection" )
	#types_collection = ("GeometryCollection", "FeatureCollection", "MultiPolygon", "MultiLineString", "MultiPoint")
	types_geometry = ("Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon")

	#types_feature = ("Feature", "FeatureCollection")

	validator_methods = {
		"Point": validateFieldAsGJPoint,
	    "MultiPoint": validateFieldAsGJMultiPoint,
	    "LineString": validateFieldAsGJLineString,
	    "MultiLineString": validateFieldAsGJMultiLineString,
	    "Polygon": validateFieldAsGJPolygon,
	    "MultiPolygon": validateFieldAsGJMultiPolygon,
	}

	#1.1 we check if the object has a valid type
	try:
		object_type = jsondata['type']
		if object_type not in types_all:
			return False, (ERROR_GEOJSON_INVALIDTYPE % (object_type, types_all))
	except:
		return False, (ERROR_GEOJSON_MISSINGTYPE % sequence)

	#1.2 we validate the non-mandatory common fields
	#TODO: IMPLEMENT validateFieldAsCRS and validateFieldAsBbox

	#2. Checking type-specific fields

	#2.1 checking for existence of "coordinates" field in geometry objects (except for GeometryCollection)
	if object_type in types_geometry:
		if not (jsondata.has_key(FIELDNAME_GEOJSON_COORDINATES) and isinstance(jsondata[FIELDNAME_GEOJSON_COORDINATES], list)):
			return False, (ERROR_GEOJSON_GEOMETRY_INVALIDCOORDINATES % sequence)

		if not validator_methods[object_type]():
			return False, (ERROR_GEOJSON_GEOMETRY_NONCOMPLIANT % sequence)


	#TODO: COMPLETE IMPLEMENTATION


	#TODO: FIX SEQUENCE BREADCRUMB HANDLING



	# All checks passed
	return True