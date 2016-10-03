import re
import sys
import json
import variables
import server
import copy
import ast

listFormat = re.compile("\["+"\S*"+"\]")
#helper functions
def cleanString(string):
	return ''.join(char for char in string if char.isalnum())
def returnStatus(status):
	return "{\"status\": " + "\""+status+"\"}"

def isStringOrRecord(string):
	return '"' in string or (string.startswith('{') and string.endswith('}'))
def isList(string):
	if type(string) is str:
		return listFormat.match(string)
	else:
		return type(string) is list

def isVariable(string):
	return not isList(string) and not(isStringOrRecord(string))
def addToList(listToAppend, obj):
	if type(obj) is list:
		listToAppend.extend(obj)
	else:
		listToAppend.append(obj)

def asList(string):
	return ast.literal_eval(string)
def getFieldValues(dictionary, key):
	dictionary = dictionary.replace('=', ':')
	newDict = dict(e.split(":") for e in dictionary.translate(None, "{}").split(","))
	newDict = {k.translate(None, ' '): v for k,v in newDict.iteritems()}
	if '"' in newDict[key]:	
		return newDict[key].strip()
	else:
		return variables.getVariable(newDict[key])
#actual functions
def asPrincipleDo(string):
	principle = re.findall(r'as principle\s*(.*?)\s*password', string)[0]
	password = re.findall(r'password\s*(.*?)\s*do', string)[0]
	if not variables.userExists(principle):
		server.statusCodes.append(returnStatus("FAILED"))
	if not variables.passwordCorrect(principle, password):
		server.statusCodes.append(returnStatus("DENIED"))
	else:
		server.curUser = cleanString(principle)
def createPrinciple(string):

	if server.curUser != 'admin':
		server.statusCodes.append(returnStatus("DENIED"))
	principle = re.findall(r'create principle\s+(.*?)\s+', string)[0]
	password = re.findall(r'"(.*?)"', string)[0]
	if variables.userExists(principle):
		server.statusCodes.append(returnStatus("FAILED"))
	else:
		variables.addUser(principle, password)
		server.statusCodes.append(returnStatus("CREATE_PRINCIPLE"))
	print variables.users


def changePassword(string):
	principle = re.findall(r'change password\s+(.*?)\s+', string)[0]
	password = re.findall(r'"(.*?)"', string)[0]
	if server.curUser != 'admin' and server.curUser != principle:
		server.statusCodes.append(returnStatus("DENIED"))
	if not variables.userExists(principle):
		server.statusCodes.append(returnStatus("FAILED"))
	else:
		variables.getUser(principle)[1] = password
		server.statusCodes.append(returnStatus("CHANGE_PASSWORD"))
	print variables.users

def setX(string):
	varName = re.findall(r'set\s+(.*?)\s+', string)[0]
	firstEquals = string.find('=')+1
	value = string[firstEquals:].strip()
	print value
	print value.startswith("{") and value.endswith("}")
	if not variables.variableExists(varName):
		if isStringOrRecord(value) or isList(value):
			variables.addVariable(varName, value)
		else:
			
			variables.addVariable(varName, copy.deepcopy(variables.getVariable(value)))
		variables.addPermission(server.curUser, varName, ["read", "write", \
							"append", "delegate"])
	else:
		if "write" not in variables.userPermissionsOnVariable(server.curUser, varName)\
		and server.curUser != 'admin':
			server.statusCodes.append(returnStatus("DENIED"))
		if isStringOrRecord(value):
			variables.editVariable(varName, value)
		elif isList(value):
			variables.editVariable(varName, asList(value))
		else:
			variables.editVariable(varName, variables.getVariable(value))
	server.statusCodes.append(returnStatus("SET"))
	print variables.variables
	print type(variables.variables[0][1]) is list
	print variables.userPermissionsOnVariable(server.curUser, varName)


def appendTo(string):
	var = re.findall(r'append\s+to\s+(.*?)\s+with',string)[0]
	afterWith = string.find('with') +4
	expr = string[afterWith:].strip()
	permissionsForVar = variables.userPermissionsOnVariable(server.curUser, var)
	if not variables.variableExists(var):
		print "variable not found"
		server.statusCodes.append(returnStatus("FAILED"))
	elif not "write" in permissionsForVar or "append" not in permissionsForVar and \
	server.curUser != 'admin':
		print "not permissioned"
		server.statusCodes.append(returnStatus("DENIED"))
	elif not type(variables.getVariable(var)) is list:
		print "is not list"
		server.statusCodes.append(returnStatus("FAILED"))
	elif isStringOrRecord(expr):
		print "is string or record"
		variables.getVariable(var).append(expr)
		server.statusCodes.append(returnStatus("APPEND"))
	elif isList(expr):
		print "is list"
		variables.getVariable(var).extend(asList(expr))
		server.statusCodes.append(returnStatus("APPEND"))
	else:
		print "add var to list"
		addToList(variables.getVariable(var), variables.getVariable(expr)[1])
		server.statusCodes.append(returnStatus("APPEND"))
	print variables.getVariable(var)

def localVariable(string):
	varName = re.findall(r'local\s+(.*?)\s+', string)[0]
	firstEquals = string.find('=')+1
	value = string[firstEquals:].strip()
	if variables.variableExists(varName):
		server.statusCodes.append(returnStatus("FAILED"))
	elif not variables.variableExists(varName):
		if isStringOrRecord(value) or isList(value):
			variables.addLocalVariable(varName, value)
		else:
			variables.addLocalVariable(varName, variables.getVariable(value))
		variables.addPermission(server.curUser, varName, ["read", "write", \
							"append", "delegate"])
	server.statusCodes.append(returnStatus("LOCAL"))
	print variables.variables
	print variables.userPermissionsOnVariable(server.curUser, varName)
	

def forEach(string):
	element = re.findall(r'foreach\s+(.*?)\s+in', string)[0]
	elements = re.findall(r'in\s+(.*?)\s+replacewith',string)[0]
	replaceWithIndex = string.find('replacewith')+11
	replaceWith = string[replaceWithIndex:].strip()
	if not variables.variableExists(elements) or not isList(variables.getVariable(elements))\
 		or variables.variableExists(element):
		server.statusCodes.append(returnStatus("FAILED"))
	elif "write" not in variables.userPermissionsOnVariable(server.curUser, elements) and \
	"read" not in variables.userPermissionsOnVariable(server.curUser, elements):
		server.statusCodes.append(returnStatus("DENIED"))		
	else:
		for index,data in enumerate(variables.getVariable(elements)):
			if isVariable(replaceWith):
				if element+'.' in replaceWith:
					variables.getVariable(elements)[index] = getFieldValues\
					(variables.getVariable(elements)[index], replaceWith.\
					split('.')[1])
				else:
					variables.getVariable(elements)[index] = \
					variables.getVariable(replaceWith)
			else:
				variables.getVariable(elements)[index] = replaceWith
		server.statusCodes.append(returnStatus("FOREACH"))
	print variables.getVariable(elements)
	

def setDelegation(string):
	splitString = string.split()
	if len(splitString) != 7:
		server.statusCodes.append(returnStatus("PARSE ERROR"))
	var = splitString[2]
	delegating = splitString[3]
	right = splitString[4]
	delegated = splitString[6]
	if not userExists(delegating) or not userExists(delegated) or (right != "write" or right != 		"read" or right != "append" or right != "delegate") or not variableExists(var):
		server.statusCodes.append(returnStatus("FAILED"))
	if "delegate" not in userPermissionsOnVariable(server.curUser) and server.curUser \
	!= 'admin':
		server.statusCodes.append(returnStatus("DENIED"))
	
def deleteDelegation(string):
	print "deleteDelegation"

def defaultDelegator(string):
	print "defaultDelegator"
	

