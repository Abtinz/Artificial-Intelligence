def DFS(currentNode , graph , visitedNodesIndexes):
    if not currentNode in visitedNodesIndexes:
        print(f'visiting {currentNode} node')
        visitedNodesIndexes.add(currentNode)
        for node in graph[currentNode]:
           DFS(node , graph , visitedNodesIndexes)

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


