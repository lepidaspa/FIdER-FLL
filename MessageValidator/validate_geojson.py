#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

from constants import *
from errors_msg import *
from validate_fields import validateFieldAsBoundingBox
from validate import parseJsonMessage


def isBetween (value, limit_a, limit_b):

	if limit_b > limit_a:
		top = limit_b
		bottom = limit_a
	else:
		top = limit_a
		bottom = limit_b

	return bottom <= value <= top

def convertToPointBasedBoundingBox (bbox):
	#convert a validated bounding box to one based on a double list, one per vertex
	pbb = [[],[]]

	for i in range (0, COORD_AXES_MODEL):
		pbb[0][i] = bbox[i]
		pbb[1][i] = bbox[COORD_AXES_MODEL+i]

	return pbb

def validatePointAsValidPosition (coordinates, bbox=None):
	#Validates a field as a GeoJSON Position according to the number of axes defined in the constants.py file and against a given validated Bounding Box, if applicable

	#we validate the coordinates as properly formed (with the number of axes specified as data model, COORD_AXES_MODEL) but we compare it to the bounding box with the number of axes relevant to the bounding box model (COORD_AXES_BBOX)

	if not (isinstance(coordinates, list) and len(coordinates)==COORD_AXES_MODEL):
		return False

	for item in coordinates:
		if not isinstance(item, float):
			return False

	#Note: the bounding box must have been validated BEFORE running this
	if bbox is not None:
		for i in range (0, COORD_AXES_COMPARE):
			if not isBetween(coordinates[i], bbox[0][i], bbox[1][i]):
				return False

	return True


def validateFieldAsGJPoint (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON Point and against a given validated bounding box, if applicable.

	
	if not (isinstance (fielddata, list)):
		return False

	if not (validatePointAsValidPosition(fielddata, bbox)):
		return False

	return True

def validateFieldAsGJMultiPoint (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON MultiPoint and against a given validated bounding box,if applicable.

	
	if not (isinstance (fielddata, list)):
		return False

	for point in fielddata:
		if not validatePointAsValidPosition(point, bbox):
			return False

	return True

def validateFieldAsGJLineString (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON LineString and against a given validated bounding box, if applicable.

	
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

	if not (isinstance (fielddata, list)):
		return False

	# Polygon should be made of LinearRings, all contained in the bbox
	for linearring in fielddata:
		if not validateFieldAsGJLinearRing(linearring, bbox):
			return False

	#NOTE: the validation of the inner linearrings does NOT follow the GeoJSON specifications. We are not checking that the linearrings are consistently concentric but only that no point is out of the initial linearring. This since some tools create polygons with non-concentric inner holes and notate them as GeoJSON polygons. For display purpose, the maps will simply ignore the inner rings and use the first ring as bounds of the area.
	if len(fielddata)>1:
		for i in range (1, len(fielddata)):
			if not containsLinearRing (fielddata[0], fielddata[i]):
				return False

	return True

def containsLinearRing (external, internal):
	#Checks if the internal linearring is contained in the external linearring, both having already been validated. Returns false if ANY point of internal is outside external, returns true if all points are inside or on the perimeter or on vertex (see containsPoint). CHECKED on *2D* only

	for position in internal:
		if not containsPoint (external, position):
			return False

	return True

def containsPoint (linearring, point):
	"""
	Checks if the linearring contains the point. CONTAINS is valid if the point is inside, on a vertex or on the perimeter of linearring.
	"""

	#quick check: if the point is in the same spot as a vertex we consider it inside
	for vertex in linearring:
		if vertex == point:
			return True

	"""
	points defined for each point vs segment check
	o = origin, point to be verified
	a = starting point of the segment
	b = ending point of the segment
	"""

	isinside = False

	# skipping point 0 as 0 and -1 are the same so cannot create the segment properly
	for i in range (1, len(linearring)):

		Xa = linearring[i-1][0]
		Ya = linearring[i-1][1]

		Xb = linearring[i][0]
		Yb = linearring[i][1]

		Xo = point[0]
		Yo = point[1]

		# skip this segment if it cannot possibly pass through the point
		if not Xa <= Xo <= Xb:
			continue

		#1. normalization: point a becomes the cartesian origin
		#   the other points are adapted

		Xb = Xb - Xa
		Yb = Yb - Ya

		Xo = Xo-Xa
		Yo = Yo-Ya


		#Xa = 0
		#Ya = 0

		#2. creating the function for point A to B
		#rounding for tolerance: in map terms we accept that a point is on the bounds of a linearring if it's less than ~1 meter away
		segment_incline = round(float(Yb)/Xb, 5)
		point_incline = round(float(Yo)/Xo, 5)

		if segment_incline > point_incline:
			# the vertical line intersects the linearring, so we switch the state of the isinside verification boolean
			isinside = not isinside
		elif segment_incline == point_incline:
			#if the point is ON the segment we consider it inside
			return True

	return isinside


def validateFieldAsGJMultiPolygon (fielddata, bbox=None):

	#Validates a coordinates field as a valid GeoJSON Polygon and against a given validated bounding box, if applicable.

	if not (isinstance (fielddata, list)):
		return False

	for polygon in fielddata:
		if not validateFieldAsGJPolygon(polygon, bbox):
			return False

	return True


def validateFieldAsGJGeometryCollection (fielddata, bbox=None):
	#Validates a "geometries" field as the list of geometry objects of a GeoJSON GeometryCollection

	if not (isinstance (fielddata, list)):
		return False

	for object in fielddata:
		if not (validateGeoJsonObject(object, bbox)):
			return False

	return True


def validateFieldAsCrs (fielddata):
	#Validates a field as a CRS definition dictionary
	# does not actually check if the CRS is correct, only that the information
	# is structured properly (fields, etc)

	if not (isinstance(fielddata, dict) and fielddata.has_key(FIELDNAME_GEOJSON_CRS_TYPE) and fielddata.has_key(FIELDNAME_GEOJSON_CRS_PROPERTIES)):
		return False

	crsproperties = fielddata[FIELDNAME_GEOJSON_CRS_PROPERTIES]

	if fielddata[FIELDNAME_GEOJSON_CRS_TYPE] == FIELDVALUE_GEOJSON_CRS_TYPE_LINKED:
		#if crs is of type linked, check that it has both unicode fields Type and Href
		if not (crsproperties.has_key(FIELDNAME_GEOJSON_CRS_LINKED_LINK) and isinstance(crsproperties[FIELDNAME_GEOJSON_CRS_LINKED_LINK], unicode)):
			return False
		if not (crsproperties.has_key(FIELDNAME_GEOJSON_CRS_LINKED_TYPE) and isinstance(crsproperties[FIELDNAME_GEOJSON_CRS_LINKED_TYPE], unicode)):
			return False
	elif fielddata[FIELDNAME_GEOJSON_CRS_TYPE] == FIELDVALUE_GEOJSON_CRS_TYPE_NAMED:
		#if crs is of type named, check that it has the unicode field Name
		if not (crsproperties.has_key(FIELDNAME_GEOJSON_CRS_NAMED_NAME) and isinstance(crsproperties[FIELDNAME_GEOJSON_CRS_NAMED_NAME], unicode)):
			return False
	else:
		#type of crs not recognized
		return False

	#All checks passed
	return True



def validateMessageAsGeoJson (jsonmessage):

	#This function validates a json message as GeoJSON data according to:
	#http://geojson.org/geojson-spec.html

	jsondata = parseJsonMessage (jsonmessage)

	return validateGeoJsonObject (jsondata)

def validateGeoJsonObject (jsondata, bbox=None, sequence="/"):
	"""
	This function validates a json object as GeoJSON data according to: http://geojson.org/geojson-spec.html
	NOTE: the bbox parameter is only available so that it a bounding box from a container object can be passed to a contained object. As such, it is validated and transformed in a [[coordinates0][coordinates1]] format at step 1.2.1 of the function. It can be passed by hand, but will not be validated or checked for errors; the only validation that is  done is, again at step 1.2.1, by checking that the sub-bbox is inside the container bbox.

	:param jsondata:
	:param bbox:
	:param sequence:
	:return:
	"""


	#1. Checking common fields: type (mandatory), crs (optional), bbox (optional)

	#1.1 we check if the object has a valid type and store it for later checks
	try:
		object_type = jsondata[FIELDNAME_GEOJSON_OBJECTTYPE]
		if object_type not in TYPES_GEOJSON_ALL:
			return False, ERROR_GEOJSON_INVALIDTYPE % (object_type, TYPES_GEOJSON_ALL)
	except:
		return False, ERROR_GEOJSON_MISSINGTYPE % sequence

	#1.2 we validate the non-mandatory common fields

	#1.2.1 validating bounding box (optional field)
	if jsondata.has_key(FIELDNAME_GEOJSON_BBOX):
		if validateFieldAsBoundingBox(jsondata[FIELDNAME_GEOJSON_BBOX]):
			# for cleaner handling by the validation functions, the program converts a [x0, y0, x1, y1] bbox to the format [[x0, y0],[x1, y1]]
			localbbox = convertToPointBasedBoundingBox(jsondata[FIELDNAME_GEOJSON_BBOX])
			# Checking that the new bounding box is contained or equal to the given bounding box
			for axis in range (0, COORD_AXES_COMPARE):
				if localbbox[0][axis] < bbox[0][axis] or localbbox[1][axis] > bbox[1][axis]:
					return False, ERROR_GEOJSON_BBOX_CONFLICT % (localbbox, bbox)
			bbox = localbbox

		else:
			return False, ERROR_GEOJSON_BBOX_INVALID % jsondata[FIELDNAME_GEOJSON_BBOX]


	#1.2.2 validating crs (optional field)
	if jsondata.has_key(FIELDNAME_GEOJSON_CRS):
		if not (validateFieldAsCrs(jsondata[FIELDNAME_GEOJSON_CRS])):
			return False, ERROR_GEOJSON_INVALID_CRS % jsondata[FIELDNAME_GEOJSON_CRS]


	#NOTE: we assume the bounding box is validated now. If it validates here but does not work on the single objects there is a deeper breakage to investigate that does not have to do with the data validation process (that is why we do not re-validate it at single JSON object level)

	#2. Checking type-specific fields

	#2.1 checking for existence of "coordinates" field in geometry objects (except for GeometryCollection)

	validator_methods = {
		"Point": validateFieldAsGJPoint,
		"MultiPoint": validateFieldAsGJMultiPoint,
		"LineString": validateFieldAsGJLineString,
		"MultiLineString": validateFieldAsGJMultiLineString,
		"Polygon": validateFieldAsGJPolygon,
		"MultiPolygon": validateFieldAsGJMultiPolygon,
	}


	if object_type in TYPES_GEOJSON_GEOMETRY:
		if not (jsondata.has_key(FIELDNAME_GEOJSON_COORDINATES)):
			return False, ERROR_GEOJSON_GEOMETRY_MISSINGCOORDINATES % object_type

		if not validator_methods[object_type](jsondata[FIELDNAME_GEOJSON_COORDINATES], bbox):
			return False, ERROR_GEOJSON_GEOMETRY_NONCOMPLIANT % (object_type, jsondata[FIELDNAME_GEOJSON_COORDINATES], bbox)

	elif object_type == "GeometryCollection":
		if not (jsondata.has_key(FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRIES) and validateFieldAsGJGeometryCollection(jsondata[FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRIES])):
			return False, ERROR_GEOJSON_INVALID_COLLECTION % "GeometryCollection"

	elif object_type == "Feature":
		#Feature object must contain a geometry key
		if not (jsondata.has_key(FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRY)):
			return False, ERROR_GEOJSON_INVALID_COLLECTION % "Feature"
		#Geometry field must contain a GeoJSON geometry object OR a null (None in python) value
		elif not jsondata[FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRY] is None:
			if not (jsondata[FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRY].has_key(FIELDNAME_GEOJSON_OBJECTTYPE) and jsondata[FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRY][FIELDNAME_GEOJSON_OBJECTTYPE] in TYPES_GEOJSON_GEOMETRY):
				return False, ERROR_GEOJSON_INVALID_COLLECTION % "Feature"

			#We validate the internal object/s
			validated, validationdata = validateGeoJsonObject(jsondata[FIELDNAME_GEOJSON_COLLECTIONS_GEOMETRY], bbox)
			if not validated:
				return False, ERROR_GEOJSON_SUBVALIDATION % (validationdata)

		#Feature object must contain a properties key
		if not (jsondata.has_key(FIELDNAME_GEOJSON_COLLECTIONS_PROPERTIES)):
			return False, ERROR_GEOJSON_INVALID_COLLECTION % "Feature"
		#properties field must be either null/None or a JSON Object (i.e. Python dict)
		elif not ((jsondata[FIELDNAME_GEOJSON_COLLECTIONS_PROPERTIES] is None or isinstance(jsondata[FIELDNAME_GEOJSON_COLLECTIONS_PROPERTIES], dict))):
			return False, ERROR_GEOJSON_INVALID_COLLECTION % "Feature"

		#NOTE: we are not validating the "id" field because the field is optional and we do not have any validation rule for its content


	elif object_type == "FeatureCollection":
		if not (jsondata.has_key(FIELDNAME_GEOJSON_COLLECTIONS_FEATURES) and isinstance(jsondata[FIELDNAME_GEOJSON_COLLECTIONS_FEATURES], list)):
			return False, ERROR_GEOJSON_INVALID_COLLECTION % "FeatureCollection"
		else:
			for feature in jsondata[FIELDNAME_GEOJSON_COLLECTIONS_FEATURES]:
				validated, validationdata = validateGeoJsonObject(feature, bbox)
				if not validated:
					return False, ERROR_GEOJSON_SUBVALIDATION % (validationdata)


	#TODO: add real breadcrumb support through sequence (wishful thinking)


	# All checks passed
	return True