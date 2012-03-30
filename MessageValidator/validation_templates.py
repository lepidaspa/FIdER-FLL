__author__ = 'Antonio Vaccarino'


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


