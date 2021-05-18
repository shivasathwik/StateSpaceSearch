class UCS:
    def __init__(self,inputFileName,source,dest):
        self.source = source
        self.dest = dest
        self.inputFileName = inputFileName
        self.inputSourceList = []
        self.inputDestList = []
        self.inputCostList = []
        self.getInputFromFile()
    # Get Inputs from Text file
    def getInputFromFile(self):
        file = open(self.inputFileName, "r")
        for line in file:
            if (str(line).lower().find("end of input") == -1):
                paths = line.strip().split(" ")
                self.inputSourceList.append(paths[0])
                self.inputDestList.append(paths[1])
                self.inputCostList.append(paths[2])

    # Get Cost for the given node
    def getCost(self,source, dest):
        for i in range(0, len(self.inputSourceList)):
            if ((self.inputSourceList[i] == source or self.inputDestList[i] == source) and (
                    self.inputSourceList[i] == dest or self.inputDestList[i] == dest)):
                return self.inputCostList[i]

    # Get Successors for the given node
    def getSuccessor(self,node):
        successors = []
        for i in range(0, len(self.inputSourceList)):
            if (self.inputSourceList[i] == node):
                successors.append((self.inputDestList[i], float(self.inputCostList[i])))
            elif (self.inputDestList[i] == node):
                successors.append((self.inputSourceList[i], float(self.inputCostList[i])))
        return sorted(successors, key=lambda x: x[1]), len(successors)

    # Get Successors for the given node
    def getRoute(self,routeTravelled):
        route = []
        if (routeTravelled is None):
            route.append("none")
        else:
            for i in range(len(routeTravelled) - 1):
                cost = self.getCost(routeTravelled[i], routeTravelled[i + 1])
                route.append(str(routeTravelled[i]) + " to " + str(routeTravelled[i + 1]) + " => " + str(cost) + "km")
        return route

    # UCS for Uninformed and Informed search with A* Implementation
    def uniformCostSearch(self):
        fringe = []
        nodesVisited = []
        nodesGenerated=0
        nodesExpaned=0
        route = []
        cost = 0
        route.append(self.source)
        fringe.append((self.source, route, cost))
        nodesGenerated += 1
        while len(fringe) != 0:
            node, route, pathCost = fringe.pop(0)
            nodesExpaned += 1
            if node == self.dest:
                return node, route, pathCost, nodesExpaned, nodesGenerated, nodesVisited
            else:
                if (node not in nodesVisited):
                    successors, successorsCount = self.getSuccessor(node)
                    nodesGenerated += successorsCount
                    nodesVisited.append(node)
                    for childNode in successors:
                        currentRoute = route[:]
                        currentRoute.append(childNode[0])
                        cumulativeCost = pathCost + childNode[1]
                        fringe.append((childNode[0], currentRoute, cumulativeCost))
                    fringe.sort(key=lambda x: x[2])
        return None, None, None, nodesExpaned, nodesGenerated, nodesVisited