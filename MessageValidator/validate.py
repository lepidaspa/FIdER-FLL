import json


from errors_msg import *
from validate_fields import *
import validation_templates

__author__ = 'Antonio Vaccarino'

def validateDictToTemplate (candidate, template):

	#This function checks (recursively) that two dicts have exactly the same structure and that the candidate respects a series of constraints defined by the template as either a specific type for the value OR as a specific range of possible values
	#The function returns a simple True or False value, and stops at the first error encountered

	#STEP 1: check if we have the same number of key/value couples at the current level
	if not (isinstance(candidate, dict) and candidate.keys() == template.keys()):
		return False

	#STEP 2: validate the values of each key/value couple according to granularity in the template
	for key in template:

		constraint = template[key]

		if not isinstance (constraint, list):
			#2.1: validate against values range
			if candidate[key] in constraint:
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
	#This function checks (recursively) that two dicts have the same structure and that the candidate respects a series of constraints defined by the template as either a specific type for the value OR as a specific range of possible values.
	#The function returns a tuple with True/False and a list of the errors encountered in the comparison. Based on the validateDictToTemplate function

	validation_errors = []

	#STEP 1: check if we have the same number of key/value couples at the current level
	try:
		if candidate.keys() != template.keys():
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
			next_level_validation = validateDictToTemplateAndLog (candidate[key], template[key], currentpath)
			if next_level_validation is not True:
				validation_errors = validation_errors + next_level_validation[1]

	if len(validation_errors) > 0:
		return False, validation_errors
	else:
		return True

def validateJsonToTemplate (jsonmessage, template):

	#This function checks that a json message has the same structure as a reference dictionary and that the json message respects a series of constraints defined by the template as either a specific type for the value OR as a specific range of possible values.
	#This function returns a tuple with two values: the True/False result and the parsed json or the errors list

	# Parsing the json message into a dict
	try:
		candidate = json.loads(jsonmessage)
	except Exception as current_error:
		return False, ("Not a JSON object? %s " % current_error.message)

	dictionary_validation = validateDictToTemplateAndLog(candidate, template)
	if dictionary_validation is not True:
		return False, dictionary_validation[1]
	else:
		return True, candidate


def validateMessageDiscovery (jsonmessage):

	# General comparison of the dictionary structure,
	# we don't continue checking if this does not work because fields may be missing
	templatevalidation = validateJsonToTemplate(jsonmessage, validation_templates.template_response_capabilities)

	if templatevalidation[0] is not True:
		return templatevalidation
	else:
		messagedata = templatevalidation[1]

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
		return True
