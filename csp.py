import copy


class GraphColorCSP:
    def __init__(self, variables, colors, adjacency):
        self.variables = variables
        self.colors = colors
        self.adjacency = adjacency

    def diff_satisfied(self, var1, color1, var2, color2):  # checks that the assigned values satisfies the constraint
        if var2 not in self.adjacency[var1]:  # if they are not adjacent, then they can take any colors
            return True
        else:
            return color1 != color2

    def is_goal(self, assignment):  # Returns true if assignment is complete and consistent. Otherwise, false.
        # complete = all(item in assignment for item in self.variables)
        complete = assignment and len(assignment) == len(self.variables)
        if not complete:
            return False
        else:
            for variable in assignment:
                for adjacency in self.adjacency[variable]:
                    if assignment[adjacency] is not None and not self.diff_satisfied(variable, assignment[variable],
                                                                                     adjacency, assignment[
                                                                                         adjacency]):  # checks if the two adjacent variables have the same color
                        return False
            return True

    def check_partial_assignment(self, assignment):  # check the consistency of partial state
        for variable in assignment:
            for adjacency in self.adjacency[variable]:
                if adjacency in assignment:
                    if assignment[adjacency] is not None and not self.diff_satisfied(variable, assignment[variable],
                                                                                     adjacency, assignment[
                                                                                         adjacency]):  # checks if the two variables have the same color
                        return False
        return True


def ac3(graphcolorcsp, arcs_queue=None, current_domains=None, assignment={}):
    if arcs_queue is None:
        arcs_queue = create_arcs_queue(graphcolorcsp, graphcolorcsp.variables)
    if current_domains is None:
        current_domains = {}
        for variable in graphcolorcsp.variables:
            current_domains[variable] = graphcolorcsp.colors
    updated_domains = copy.deepcopy(current_domains)
    set(arcs_queue)
    while arcs_queue:
        xi, xj = arcs_queue.pop()
        if revise(graphcolorcsp, updated_domains, assignment, xi, xj):
            if len(updated_domains[xi]) == 0:
                return False, updated_domains
            else:
                for xk in graphcolorcsp.adjacency[xi]:
                    if xk != xj and xk not in assignment:
                        arcs_queue.add((xk, xi))
        # print(updated_domains)
    return True, updated_domains


def revise(graphcolorcsp, updated_domains, assignment, xi, xj):
    revised = False
    for color in updated_domains[xi]:
        if color in updated_domains[xj] and len(updated_domains[xj]) == 1:  # if the neighbour have the same color and has no other color choice
            new_domain = set(updated_domains[xi])
            new_domain.remove(color)
            updated_domains[xi] = new_domain
            # print(updated_domains)
            revised = True
    return revised


def create_arcs_queue(graphcolorcsp, variables):
    acrs_queue = set()
    for variable in variables:
        for adjacency in graphcolorcsp.adjacency[variable]:
            acrs_queue.add((adjacency, variable))
    return acrs_queue


def backtracking(graphcolorcsp):
    current_domains = {}
    for variable in graphcolorcsp.variables:
        current_domains[variable] = list(graphcolorcsp.colors)
    return backtracking_helper(graphcolorcsp, {}, current_domains)


def backtracking_helper(graphcolorcsp, assignment={}, current_domains=None):
    if graphcolorcsp.is_goal(assignment):
        return assignment
    MRV = find_MRV(graphcolorcsp, current_domains,
                   assignment if assignment else {})  # find the variable with Minimum Remaining Values
    for color in current_domains[MRV]:  # iterate on the colors that are in the variable domain
        assignment[MRV] = color
        current_domains[MRV] = {color}
        if graphcolorcsp.check_partial_assignment(assignment):  # checks if color assignment is consistent
            inferences, updated_domains = ac3(graphcolorcsp, create_arcs_queue(graphcolorcsp, [MRV]), copy.deepcopy(current_domains),assignment)  # apply ac3 constraints after the assignment
            if inferences is not False:
                # current_domains = copy.deepcopy(updated_domains)  # update the current domains
                result = backtracking_helper(graphcolorcsp, assignment, updated_domains)  # recall the function for the other assignments
                if result is not None:
                    return result
            del assignment[MRV]
    return None



def find_MRV(graphcolorcsp, current_domains, assignment={}):
    unassigned_var = [variable for variable in graphcolorcsp.variables if variable not in assignment]
    MRV = unassigned_var[0]
    for variable in unassigned_var:
        if len(current_domains[variable]) < len(current_domains[MRV]):  # checks if there is better unassigned_var
            MRV = variable
        elif len(current_domains[variable]) == len(current_domains[MRV]):
            if len(graphcolorcsp.adjacency[variable]) > len(
                    graphcolorcsp.adjacency[MRV]):  # if unassigned_var equal check Degree value [as tie breaker]
                MRV = variable
    return MRV


def LCV_order(graphcolorcsp, current_domains, MRV, assignment): # implementation is not correct
    domains_count = []
    for color in current_domains[MRV]:
        count = 0
        current_domains[MRV] = {color}
        updated_domains = ac3(graphcolorcsp, create_arcs_queue(graphcolorcsp, [MRV]), copy.deepcopy(current_domains), assignment)[1]
        unassigned_var = [variable for variable in updated_domains if variable not in assignment]
        for variable in unassigned_var:
            # print(updated_domains[variable])
            count += len(updated_domains[variable])
        domains_count.append([count, color])
    domains_count.sort()
    # print(domains_count)
    return list(list(zip(*domains_count))[1])
