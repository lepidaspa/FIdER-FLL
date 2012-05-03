#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MessageTemplates
from MessageValidator import validateDictToTemplate
import validate_geojson


__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

import httplib
import re
import urlparse
import datetime

from constants import *

def validateFieldAsIsoDateTime (isostring):
	"""
	Validates a generic string as ISO8601 datetime string with time zone, first by checking the notation and then the fields values

	:param isostring: candidate ISO8601 string
	:return: bool
	"""

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
	if not isinstance(tokenstring, unicode):
		return False

	return True


def validateFieldAsIsoDateTimeNotation (datestring):
	"""Validates the format of a generic string as campatible with the structure of an ISO 8601 datetime string. Values are not cheked

	:param datestring: unicode
	:return: bool
	"""

	#regex_string = r"[\+\-]{0,1}(\d{8}|\d{4}-\d{2}-\d{2})T\d{2}(:{0,1}\d{2}){0,2}(Z|([\+\-]{1}\d{2}(:{0,1}\d{2})))"
	regex_string = r"[\+\-]{0,1}(\d{8}|\d{4}-\d{2}-\d{2})T\d{2}(:{0,1}\d{2}){0,2}(Z|([\+\-]{1}\d{2}(:{0,1}\d{2})))"

	if isinstance(datestring, unicode):
		return bool(re.match(regex_string, datestring))
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

	try:

		if parsed.scheme == "http":
			conn = httplib.HTTPConnection(parsed.netloc)
		elif parsed.scheme == "https":
			conn = httplib.HTTPSConnection(parsed.netloc)


		conn.request('HEAD', parsed.path)
		response = conn.getresponse()
		conn.close()

		#TODO: move answers_valid to constants
		#TODO: decide the full range of acceptable answers from sites
		answers_valid = (200, 302, 303)
		if not response.status in answers_valid:
			return False
	except:
		return False



	#If all checks are passed
	return True


def validateFieldAsTimeSpan (fielddata):
	"""Validates a field as timespan data, defined as: list with two datetime + timezone strings

	:param fielddata:
	:return:
	"""



	if not (isinstance(fielddata, list) and len(fielddata)==2):
		return False
	else:
		if not ( validateFieldAsIsoDateTime(fielddata[0]) and validateFieldAsIsoDateTime(fielddata[1]) ):
			return False

	return True



def validateFieldAsBoundingBox (fielddata):
	#Bounding box definition: array of 2*COORD_AXES_MODEL values (see constants) coordinates each as float values, direction S-N / W-E

	#1. Checking if value is a collection of 2*COORD_AXES_MODEL values
	if not (isinstance(fielddata, list) and len(fielddata)==2*COORD_AXES_MODEL):
		return False

	#2. Checking if each element in the coords array is of the correct type
	for coord in fielddata:
		if not (isinstance(coord, float)):
			return False

	#3. Checking if the relative position of the points in the bounding box is consistent (or corner 1 coordinates < same coordinates on corner 2)
	#IMPORTANT NOTE: will NOT work if passing through the opposite Prime Meridian
	for axis in range(0,COORD_AXES_COMPARE):
		if not fielddata[axis] <= fielddata[COORD_AXES_MODEL+axis]:
			return False

	#All checks passed
	return True

def validateFieldAsGJListing (fielddata):
	"""
	Validates the field as a list of geojson objects
	:param fielddata:
	:return: bool
	"""

	if not isinstance (fielddata, (list, tuple)):
		return False

	for element in fielddata:
		if not validate_geojson.validateGeoJsonObject(element):
			return False

	return True





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
		elif not isinstance(metadata[FIELDNAME_METADATA_NAME], unicode):
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
	#TODO: check if IDs are numeric only or alphanumeric and implement?
	return isinstance(fielddata, str)

def validateFieldAsAnomaly (fielddata):

	return validateDictToTemplate(fielddata, MessageTemplates.model_field_anomaly, MessageTemplates.process_field_anomaly, withlog=False)