#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import validate_message

__author__ = 'Antonio Vaccarino'
__docformat__ = 'restructuredtext en'


def buildDictFromTemplate (model, breakpath=None):

	clone = {}

	#TODO: implement
	for key in model:

		if isinstance(model[key], list):
			clone[key] = model[key][-1]

		elif isinstance (model[key], type):

			clone[key] = model[key]()

		elif isinstance(model[key], dict):
			clone[key] = buildDictFromTemplate(model[key])

	return clone

def createInvalidClones (reference, model):


	basictypeslist = int, unicode, list, dict

	clones = []
	clones.append (None)

	for key in model:

		baseclone = copy.deepcopy(reference)

		if not (isinstance(model[key], dict)):

			voidclone = copy.deepcopy(baseclone)
			voidclone[key] = None
			clones.append(voidclone)

			if isinstance (model[key], list):
				garbagedata = u'INTENTIONALLYNONVALIDVALUE'
				baseclone[key] = garbagedata
			elif isinstance (model[key], type):
				for ct in basictypeslist:
					if ct != model[key]:
						baseclone[key] = ct()

			clones.append(baseclone)


		else:

			subclones = createInvalidClones(baseclone[key], model[key])
			for sub in subclones:
				appliedsub = copy.deepcopy(baseclone)
				appliedsub[key] = sub
				clones.append(appliedsub)

			#get sub-changes and merge them

	return clones


def extractDictPaths (model):

	dictpaths = []

	for key in model:

		if not isinstance(model[key], dict):
			dictpaths.append([key,])
		else:
			subpaths = extractDictPaths(model[key])
			for sub in subpaths:
				dictpaths.append([key,]+sub)

	return dictpaths

def getDictValueFromPath (source, pathlisting):

	position = source
	for i in range (0, len(pathlisting)):
		position = position[pathlisting[i]]

	return position







def stressDictModel (model):
	"""
	Takes one reference dictionary and creates a list with: a compliant reference dictionary and a sequence of "bad" dictionaries created by modifying the original dictionary one field at a time

	:param model:
	:return:
	"""


	baddicts = []
	gooddicts = []

	errors = 0
	totals = 0

	totals += 1
	#leaving as a list in case we want to add support for several possible correct instances
	gooddicts.append(buildDictFromTemplate(model))
	if not validate_message.validateDictToTemplate(gooddicts[0], model):
		print "ERROR in good dict validation"
		print "Dict dump: "+str(gooddicts[0])
		print "Modl dump: "+str(model)
		errors += 1


	baddicts = createInvalidClones(gooddicts[0], model)
	for clone in baddicts:
		totals += 1
		if validate_message.validateDictToTemplate(clone, model):
			print "ERROR in bad dict validation"
			print "Dict dump: "+str(clone)
			print "Model dmp: "+str(model)
			errors += 1

	print "Result: %d/%d errors/tests" % (errors, totals)

