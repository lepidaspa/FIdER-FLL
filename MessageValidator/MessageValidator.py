#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from error_handlers import ValidationError
from errors_msg import ERROR_JSON_PARSING

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en' 


from MarconiLabsTools import ArDiVa



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

def validateJsonToTemplate (jsonmessage, model, script=None, strictness=ArDiVa.Model.VAL_STRICT):
	"""Checks that a json message has the same structure as a reference dictionary and that the json message respects a series of constraints defined by the template as either a specific type for the value OR as a specific range of possible values.
	Returns a tuple with two values: the True/False result and the parsed json or the errors list

	:param jsonmessage: stringified json data, not yet in python dict form
	:param model: ArDiVa Model compliant dictionary
	:param script: ArDiVa Process compliant list
	:param strictness: strictness level, defaults to maximum (all keys match perfectly, no optional keys allowed)
	:return: tuple (bool, validation result/parsed message)
	"""



	candidate = parseJsonMessage(jsonmessage)

	return validateDictToTemplate (candidate, model, script, strictness)

def validateDictToTemplate (candidate, model, script=None, strictness=ArDiVa.Model.VAL_STRICT, withlog=True):

	validator = ArDiVa.Validator (model, script)
	validator.model.setDefaultRule(strictness)

	if withlog is True:
		if validator.model.validateCandidate(candidate, strictness) and validator.process.performValidations():
			return True, candidate
		else:
			return False, validator.getLog()
	else:
		return validator.model.validateCandidate(candidate, strictness) and validator.process.performValidations()





