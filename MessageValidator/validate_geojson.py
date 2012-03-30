import json

from constants import *
from errors_msg import *

<<<<<<< HEAD
from validate_fields import validateFieldAsBoundingBox

=======
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
__author__ = 'Antonio Vaccarino'

def isBetween (value, limit_a, limit_b):

	if limit_b > limit_a:
		top = limit_b
		bottom = limit_a
	else:
		top = limit_a
		bottom = limit_b

	return bottom <= value <= top

<<<<<<< HEAD
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
=======
def validatePointAsValidPosition (coordinates, bbox=None):
	#Validates a field as a GeoJSON Position according to the number of axes defined in the constants.py file and against a given validated Bounding Box, if applicable

	if not (isinstance(coordinates, list) and len(coordinates)==COORD_AXES):
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
		return False

	for item in coordinates:
		if not isinstance(item, float):
			return False

	#Note: the bounding box must have been validated BEFORE running this
	if bbox is not None:
<<<<<<< HEAD
		for i in range (0, COORD_AXES_COMPARE):
			if not isBetween(coordinates[i], bbox[0][i], bbox[1][i]):
=======
		for i in range (0, COORD_AXES):
			if not isBetween(coordinates[i], bbox[i][0], bbox[i][1]):
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
				return False

	return True


def validateFieldAsGJPoint (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON Point and against a given validated bounding box, if applicable.

<<<<<<< HEAD
	
	if not (isinstance (fielddata, list)):
		return False

	if not (validatePointAsValidPosition(fielddata, bbox)):
=======
	# near duplicate from validateGeoJsonObject
	if not (isinstance (fielddata, list)):
		return False

	if not (validateFieldAsGJPoint(fielddata)):
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
		return False

	return True

def validateFieldAsGJMultiPoint (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON MultiPoint and against a given validated bounding box,if applicable.

<<<<<<< HEAD
	
=======
	# near duplicate from validateGeoJsonObject
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
	if not (isinstance (fielddata, list)):
		return False

	for point in fielddata:
		if not validatePointAsValidPosition(point, bbox):
			return False

	return True

def validateFieldAsGJLineString (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON LineString and against a given validated bounding box, if applicable.

<<<<<<< HEAD
	
=======
	# near duplicate from validateGeoJsonObject
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
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

<<<<<<< HEAD
	
=======
	# near duplicate from validateGeoJsonObject
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
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

<<<<<<< HEAD
	if not (isinstance (fielddata, list)):
		return False

	# Polygon should be made of LinearRings, all contained in the bbox
=======
	# near duplicate from validateGeoJsonObject
	if not (isinstance (fielddata, list)):
		return False

	# Polygon should be made of LinearRings
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
	for linearring in fielddata:
		if not validateFieldAsGJLinearRing(linearring, bbox):
			return False

<<<<<<< HEAD
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
	#Checks if the linearring contains the point. CONTAINS is valid if the point is inside, on a vertex or on the perimeter of linearring.

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
		Xo = point[1]

		# skip this segment if it cannot possibly pass through the point
		if not Xa <= Xo <= Xb:
			continue

		#1. normalization: point a becomes the cartesian origin
		#   the other points are adapted

		Xb = Xb - Xa
		Yb = Yb - Ya

		Xo = point[0]-Xa
		Yo = point[1]-Ya

		Xa = 0
		Ya = 0

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

=======
	#TODO: add check that ensures every subsequent linearring is INSIDE the preceding one and all inside the bbox

	return True

def validateFieldAsGJMultiPolygon (fielddata, bbox=None):
	#Validates a coordinates field as a valid GeoJSON Polygon and against a given validated bounding box, if applicable.

	# near duplicate from validateGeoJsonObject
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
	if not (isinstance (fielddata, list)):
		return False

	for polygon in fielddata:
		if not validateFieldAsGJPolygon(polygon, bbox):
			return False

	return True

<<<<<<< HEAD
#TODO: all geometry types done, still missing features and collections


def validateFieldAsGJGeometryCollection (fielddata, bbox=None):
	#Validates a "geometries" field as the list of geometry objects of a GeoJSON GeometryCollection

	if not (isinstance (fielddata, list)):
		return False

	for object in fielddata:
		if not (validateGeoJsonObject(object)):
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
		#if crs is of type linked, check that it has both str fields Type and Href
		if not (crsproperties.has_key(FIELDNAME_GEOJSON_CRS_LINKED_LINK) and instanceof(crsproperties[FIELDNAME_GEOJSON_CRS_LINKED_LINK], str)):
			return False
		if not (crsproperties.has_key(FIELDNAME_GEOJSON_CRS_LINKED_TYPE) and instanceof(crsproperties[FIELDNAME_GEOJSON_CRS_LINKED_TYPE], str)):
			return False
	elif fielddata[FIELDNAME_GEOJSON_CRS_TYPE] == FIELDVALUE_GEOJSON_CRS_TYPE_NAMED:
		#if crs is of type named, check that it has the str field Name
		if not (crsproperties.has_key(FIELDNAME_GEOJSON_CRS_NAMED_NAME) and instanceof(crsproperties[FIELDNAME_GEOJSON_CRS_NAMED_NAME], str)):
			return False
	else:
		#type of crs not recognized
		return False

	#All checks passed
	return True

=======
#TODO: all geometry types done (NEARLY, see polygon), now it's features and collections
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778


def validateMessageAsGeoJson (jsonmessage):

	#This function validates a json message as GeoJSON data according to:
	#http://geojson.org/geojson-spec.html

	# Parsing the json message into a dict
	try:
		jsondata = json.loads(jsonmessage)
	except Exception as current_error:
		return False, ("Not a JSON object? %s " % current_error.message)

	return validateGeoJsonObject (jsondata)

<<<<<<< HEAD
def validateGeoJsonObject (jsondata, bbox=None, sequence="/"):
=======
def validateGeoJsonObject (jsondata, sequence="/"):
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778

	#This function validates a json object as GeoJSON data according to:
	#http://geojson.org/geojson-spec.html

	#1. Checking common fields: type (mandatory), crs (optional), bbox (optional)

<<<<<<< HEAD


	#1.1 we check if the object has a valid type
	try:
		object_type = jsondata[FIELDNAME_GEOJSON_OBJECTTYPE]
		if object_type not in TYPES_GEOJSON_ALL:
			return False, (ERROR_GEOJSON_INVALIDTYPE % (object_type, TYPES_GEOJSON_ALL))
=======
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
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778
	except:
		return False, (ERROR_GEOJSON_MISSINGTYPE % sequence)

	#1.2 we validate the non-mandatory common fields
<<<<<<< HEAD

	#TODO: validate DECLARED bounding box (memeber) against GIVEN bounding box (parameter)

	#1.2.1 validating bounding box
	if jsondata.has_key(FIELDNAME_GEOJSON_BBOX):
		if validateFieldAsBoundingBox(jsondata[FIELDNAME_GEOJSON_BBOX]):
			bbox = convertToPointBasedBoundingBox(jsondata[FIELDNAME_GEOJSON_BBOX])
		else:
			return False, (ERROR_GEOJSON_INVALID_BBOX % sequence)
	else:
		bbox = None
		#we still create a bbox value (None) so we don't have a NameError later when calling the object validation

	#1.2.2 validating crs
	if jsondata.has_key(FIELDNAME_GEOJSON_CRS):
		if not (validateFieldAsCrs(jsondata[FIELDNAME_GEOJSON_CRS])):
			return False



	#NOTE: we assume the bounding box is validated now. If it validates here but does not work on the single objects there is a deeper breakage to investigate that does not have to do with the data validation process (that is why we do not re-validate it at single JSON object level)
=======
	#TODO: IMPLEMENT validateFieldAsCRS and validateFieldAsBbox
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778

	#2. Checking type-specific fields

	#2.1 checking for existence of "coordinates" field in geometry objects (except for GeometryCollection)
<<<<<<< HEAD

	validator_methods = {
		"Point": validateFieldAsGJPoint,
		"MultiPoint": validateFieldAsGJMultiPoint,
		"LineString": validateFieldAsGJLineString,
		"MultiLineString": validateFieldAsGJMultiLineString,
		"Polygon": validateFieldAsGJPolygon,
		"MultiPolygon": validateFieldAsGJMultiPolygon,
		}


	#TODO: COMPLETE IMPLEMENTATION (add handling of collections)
	#and remove hardcoded names and types

	if object_type in TYPES_GEOJSON_GEOMETRY:
		if not (jsondata.has_key(FIELDNAME_GEOJSON_COORDINATES)):
			return False, (ERROR_GEOJSON_GEOMETRY_INVALIDCOORDINATES % object_type)

		if not validator_methods[object_type](jsondata[FIELDNAME_GEOJSON_COORDINATES], bbox):
			return False, (ERROR_GEOJSON_GEOMETRY_NONCOMPLIANT % sequence)

	elif object_type == "GeometryCollection":
		if not (jsondata.has_key("geometries") and validateFieldAsGJGeometryCollection(jsondata["geometries"])):
			return False, (ERROR_GEOJSON_INVALID_COLLECTION % sequence)

	elif object_type == "Feature":
		#Feature object must contain a geometry key
		if not (jsondata.has_key("geometry")):
			return False
		#Geometry field must contain a GeoJSON geometry object OR a null (None in python) value
		elif not jsondata["geometry"] is None:
			if not (jsondata["geometry"].has_key("type") and jsondata["geometry"]["type"] in TYPES_GEOJSON_GEOMETRY):
				return False
			if not (validateGeoJsonObject(jsondata["geometry"],bbox=bbox)):
				return False

		#Feature object must contain a properties key
		if not (jsondata.has_key("properties")):
			return False
		#properties field must be either null/None or a JSON Object (i.e. Python dict)
		elif not (jsondata["properties"] is None or isinstance(jsondata["properties"], dict)):
			return False

		#NOTE: we are not validating the "id" field because the field is optional and we do not have any validation rule for its content


	elif object_type == "FeatureCollection":
		if not (jsondata.has_key("features")):
			return False
		else:
			for feature in jsondata["features"]:
				if not validateGeoJsonObject(feature, bbox):
					return False

	#TODO: FIX SEQUENCE BREADCRUMB HANDLING (NOTE: not sure if actually feasible)
=======
	if object_type in types_geometry:
		if not (jsondata.has_key(FIELDNAME_GEOJSON_COORDINATES) and isinstance(jsondata[FIELDNAME_GEOJSON_COORDINATES], list)):
			return False, (ERROR_GEOJSON_GEOMETRY_INVALIDCOORDINATES % sequence)

		if not validator_methods[object_type]():
			return False, (ERROR_GEOJSON_GEOMETRY_NONCOMPLIANT % sequence)


	#TODO: COMPLETE IMPLEMENTATION


	#TODO: FIX SEQUENCE BREADCRUMB HANDLING
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778



	# All checks passed
	return True