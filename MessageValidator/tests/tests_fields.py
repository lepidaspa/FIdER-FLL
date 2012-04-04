#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'


from stressor_fields import *
from validate_fields import *


print "Testing date/time functions"

dates_compliant = (u"2012-04-04T06:04Z", u"20120404T06Z", u"20120404T06-0200",  u"20120404T06+02:00", u"2012-04-04T06:04+78:93")
dates_noncomp = ([u"2012-04-04T06:04Z"],  u"2012:04:04T06:04Z", u"201204040604Z", u"2012:04:04T06Z")

runTest(validateFieldAsIsoDateTimeNotation, dates_compliant, True)
runTest(validateFieldAsIsoDateTimeNotation, dates_noncomp, False)

dates_compliant = (u"2012-04-04T06:04Z", u"20120404T06Z", u"20120404T06-0200",  u"20120404T06+02:00")
dates_noncomp = ([u"2012-04-04T06:04Z"],  u"2012:04:04T06:04Z", u"201204040604Z", u"2012:04:04T06Z", u"2012-29-86T76:34Z", u"2012-04-04T06:04+78:93")

runTest(validateFieldAsIsoDateTime, dates_compliant, True)
runTest(validateFieldAsIsoDateTime, dates_noncomp, False)


print "Testing URL validation function"

#testing validateFieldAsActiveUrl
url_compliant = ("http://www.cnn.com", "https://oriente.labs.it")
url_noncomp = ("www.cnn.com", "http://www.rg44v4vwfwv.com")
testfunction = validateFieldAsActiveUrl

runTest (validateFieldAsActiveUrl, url_compliant, True)
runTest (validateFieldAsActiveUrl, url_noncomp, False)

print "Testing TimeSpan validation function"

#testing validateFieldAsTimeSpan
timespan_compliant = ([u"2012-04-04T06:04Z", u"20120404T06+02:00"],)
timespan_noncomp = ([], u"2012-04-04T06:04Z", [u"2012-04-04T06:04Z",], [u"2012-04-04T06:04+78:93", u"2012-04-04T06:04+78:93"] )

runTest (validateFieldAsTimeSpan, timespan_compliant, True)
runTest (validateFieldAsTimeSpan, timespan_noncomp, False)

print "Testing BoundingBox validation function"

#testing ValidateFieldAsBoundingBox against constants for 3 axes in model and 2 axes in compare

bbox_compliant = ( [0.,0.,0., 12.,12.,12.] , [-2.,3.,-15.,3.,5.,0.] )
bbox_noncomp = ( [], [0,0,0, 12,12,12], [0.,0.,0.,12.], [3.,0.,0., -2.,5.,-15.], [[0.,0.,0.],[12.,12.,12.]] )

runTest (validateFieldAsBoundingBox, bbox_compliant, True)
runTest (validateFieldAsBoundingBox, bbox_noncomp, False)

print "Testing Metadata validation function"

#TODO: create test


