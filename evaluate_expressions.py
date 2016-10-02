import re
import sys
import json
import variables
import server

listFormat = re.compile("\["+"\S*"+"\]")
#helper functions
def cleanString(string):
	return ''.join(char for char in string if char.isalnum())
def returnStatus(status):
	return "{\"status\": " + "\""+status+"\"}"

def isStringOrRecord(string):
	return '"' in string or (string.startswith('{') and string.endswith('}'))
def isList(string):
	return listFormat.match(string)
def addToList(listToAppend, obj):
	if type(obj) is list:
		listToAppend.extend(obj)
	else:
		listToAppend.append(obj)

def asList(string):
	return json.loads(string)


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
			variables.addVariable(varName, variables.getVariable(value)[1])
		variables.addPermission(server.curUser, varName, ["read", "write", \
							"append", "delegate"])
	else:
		if isStringOrRecord(value):
			variables.getVariable(varName)[1] = value
		else:
			variables.getVariable(varName)[1] = asList(value)
	server.statusCodes.append(returnStatus("SET"))
	print variables.variables
	print type(variables.variables[0][1]) is list
	print variables.userPermissionsOnVariable(server.curUser, varName)


def appendTo(string):
	var = re.findall(r'append\s+to\s+(.*?)\s+with',string)[0]
	afterWith = string.find('with') +4
	expr = string[afterWith:].strip()
	print expr
	print isStringOrRecord(expr)
	permissionsForVar = variables.userPermissionsOnVariable(server.curUser, var)
	if not variables.getVariable(var):
		server.statusCodes.append(returnStatus("FAILED"))
	elif not "write" in permissionsForVar and "append" not in permissionsForVar and \
	server.curUser != 'admin':
		server.statusCodes.append(returnStatus("DENIED"))
	elif not type(variables.getVariable(var)[1]) is list:
		server.statusCodes.append(returnStatus("FAILED"))
	elif isStringOrRecord(expr):
		variables.getVariable(var)[1].append(expr)
		server.statusCodes.append(returnStatus("APPEND"))
	elif isList(expr):
		variables.getVariable(var)[1].extend(asList(expr))
		server.statusCodes.append(returnStatus("APPEND"))
	else:
		addToList(variables.getVariable(var)[1], variables.getVariable(expr)[1])
		server.statusCodes.append(returnStatus("APPEND"))

def localVariable(string):
	print "localVariable"

def forEach(string):
	print "forEach"

def setDelegation(string):
	print "setDelegation"

def deleteDelegation(string):
	print "deleteDelegation"

def defaultDelegator(string):
	print "defaultDelegator"
	
