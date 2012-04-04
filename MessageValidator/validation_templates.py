#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'



template_response_capabilities = {
	"token": unicode,
	"message_type": [u'response',],
	"message_format": [u'capabilities',],
	"base_url": unicode,
	"area": list,
	"time": list,
	"operations": {
		"write": [u"full", u"sync", u"none"],
		"read": [u"full", u"diff", u"none"],
		"query": {
			"inventory": [u"full", u"simple", u"none"],
			"geographic": [u"full", u"BB", u"none"],
			"time": [u"full", u"none"],
			"bi": [u"full", u"simple", u"none"]
		},
		"signs": bool,
		"metadata": list
	}
}

template_response_read = {
	"token": unicode,
	"message_type": [u'response',],
	"message_format": [u'read',],
	"operation": [u'full', u'diff', u'none'],
	"data": {
		"upsert": list,
		"delete": list
	}
}

template_request_write = {
	"token": unicode,
	"message_type": [u'request',],
	"message_format": [u'write,'],
	"data": {
		"upsert": list,
		"delete": list
	}
}

template_response_welcome = {
	"token": unicode,
	"message_type": [u'response',],
	"message_format": [u'welcome,'],
	"latest_model_version": unicode,
}

template_request_query = {
	"token": unicode,
	"message_type": [u'request',],
	"message_format": [u'query,'],
	"query" : {
		"BB": list,
		"inventory": dict,
		"time": unicode,
		"signed": bool
	},
}

template_response_write = {
	"token": unicode,
	"message_type": [u'response',],
	"message_format": [u'write',],
	"acknowledge": {
		"upsert": list,
		"delete": list
	},
	"anomalies": list
}

template_error_anomaly = {
	"token": unicode,
	"message_type": [u'error',],
	"message_format": [u'anomaly',],
	"anomalies": list
}

template_anomaly = {
	"id": unicode,
	"anomaly": unicode,
	"BB": list
}

template_error_error = {
	"token": unicode,
	"message_type": [u'error',],
	"message_format": [u'error',],
	"error_message": unicode,
	"error_code": unicode
}

template_request_api = {
	"token": unicode,
	"message_type": [u'request',],
	"message_format": [u'query,'],
	"query" : {
		"BB": list,
		"time": unicode,
		"sign": unicode
	},
	"key": unicode,
}