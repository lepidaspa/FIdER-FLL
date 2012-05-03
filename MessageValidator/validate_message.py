#!/usr/bin/env python
# -*- coding: utf-8 -*-
from MessageValidator import validateJsonToTemplate

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

import MessageTemplates


def validateMessageResponseCapabilities (jsonmessage):
	"""
	Validates a json message as a proper capabilities response message for the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	return validateJsonToTemplate(jsonmessage, MessageTemplates.model_response_capabilities, MessageTemplates.process_response_capabilities)


def validateMessageResponseWelcome (jsonmessage):
	"""
	Validates a json message as a proper welcome response message from the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error message/json dict)
	"""

	return validateJsonToTemplate(jsonmessage, MessageTemplates.model_response_welcome)


def validateMessageResponseRead (jsonmessage):
	"""
	Validates a json message as a proper read response message from the federator and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	return validateJsonToTemplate(jsonmessage, MessageTemplates.model_response_read, MessageTemplates.process_response_read)

def validateMessageRequestWrite (jsonmessage):
	"""
	Validates a json message as a proper write request message from the proxy and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	return validateJsonToTemplate(jsonmessage, MessageTemplates.model_request_write, MessageTemplates.process_request_write)


def validateMessageRequestQuery (jsonmessage):
	"""
	Validates a json message as a proper query request message from the main server and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	return validateJsonToTemplate(jsonmessage, MessageTemplates.model_request_query, MessageTemplates.process_request_query)

def validateMessageResponseWrite (jsonmessage):
	"""
	Validates a json message as a proper write response message from the main server and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	return validateJsonToTemplate(jsonmessage, MessageTemplates.model_response_write, MessageTemplates.process_response_write)

def validateMessageErrorAnomaly (jsonmessage):
	"""
	Validates a json message as a proper anomaly listing message from the main server and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	return validateJsonToTemplate(jsonmessage, MessageTemplates.model_error_anomaly, MessageTemplates.process_error_anomaly)

def validateMessageErrorError (jsonmessage):
	"""
	Validates a json message as a proper error reporting message from the main server and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	return validateJsonToTemplate (jsonmessage, MessageTemplates.model_error_error)

def validateMessageRequestApi (jsonmessage):
	"""
	Validates a json message as a proper api request message and, if validated, returns the corresponding Python dict
	:param jsonmessage: unicode, stringified json data
	:return: tuple (bool, error list/json dict)
	"""

	return validateJsonToTemplate (jsonmessage, MessageTemplates.model_request_api, MessageTemplates.process_request_api)




