def DFS(currentNode , graph , visitedNodesIndexes):
    if not currentNode in visitedNodesIndexes:
        print(f'visiting {currentNode} node')
        visitedNodesIndexes.add(currentNode)
        for node in graph[currentNode]:
           DFS(node , graph , visitedNodesIndexes)

#complete Graph search
def DFSCompleteSearchOfGraph():
    graph = {
                '6' : ['4','7'],
                '5' : ['0','7'],
                '18' : ['22'],
                '22' : ['5','18'],
                '0' : ['5', '6' , '7'],
                '7' : ['8'],
                '2' : [], #unreafrenced G
                '4' : ['8'],
                '8' : ['22']
    }

    visitedNodesIndexes = set()
    DFS('6' , graph , visitedNodesIndexes)
    print(visitedNodesIndexes)


def DFS_with_goal(currentNode , graph , visitedNodesIndexes,goal):
    if currentNode == goal: 

        return 1
    
    else :
        if len(graph[currentNode]) == 0 : 
            return 0
        if not currentNode in visitedNodesIndexes:
            print(f'visiting {currentNode} node')
            visitedNodesIndexes.append(currentNode)
            index = 0
            for node in graph[currentNode]:
                index -=-1
                if(DFS_with_goal(node , graph , visitedNodesIndexes,goal)):
                    return 1
                else:
                    if index == len(graph[currentNode]):
                        visitedNodesIndexes.pop()
                        return 0


def DFSUnInformedSearchOfGraph():
    graph = {
                '6' : ['2','4'],
                '5' : ['0','7'],
                '18' : ['22'],
                '22' : ['5','18'],
                '0' : ['5', '6' , '7'],
                '7' : ['8'],
                '2' : ['12'],
                '12' : ['66'],
                '66' : [],
                '4' : ['8'],
                '8' : ['22']
    }

    goal = '7'
    visitedNodesIndexes = []
    DFS_with_goal('6' , graph , visitedNodesIndexes,goal)
    print(f"the best way to reach into {goal} is {visitedNodesIndexes}")

DFSUnInformedSearchOfGraph()