#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'



template_response_capabilities = {
	"token": str,
	"message_type": ['response',],
	"message_format": ['capabilities',],
	"base_url": str,
	"area": list,
	"time": list,
	"operations": {
		"write": ["full", "sync", "none"],
		"read": ["full", "diff", "none"],
		"query": {
			"inventory": ["full", "simple", "none"],
			"geographic": ["full", "BB", "none"],
			"time": ["full", "none"],
			"bi": ["full", "simple", "none"]
		},
		"signs": bool,
		"metadata": list
	}
}

template_response_read = {
	"token": str,
	"message_type": ['response',],
	"message_format": ['read',],
	"operation": ['full', 'diff', 'none'],
	"data": {
		"upsert": list,
		"delete": list
	}
}

template_request_write = {
	"token": str,
	"message_type": ['request',],
	"message_format": ['write,'],
	"data": {
		"upsert": list,
		"delete": list
	}
}

template_response_welcome = {
	"token": str,
	"message_type": ['response',],
	"message_format": ['welcome,'],
	"latest_model_version": str,
}

template_request_query = {
	"token": str,
	"message_type": ['request',],
	"message_format": ['query,'],
	"query" : {
		"BB": list,
		"inventory": dict,
		"time": str,
		"signed": bool
	},
}

template_response_write = {
	"token": str,
	"message_type": ['response',],
	"message_format": ['write',],
	"acknowledge": {
		"upsert": list,
		"delete": list
	},
	"anomalies": list
}

template_error_anomaly = {
	"token": str,
	"message_type": ['error',],
	"message_format": ['anomaly',],
	"anomalies": list
}

template_anomaly = {
	"id": str,
	"anomaly": str,
	"BB": list
}

template_error_error = {
	"token": str,
	"message_type": ['error',],
	"message_format": ['error',],
	"error_message": str,
	"error_code": str
}

template_request_api = {
	"token": str,
	"message_type": ['request',],
	"message_format": ['query,'],
	"query" : {
		"BB": list,
		"time": str,
		"sign": str
	},
	"key": str,
}