# -*- coding: utf-8 -*-

from collections import deque


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """

    if is_complete(csp):
        return True
    nextVar = select_unassigned_variable(csp)
    for value in order_domain_values(csp, nextVar):
        if is_consistent(csp, nextVar, value):
	    csp.variables.begin_transaction()
            nextVar.assign(value)
            inferences = inference(csp, nextVar)
            if inferences:
                # add inferences to assignment
                if backtrack(csp):
                    return True
		else:
		    csp.variables.rollback()
	    else:
	        csp.variables.rollback()
        # rollback?
        else:
            nextVar.domain.remove(value)
    return False

def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise.  Note that this method does not
    return any additional variable assignments (for simplicity)."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    # TODO implement this
    while queue_arcs:
        arc = queue_arcs.popleft()
	if revise(csp, arc[0], arc[1]):
	    if len(arc[0].domain) == 0:
	    	return False
	    for neighborArc in csp.constraints.arcs():
	    	if neighborArc[0] == arc[0] or neighborArc[1] == arc[0]:
	    	    queue_arcs.append(neighborArc)
    return True

def revise(csp, xi, xj):
    # You may additionally want to implement the 'revise' method.
    revised = False
    for value in xi.domain:
    	valueSat = False
        for otherVal in xj.domain:
	    constVar = True
	    for constraint in csp.constraints[xi, xj]:
	    	if not constraint.is_satisfied(value, otherVal):
		    constVar = False
	    if constVar:
	    	valueSat = True
	if not valueSat:
	    xi.domain.remove(value)
	    revised = True
    return revised

def is_complete(csp):
    for var in csp.variables:
        if not var.is_assigned():
            return False
    return True

def is_consistent(csp, variable, value):
    for constraint in csp.constraints[variable]:
        otherVar = constraint.var2
        if otherVar.is_assigned():
            if not constraint.is_satisfied(value, otherVar.value):
                return False
    return True

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

