#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'

class ValidationError (Exception):

	def __init__ (self, candidate=None, errormsg="Undefined validation exception"):
		super(ValidationError, self).__init__()
		self.message = errormsg
		self.candidate = candidate

	def __str__ (self):
		return self.message, str(self.candidate)

	def getRawData (self):
		return self.candidate

	def getError (self):
		return self.message


