#!/usr/bin/env python
# -*- coding: utf-8 -*-
from validate_geojson import validateGeoJsonObject

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

from validate import *
from validate_fields import *
from constants import *
import validation_templates

#TODO: general clean up of hardcoded and semi-hardcoded values


def validateMessageResponseCapabilities (jsonmessage):
	"""
	Validates a json message as a proper capabilities response message for the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	# General comparison of the dictionary structure,
	# we don't continue checking if this does not work because fields may be missing
	validated, messagedata = validateJsonToTemplate(jsonmessage, validation_templates.template_response_capabilities)

	if not validated:
		return validated, messagedata


	validation_errors = []
	if not validateFieldAsActiveUrl(messagedata[FIELDNAME_DISCOVERY_URL]):
		validation_errors.append ("Field %s is not a working URL" % FIELDNAME_DISCOVERY_URL)
	if not validateFieldAsTimeSpan(messagedata[FIELDNAME_DISCOVERY_TIMESPAN]):
		validation_errors.append ("Field %s is not a valid timespan" % FIELDNAME_DISCOVERY_TIMESPAN)
	if not validateFieldAsBoundingBox(messagedata[FIELDNAME_DISCOVERY_BBOX]):
		validation_errors.append("Field %s is not a valid bounding box" % FIELDNAME_DISCOVERY_BBOX)

	if len(validation_errors) > 0:
		return False, validation_errors
	else:
		return True, messagedata

def validateMessageResponseWelcome (jsonmessage):
	"""
	Validates a json message as a proper welcome response message from the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error message/json dict)
	"""

	return validateJsonToTemplate(jsonmessage, validation_templates.template_response_welcome)

def validateMessageResponseRead (jsonmessage):
	"""
	Validates a json message as a proper read response message from the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""
	validated, messagedata = validateJsonToTemplate(jsonmessage, validation_templates.template_response_read)

	if not validated:
		return False, messagedata

	validation_errors = []
	for gjobject in messagedata[FIELDNAME_LISTING_DATA][FIELDNAME_LISTING_UPSERT]:
		validated, objectdata = validateGeoJsonObject (gjobject)
		if not validated:
			validation_errors.append (objectdata)

	for dataid in messagedata[FIELDNAME_LISTING_DATA][FIELDNAME_LISTING_DELETE]:
		if not isinstance(dataid, unicode):
			validation_errors.append(ERROR_VALUE_WRONG_TYPE % (type(dataid), unicode))

	if len(validation_errors) > 0:
		return False, validation_errors
	else:
		return True, messagedata

def validateMessageRequestWrite (jsonmessage):
	"""
	Validates a json message as a proper write request message for the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""
	validated, messagedata = validateJsonToTemplate(jsonmessage, validation_templates.template_request_write)

	if not validated:
		return False, messagedata

	validation_errors = []
	for gjobject in messagedata[FIELDNAME_LISTING_DATA][FIELDNAME_LISTING_UPSERT]:
		validated, objectdata = validateGeoJsonObject (gjobject)
		if not validated:
			validation_errors.append (objectdata)

	for dataid in messagedata[FIELDNAME_LISTING_DATA][FIELDNAME_LISTING_DELETE]:
		if not isinstance(dataid, unicode):
			validation_errors.append(ERROR_VALUE_WRONG_TYPE % (type(dataid), unicode))

	if len(validation_errors) > 0:
		return False, validation_errors
	else:
		return True, messagedata

def validateMessageResponseWrite (jsonmessage):
	"""
	Validates a json message as a proper write response message from the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""
	validated, messagedata = validateJsonToTemplate(jsonmessage, validation_templates.template_response_write)
	if not validated:
		return False, messagedata

	validation_errors = []
	for dataid in messagedata[FIELDNAME_LISTING_ACKNOWLEDGE][FIELDNAME_LISTING_UPSERT]:
		if not (isinstance(dataid, unicode)):
			validation_errors.append(ERROR_VALUE_WRONG_TYPE % (type(dataid), unicode))

	for dataid in messagedata[FIELDNAME_LISTING_ACKNOWLEDGE][FIELDNAME_LISTING_DELETE]:
		if not (isinstance(dataid, unicode)):
			validation_errors.append(ERROR_VALUE_WRONG_TYPE % (type(dataid), unicode))

	for anomaly in messagedata[FIELDNAME_LISTING_ANOMALIES]:
		if not validateFieldAsAnomaly(anomaly):
			validation_errors.append (ERROR_INVALID_ANOMALY % anomaly)

	if len(validation_errors) > 0:
		return False, validation_errors

	return True, messagedata


def validateMessageRequestQuery (jsonmessage):
	"""
	Validates a json message as a proper query request message for the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error message/json dict)
	"""
	validated, messagedata = validateJsonToTemplate(jsonmessage, validation_templates.template_request_query)

	if not validated:
		return False, messagedata


	bboxfield = messagedata["query"]["BB"]
	if not (validateFieldAsBoundingBox(bboxfield) or len(bboxfield)==0):
		return False, ERROR_GEOJSON_BBOX_INVALID % bboxfield

	if not (validateFieldAsIsoDateTime(messagedata["query"]["time"])):
		return False, ERROR_INVALID_DATETIME % messagedata["query"]["time"]

	return True, messagedata

def validateMessageAnomaly (jsonmessage):
	"""
	Validates a json message as a proper error message and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error message/json dict)
	"""

	validated, messagedata = validateJsonToTemplate (jsonmessage, validation_templates.template_error_anomaly)

	if not validated:
		return False, messagedata

	for anomaly in messagedata[FIELDNAME_LISTING_ANOMALIES]:
		if not validateFieldAsAnomaly(anomaly):
			return False, ERROR_INVALID_ANOMALY % anomaly

	return True, messagedata

def validateMessageError (jsonmessage):
	"""
	Validates a json message as a proper error message and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error message/json dict)
	"""

	return validateJsonToTemplate (jsonmessage, validation_templates.template_error_error)

def validateMessageRequestApi (jsonmessage):
	"""
	Validates a json message as a proper API request message for the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	validated, messagedata = validateJsonToTemplate (jsonmessage, validation_templates.template_request_api)

	if not validated:
		return False, messagedata

	if not validateFieldAsBoundingBox(jsonmessage["query"]["BB"]):
		return False, ERROR_GEOJSON_BBOX_INVALID % jsonmessage["query"]["BB"]

	return True, messagedata

