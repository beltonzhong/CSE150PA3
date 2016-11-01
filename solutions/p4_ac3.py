# -*- coding: utf-8 -*-

from collections import deque


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

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
