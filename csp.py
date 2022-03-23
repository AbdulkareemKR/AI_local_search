class GraphColorCSP:
    def __init__(self, variables, colors, adjacency):
        self.variables = variables
        self.colors = colors
        self.adjacency = adjacency

    def diff_satisfied(self, var1, color1, var2, color2):  # checks that the asssigned values satisifies the constraint
        if var2 not in self.adjacency[var1]:  # if they are not adjacent, then thay can take any calue
            return True
        else:
            return color1 != color2