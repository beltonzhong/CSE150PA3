# -*- coding: utf-8 -*-

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """
    if is_complete(csp):
    	return None
    minDomainSize = 9999999999
    variables = []
    for var in csp.variables:
    	domSize = len(var.domain)
	if domSize == 1:
	    continue
	if domSize == minDomainSize:
	    variables.append(var)
	elif domSize < minDomainSize:
	    variables = [var]
	    minDomainSize = domSize 
    if len(variables) == 1:
    	return variables[0]
    degreeHeur = -1
    selectedVar = None
    for var in variables:
    	deg = len(csp.constraints[var])
	if deg > degreeHeur:
	   selectedVar = var
	   degreeHeur = deg
    return selectedVar

def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """

    # TODO implement this
    valueTuples = []
    for val in variable.domain:
    	count = 0
	for neighbor in neighbors(csp, variable):
	    for otherVal in neighbor.domain:
	        eliminated = False
	        for constraint in csp.constraints[variable, neighbor]:
	            if not constraint.is_satisfied(val, otherVal):
		        eliminated = True
		if eliminated:
		    count = count + 1
	valueTuples.append((val, count))
    orderedTuples = sorted(valueTuples, key = lambda value: value[1])
    returnList = []
    for tuple in orderedTuples:
        returnList.append(tuple[0])
    return returnList

def neighbors(csp, variable):
    neighList = []
    for arc in csp.constraints.arcs():
        if arc[0] == variable:
	    if not arc[1] in neighList:
	        neighList.append(arc[1])
	elif arc[1] == variable:
	    if not arc[0] in neighList:
	        neighList.append(arc[0])
    return neighList

def is_complete(csp):
    for var in csp.variables:
    	if not var.is_assigned():
	    return False
    return True
