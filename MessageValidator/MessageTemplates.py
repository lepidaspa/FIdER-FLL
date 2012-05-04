#!/usr/bin/env python
# -*- coding: utf-8 -*-
from MarconiLabsTools.ArDiVa import validateFieldIteratively, validateFieldAsListOf
from validate_geojson import validateGeoJsonObject


__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

from validate_fields import *

# This file contains ArDiVa-based models and processes for the message validator

model_response_capabilities = {
	"token": unicode,
	"message_type": (u'response',),
	"message_format": (u'capabilities',),
	"base_url": unicode,
	"area": list,
	"time": list,
	"operations": {
		"write": (u"full", u"sync", u"none"),
		"read": (u"full", u"diff", u"none"),
		"query": {
			"inventory": (u"full", u"simple", u"none"),
			"geographic": (u"full", u"BB", u"none"),
			"time": (u"full", u"none"),
			"bi": (u"full", u"simple", u"none")
		},
		"signs": bool,
		"metadata": list
	}
}

process_response_capabilities = [
	(("area",),((validateFieldAsBoundingBox,True, None, None),)),
	(("time",),((validateFieldAsTimeSpan, True, None, None),)),
	(("base_url",), ((validateFieldAsActiveUrl, True, None, None),)),
	(("metadata"), ((validateFieldAsMetadataListing, True, None, None),))
]

model_response_welcome = {
	"token": unicode,
	"message_type": (u'response',),
	"message_format": (u'welcome',),
	"latest_model_version": unicode,
}

# no process_response_welcome

model_field_anomaly = {
	"id": unicode,
	"anomaly": unicode,
	"BB": list
}

process_field_anomaly = (
	(("BB",),((validateFieldAsBoundingBox,True, None, None),)),
)

model_response_read = {
	"token": unicode,
	"message_type": (u'response',),
	"message_format": (u'read',),
	"operation": (u'full', u'diff', u'none'),
	"data": {
		"upsert": dict,
		"delete": list
	}
}

#TODO: verify the specific subset of geojson objects that we need to use for this

#removed temporarily since now we don't have a list but a dict of lists
#	((["data", "upsert"],),((validateFieldIteratively,True, validateGeoJsonObject, None),)),
process_response_read = (
	((["data", "delete"],),((validateFieldAsListOf,True,(str, unicode),None),))
)


model_request_write = {
	"token": unicode,
	"message_type": [u'request',],
	"message_format": [u'write',],
	"data": {
		"upsert": dict,
		"delete": list
	}
}

# NOTE: same as process_response_read, but cloned in case the two branch out in the future
#TODO: verify the specific subset of geojson objects that we need to use for this

#removed temporarily since now we don't have a list but a dict of lists
#	((["data", "upsert"],),((validateFieldIteratively,True, validateGeoJsonObject, None),)),
process_request_write = (
	((["data", "delete"],),((validateFieldAsListOf,True,(str, unicode),None),))
)

#TODO: verify is DICT is the correct type for QUERY/INVENTORY
model_request_query = {
	"token": unicode,
	"message_type": [u'request',],
	"message_format": [u'query',],
	"query" : {
		"BB": list,
		"inventory": dict,
		"time": unicode,
		"signed": bool
	},
}

process_request_query = (
	((["query", "BB"],),((validateFieldAsBoundingBox,True, None, None),)),
	((["query", "time"],),((validateFieldAsIsoDateTime,True, None, None),)),
)



model_response_write = {
	"token": unicode,
	"message_type": [u'response',],
	"message_format": [u'write',],
	"acknowledge": {
		"upsert": list,
		"delete": list
	},
	"anomalies": list
}

#NOTE: unlike response_read and request_write, we are always passing geo objects IDs in this one
process_response_write = (
	((["acknowledge", "upsert"],),((validateFieldAsListOf,True,(str, unicode),None),)),
	((["acknowledge", "delete"],),((validateFieldAsListOf,True,(str, unicode),None),)),
	(("anomalies",),((validateFieldAsListOf,True,(str, unicode),None),)),
)



model_error_anomaly = {
	"token": unicode,
	"message_type": [u'error',],
	"message_format": [u'anomaly',],
	"anomalies": list
}

process_error_anomaly = {
	(("anomalies",),((validateFieldIteratively,True,validateFieldAsAnomaly,None),)),
}



model_error_error = {
	"token": unicode,
	"message_type": [u'error',],
	"message_format": [u'error',],
	"error_message": unicode,
	"error_code": unicode
}




model_request_api = {
	"token": unicode,
	"message_type": [u'request',],
	"message_format": [u'query',],
	"query" : {
		"BB": list,
		"time": unicode,
		"sign": unicode
	},
	"key": unicode,
}

process_request_api = (
	((["query", "BB"],),((validateFieldAsBoundingBox,True, None, None),)),
	((["query", "time"],),((validateFieldAsIsoDateTime,True, None, None),)),
)