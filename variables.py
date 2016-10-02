import evaluate_expressions

users = [['admin','admin']]
variables = []
permissions = []

def addUser(user, password):
	users.append([user, password])

def addVariable(variable, data):
	if evaluate_expressions.isList(data):
		variables.append([variable,evaluate_expressions.asList(data)])
	else:
		variables.append([variable, data])
def addPermission(user,data, permission):
	permissions.append([user, data, permission])
def getUser(user):
	for existingUser in users:
		if existingUser[0] == user:
			return existingUser
	return []
def getVariable(variable):
	for existingVariable in variables:
		if existingVariable[0] == variable:
			return existingVariable
	return []
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
