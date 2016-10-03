import re
import json

import sys
import evaluate_expressions

#Creating regular expressions for all possible inputs
string_constant = "[A-Za-z0-9_,:\.?!-]+"
identifier = "[A-ZZa-z][AA-ZZa-z0-9_]*"
string_variable = "\"\s*" + string_constant + "\s*\"\s*"
expression = "("+string_variable+"|"+string_constant+")"
field_variable="{(\s*"+identifier+"\s*=\s*"+expression+"\s*\D?)+}"

tgt = "(all|"+identifier+")"
right = "(read|write|append|delegate)"

as_principle_do = re.compile("\s*as\s+principle\s+" + identifier + "\s+password\s+" + \
				identifier + "\s+do\s*")
create_principle = re.compile("\s*create\s+principle\s+" + identifier + "\s+" + string_variable)
change_password = re.compile("\s*change\s+password\s+" + identifier + "\s+" + string_variable)
#field_variable = re.compile("\s*{\s*"+identifier+"\s*=\s*"+expression+"\s*}\s*")
set_x = re.compile("\s*set\s+" + identifier + "\s*=\s*" + "("+expression+"|"+field_variable+\
			"|\[\]" +")")
append_to = re.compile("\s*append\s+to\s+" + identifier + "\s+with\s+" + "("+expression+"|"\
			+field_variable+")")
local_variable = re.compile("\s*local\s+" + identifier + "\s*\s*" + expression)
for_each = re.compile("\s*foreach\s+"+identifier+"\s+in\s+"+identifier + "\s+replacewith\s+"\
			+expression)
set_delegation = re.compile("\s*set\s+delegation\s+" + tgt +"\s+"+ identifier+"\s*"+right+\
				"\s+->\s+"+identifier+"\s*")
delete_delegation = re.compile("\s*delete\s+delegation\s+" + tgt +"\s+"+ identifier+"\s"+right+\
				"\s+->\s+"+identifier+"\s*")
default_delegator = re.compile("\s*default\s+delegator\s+=\s+" + identifier +"\s*")

def parse_expression(string):
	if as_principle_do.match(string):
		evaluate_expressions.asPrincipleDo(string)
	elif create_principle.match(string):
		evaluate_expressions.createPrinciple(string)
	elif change_password.match(string):
		evaluate_expressions.changePassword(string)
	elif set_x.match(string):
		evaluate_expressions.setX(string)
	elif append_to.match(string):
		evaluate_expressions.appendTo(string)
	elif local_variable.match(string):
		evaluate_expressions.localVariable(string)
	elif for_each.match(string):
		evaluate_expressions.forEach(string)
	elif set_delegation.match(string):
		evaluate_expressions.setDelegation(string)
	elif delete_delegation.match(string):
		evaluate_expressions.deleteDelegation(string)
	elif default_delegator.match(string):
		evaluate_expressions.default_delegator(string)
	else:
		print "PARSE ERROR"
