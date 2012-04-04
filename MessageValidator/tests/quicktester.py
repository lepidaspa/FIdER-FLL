#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'




test_dump = {'token': u'', 'message_format': u'write', 'message_type': u'response', 'anomalies': [], 'acknowledge': {'upsert': [], 'delete': []}}
modl_dump = {'token': unicode, 'acknowledge': {'delete': list, 'upsert': list}, 'message_type': [u'response'], 'anomalies': list, 'message_format': [u'write']}

import sys
sys.path.insert(0,"../")
from validate import *

print test_dump.keys()
print modl_dump.keys()


print validateDictToTemplate(test_dump, modl_dump)