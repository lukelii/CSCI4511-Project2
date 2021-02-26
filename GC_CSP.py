from typing import Generic,TypeVar
import sys
import pprint

#defining Types for generic
V = TypeVar('V') # variable type
D = TypeVar('D') # domain type

#pretty print for nested dict
pp = pprint.PrettyPrinter(depth=4)

#file readin from txt.file
txt_path = 'text1.txt'
f = open(txt_path)
data_lists = f.readlines()
#three arrays for data storage
Edges = []
Vertexes = []
colors = []
#data regulations & array filled up
for data in data_lists:
    data = data.partition('#')[0]
    data = data.rstrip()
    data1 = data.strip("\n")
    data2 = data1.split(',')
    for word in data.split():
        if len(data2) == 1:
            colors.append(word)
    if len(data2) == 2:
        if data2[0] not in Vertexes:
            Vertexes.append(data2[0])
        if data2[1] not in Vertexes:
            Vertexes.append(data2[1])
        Edges.append(data2)
# convert str readin to int
Vertexes = list( map(int,Vertexes) )
# same convertion but doing it by each row
Edges = [list( map(int,i) ) for i in Edges]
color = int(colors[2])
# generating int representing color
Domain =[]
for i in range(color):
    Domain.append(i)

#define constraint using generic
class ColoringConstraint(Generic[V, D]):
    def __init__(self, Vert1, Vert2):
        self.variables = Vertexes
        self.Vert1 = Vert1
        self.Vert2 = Vert2

    #herustic as constraint with rules no adjacent plots with same color
    def herustic(self, ans):
        #both place not in ans, then no conflict is possible
        if self.Vert1 not in ans or self.Vert2 not in ans:
            return True
        else:#checking for adjacent spot with same color
            return ans[self.Vert1] != ans[self.Vert2]

class CSP(Generic[V, D]):
    def __init__(self, variables, domains):
        self.variables = variables # variables needed to be calc
        self.domains = domains # domain of these variables
        self.constraints = {}#varaibles with its domains
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                sys.exit("Missing Domain")

    #add constraint from txt
    def add_constraint(self, cons:ColoringConstraint[V,D]):
        for variable in cons.variables:
            if variable not in self.variables:
                sys.exit("Failed to add constraint")
            else:#appending constraint into constraints array
                self.constraints[variable].append(cons)

    def backtracking(self, ans = {}):
        # all variables assign, our coloring is finished
        if len(ans) == len(self.variables):
            return ans

        # get all variables in the CSP but not in the ans set
        unassigned = [v for v in self.variables if v not in ans]

        # get the every possible domain value of the first unassigned variable
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_ans = ans.copy()
            local_ans[first] = value
            # if we're still valid under herustic, we will recurse
            if self.checker(first, local_ans):
                result = self.backtracking(local_ans)
                #result equals to none, we return result
                if result is not None:
                    return result
        return None

    #checker for herustic within backtracking
    def checker(self, variable: V, ans):
        for cons in self.constraints[variable]:
            if not cons.herustic(ans):
                return False
        return True

domains = {}
for Vertex in Vertexes:
    domains[Vertex] = Domain
csp: CSP[int, int] = CSP(Vertexes  , domains)
for a in Edges:
    csp.add_constraint(ColoringConstraint(a[0], a[1]))
solution = csp.backtracking()
if solution is None:
    print("Failed to color!")
else:
    pp.pprint(solution)