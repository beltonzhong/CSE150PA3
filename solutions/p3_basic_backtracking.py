# -*- coding: utf-8 -*-


def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    For P3, *you do not need to modify this method.*
    """
    return next((variable for variable in csp.variables if not variable.is_assigned()))


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    For P3, *you do not need to modify this method.*
    """
    return [value for value in variable.domain]


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P3, *you do not need to modify this method.*
    """
    return True


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P3, *you do not need to modify this method.*
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


