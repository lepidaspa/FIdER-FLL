#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

import stressor_template

import validation_templates

for objectname in dir(validation_templates):
	if objectname not in ('__author__', '__builtins__', '__doc__', '__docformat__', '__file__', '__name__', '__package__'):
		current = getattr(validation_templates, objectname)

		print "Stress testing "+objectname

		stressor_template.stressDictModel(current)