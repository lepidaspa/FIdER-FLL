import httplib
import re
import string
import urlparse
import datetime


from constants import *

__author__ = 'Antonio Vaccarino'

def validateFieldAsIsoDateTime (isostring):
	#Validates a ISO8601 datetime string with time zone, first by checking the notation and then the values

	#If the string is not well formed, stop now
	if validateFieldAsIsoDateTimeNotation(isostring) in (False, None):
		return False

	#finding all number groups in the string
	regex = re.compile(r"\d{2}")

	#splitting the datetime string in date and time+timezone
	try:
		datestring, timezonestring = isostring.split("T")
	except:
		return False

	#All parts of the date are mandatory
	try:
		elements_date = regex.findall(datestring)
		field_date = [int(elements_date[0]+elements_date[1]), int(elements_date[2]), int(elements_date[3])]
		#ignoring BC dates on purpose
	except:
		return False

	# passing the date to datetime
	try:
		validateddate = datetime.datetime (field_date[0], field_date[1], field_date[2])
	except:
		return False

	#Splitting time and timezone
	tzseparators = ("Z+-")
	hastzdata = False
	for sep in tzseparators:
		if sep in timezonestring:
			hastzdata = True
			timestring, ztype, zonestring = timezonestring.partition(sep)
			break
	if not hastzdata:
		return False


	#Building time data; we may have hh, hh[:]mm, hh[:]mm[:]ss
	field_time = [0, 0, 0]
	elements_time = regex.findall(timestring)
	try:
		for i in range (0, len(elements_time)):
			field_time[i]=int(elements_time[i])
		#validating time data
		if field_time[0] > 24 or field_time[1] > 59 or field_time[2] > 59:
			return False
	except:
		return False



	#Building zone data; we may have hh or hh[:]mm if we have +/-, nothing if we have Z (UTC)
	field_zone = [0, 0]
	if ztype == "+" or ztype == "-":
		elements_zone = regex.findall(zonestring)
		for i in range (0, len(elements_zone)):
			field_zone[i]=int(elements_zone[i])
		# Python does not have time zone validation built in, so we check it here
		# Note that +/- has been removed so we are working with abs values
		if field_zone[0] > 13 or field_zone[1] > 59:
			return False
	elif ztype == "Z":
		if zonestring != '':
			return False
	#No valid TZ descriptor
	else:
		return False

	#All checks passed, date time and timezone are valid
	return True


def validateServerToken (tokenstring):
	#TODO: verify if this can be implemented during validation or if there is not enough rules to check it without the actual tokens list
	return True


def validateFieldAsIsoDateTimeNotation (datestring):
	#This function parses a mostly generic ISO8601 date string with timezone

	regex_string = r"[\+\-]{0,1}(\d{8}|\d{4}-\d{2}-\d{2})T\d{2}(:{0,1}\d{2}){0,2}(Z|([\+\-]{1}\d{2}(:{0,1}\d{2})))"

	if isinstance(datestring, str):
		return re.match(datestring, regex_string)
	else:
		# wrong data type
		return False

def validateFieldAsActiveUrl (fielddata):
	#Url definition: string starting with http:// (or https:// ?), then domain data and any number of subdirs in the paths
	try:
		parsed = urlparse.urlparse(fielddata)
	except:
		return False

	#Checking if we are using one of the allowed protocols
	if parsed.scheme not in ('http', 'https'):
		return False

	#Testing if the URL actually exists
	#TODO: verify if we need proxy settings and such to try this
	conn = httplib.HTTPConnection(parsed.scheme+"://"+parsed.netloc)
	conn.request('HEAD', parsed.path)
	response = conn.getresponse()
	conn.close()
	if response.status != 200:
		return False

	#If all checks are passed
	return True


def validateFieldAsTimeSpan (fielddata):
	#TimeSpan definition: list with two datetime + timezone strings
	#TODO: actual date parsing to that we can verify the timespan is realistic? (e.g. element 1 BEFORE element2)

	if not (isinstance(fielddata, list) and len(fielddata)==2):
		return False
	else:
		if not ( validateFieldAsIsoDateTime(fielddata[0]) and validateFieldAsIsoDateTime(fielddata[1]) ):
			return False

	return True

def validateFieldAsBoundingBox (fielddata):
<<<<<<< HEAD
	#Bounding box definition: array of 2*COORD_AXES_MODEL values (see constants) coordinates each as float values, direction S-N / W-E

	#1. Checking if value is a collection of 2 arrays
	if not (isinstance(fielddata, list) and len(fielddata)==2*COORD_AXES_MODEL):
		return False

	#2. Checking if each element in the coords array is of the correct type
	for coord in coords:
		if not (isinstance(coord, float)):
			return False

	#3. Checking if the relative position of the points in the bounding box is consistent. Note that we this is 2D only
	#IMPORTANT NOTE: will NOT work if passing through the opposite Prime Meridian
	for axis in range(0,2):
		if not fielddata[axis] <= fielddata[COORD_AXES_MODEL+axis]:
			return False

	#All checks passed
	return True

=======
	#Bounding box definition: collection of 2 arrays of COORD_AXES (see constants) coordinates each as int values, direction S-N / W-E

	#1. Checking if value is a collection of 2 arrays
	if isinstance(fielddata, list) and len(fielddata)==2:
		#2. Checking if each array is made of 2 elements
		for coords in fielddata:
			if isinstance(coords, list) and len(coords)==COORD_AXES:
				#3. Checking if each element in the coords array is an int
				for coord in coords:
					if not (isinstance(coord, float)):
						return False
		#4. Checking if the relative position of the points in the bounding box is consistent
		if fielddata[0][0] <= fielddata[1][0] and fielddata[0][1] <= fielddata[1][1]:
			return True

	# Failed at least one check
	return False
>>>>>>> 00e8c9a1e66057dda8996bebf46019e22751c778


def validateFieldAsMetadataListing (fielddata):
	#This function validates the field as list of metadata
	#A metadata is a dictionary with one name field string (unique in the list) and two optional fields (timespan and bounding box)

	# checking field type
	if not (isinstance(fielddata, list)):
		return False

	metadatanames = []
	for metadata in fielddata:

		#checking for type
		if not isinstance(metadata, dict):
			return False

		#checking mandatory name field
		if not metadata.has_key(FIELDNAME_METADATA_NAME):
			#metadata must have a name
			return False
		elif not isinstance(metadata[FIELDNAME_METADATA_NAME], str):
			#metadata name must be a string
			return False
		elif metadata[FIELDNAME_METADATA_NAME] in metadatanames:
			#metadata name must be unique
			return False

		#checking optional field 'time'
		if metadata.has_key(FIELDNAME_METADATA_TIMESPAN):
			if not validateFieldAsTimeSpan(metadata[FIELDNAME_METADATA_TIMESPAN]):
				return False

		#checking optional field 'area'
		if metadata.has_key(FIELDNAME_METADATA_BBOX):
			if not validateFieldAsBoundingBox(metadata[FIELDNAME_METADATA_BBOX]):
				return False

	return True

def validateFieldAsDataIds (fielddata):
	#This function verifies if the data provided by the field is realistic as a series of ID for our database
	#TODO: check if IDs are numeric only or alphanumeric and implement
	return True

