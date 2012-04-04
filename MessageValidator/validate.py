#!/usr/bin/env python
# -*- coding: utf-8 -*-
from error_handlers import ValidationError

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

import json

from errors_msg import *


def validateDictToTemplate (candidate, template):
	"""
	This function checks (recursively) that two dicts have the same structure and that the candidate respects a series of constraints defined by the template as either a specific type for the value OR as a specific range of possible values.

	:param candidate: a generic dictionary object
	:param template: a reference dictionary
	:return: boolean
	"""

	#STEP 1: check if we have the same key/value couples at the current level
	if not isinstance(candidate, dict):
		return False
	else:
		keys_candidate = candidate.keys()
		keys_candidate.sort()
		keys_template = template.keys()
		keys_template.sort()

		if keys_candidate != keys_template:
			return False




	#STEP 2: validate the values of each key/value couple according to granularity in the template
	for key in template:

		constraint = template[key]

		if isinstance (constraint, list):
			#2.1: validate against values range
			if not candidate[key] in constraint:
				return False
		elif isinstance(constraint, type):
			#2.2: validate against type
			if not isinstance(candidate[key], constraint):
				return False
		elif isinstance(constraint, dict):
			#2.3: recurse and check level below
			if not validateDictToTemplate (candidate[key], template[key]):
				return False

	return True

def validateDictToTemplateAndLog (candidate, template, sequence="/"):
	"""This function checks (recursively) that two dicts have the same structure and that the candidate respects a series of constraints defined by the template as either a specific type for the value OR as a specific range of possible values. Based on the validateDictToTemplate function
	#The function returns a tuple with True/False and a list of the errors encountered in the comparison or the dict data.

	:param candidate: candidate dict
	:param template: template dict against which the candidate is validated
	:param sequence: key sequence for breadcrumb reporting (set automatically)
	:return: tuple with True/False validation result and validated dict/errors list
	"""


	validation_errors = []

	#STEP 1: check if we have the same number of key/value couples at the current level

	try:
		keys_candidate = candidate.keys()
		keys_candidate.sort()
		keys_template = template.keys()
		keys_template.sort()

		if keys_candidate != keys_template:
			return False, [ERROR_FIELDS_MISMATCH % sequence,]

	except:
		return False, [ERROR_NO_DICT % sequence,]

	#STEP 2: validate the values of each key/value couple according to granularity in the template
	for key in template:

		constraint = template[key]
		currentpath = sequence+"/"+key

		if isinstance (constraint, list):
			#2.1: validate against values range
			if not candidate[key] in constraint:
				validation_errors.append(ERROR_VALUE_NOT_IN_RANGE % (currentpath, candidate[key], constraint))
		elif isinstance(constraint, type):
			#2.2: validate against type
			if not isinstance(candidate[key], constraint):
				validation_errors.append(ERROR_VALUE_WRONG_TYPE % (currentpath, type(candidate[key]), constraint))
		elif isinstance(constraint, dict):
			#2.3: recurse and check level below
			next_level_validation, report = validateDictToTemplateAndLog (candidate[key], template[key], currentpath)
			if next_level_validation is not True:
				validation_errors = validation_errors + report

	if len(validation_errors) > 0:
		return False, validation_errors
	else:
		return True, candidate

def parseJsonMessage (jsonmessage):
	"""
	Validates and parses a json message into a Python dict
	:param jsonmessage: unicode, stringified json message
	:return: dict
	"""

	try:
		jsondata = json.loads(jsonmessage)
	except Exception as current_error:
		#NOTE: in this case we put the error message from the original
		raise ValidationError (ERROR_JSON_PARSING+"\n"+current_error.message, jsonmessage)

	return jsondata


def validateJsonToTemplate (jsonmessage, template):
	"""Checks that a json message has the same structure as a reference dictionary and that the json message respects a series of constraints defined by the template as either a specific type for the value OR as a specific range of possible values.
	Returns a tuple with two values: the True/False result and the parsed json or the errors list

	:param jsonmessage: stringified json data, not yet in python dict form
	:param template:
	:return: tuple (bool, validation result/parsed message)
	"""


	# Parsing the json message into a dict

	candidate = parseJsonMessage(jsonmessage)

	validated, data = validateDictToTemplateAndLog(candidate, template)
	if not validated:
		return False, data
	else:
		return True, data


