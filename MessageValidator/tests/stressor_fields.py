#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

ASSERT_ERROR_MSG = "Error applying %s to %s: expected %s, found %s"

def compareResults (expected, candidate):

	if isinstance (expected, type):
		if not isinstance(candidate, expected):
			return False
	else:
		if candidate != expected:
			return False

	return True

def runTest (function, candidates=None, expected=True):

	print "Testing %s for %s : starting" % (function.__name__, expected)

	for candidate in candidates:
		result = function(candidate)

		# expected is a non nested list/tuple or a single value
		# single values are compared directly or by type if describing a type

		if isinstance(expected, (list, tuple)):
			for i in range (0, len(expected)):
				assert compareResults (expected[i], result[i]) == True, ASSERT_ERROR_MSG % (function.__name__, candidate, expected[i], result[i])
		else:
			assert compareResults (expected, result) == True, ASSERT_ERROR_MSG % (function.__name__, candidate, expected, result)

	print "Testing %s for %s: completed" % (function.__name__, expected)






