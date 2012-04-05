#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tests import templates_geojson

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

import validate_geojson
import stressor_fields


total = 0
failed = 0

for objectname in dir(templates_geojson):
	if objectname not in ('__author__', '__builtins__', '__doc__', '__docformat__', '__file__', '__name__', '__package__'):
		current = getattr(templates_geojson, objectname)

		print "Stress testing "+objectname


		success = stressor_fields.runTest(validate_geojson.validateGeoJsonObject, [current,], (True, object))

		if not success:
			failed += 1
		total+= 1

print "Result: %d/%d errors/tests" % (failed, total)

#LINEARRING TESTING

[[100.0, 0.0], [101.0, 0.0], []]