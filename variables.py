import evaluate_expressions
import ast
import copy
users = [['admin','admin']]
variables = []
permissions = []
def addUser(user, password):
	users.append([user, password])

def addVariable(variable, data):
	if evaluate_expressions.isList(data):
		if type(data) is list:
			variables.append([variable, data])
		else:
			variables.append([variable,evaluate_expressions.asList(data)])
	else:
		variables.append([variable, data])
def addPermission(user,data, permission):
	permissions.append([user, data, permission])
def addAllPermission(user,anotherUser, permission):
	for existingUser, existingData, existingPermission in permissions:
		if existingUser == user:
			permissions.append("hi")
def addLocalVariable(variable, data):
	if evaluate_expressions.isList(data):
		variables.append([variable, evaluate_expressions.asList(data), 'local'])
	else:
		variables.append([variable, data, 'local'])
def getUser(user):
	for existingUser in users:
		if existingUser[0] == user:
			return existingUser
	return []
def getVariable(variable):
	if '.' in variable:
		varName = variable.split('.')[0]
		varField = variable.split('.')[1]
		for existingVariable in variables:
			if existingVariable[0] == varName:
				data = existingVariable[1].replace('=',':')
				newData = dict(e.split(":") for e in data.translate(None, "{}")\
					.split(","))
				newData={k.translate(None, ' '): v for k, v in newData.iteritems()}
				print newData
				if evaluate_expressions.isVariable(newData[varField]):
					return getVariable(newData[varField])
				else:
					return newData[varField]
	for existingVariable in variables:
		if existingVariable[0] == variable:
			return existingVariable[1]
	return []
def editVariable(variable, data):
	for existingVariable in variables:
		if existingVariable[0] == variable:
			existingVariable[1] = data

def check_admin(password):
	for user in users:
		if user[1] == password:
			return True
	return False
def userExists(user):
	for existingUser in users:
		if existingUser[0] == user:
			return True
	return False
def passwordCorrect(user, password):
	for existingUser, existingPassword in users:
		if existingUser == user and existingPassword == password:
			return True
	return False
def variableExists(variable):
	for existingVariable in variables:
		if variable == existingVariable[0]:
			return True
	return False
def userPermissionsOnVariable(user, variable):
	for existingUser, existingVariable, permission in permissions:
		if existingUser == user and existingVariable == variable:
			return permission
	return []
