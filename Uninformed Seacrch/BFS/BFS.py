def bfs(currentNode, graph ,visited,queue): 
  visited.append(currentNode)
  queue.append(currentNode)
  while queue:
    currentVisiting = queue.pop(0) 
    print (currentVisiting, end = " ") 

    #row expansion
    for node in graph[currentVisiting]:
      if not node in visited:
        visited.append(node)
        queue.append(node)

def main():
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

    visited = []
    queue = []

    bfs_with_goal('6', graph ,visited,queue,'66')
    print(f"\n{visited}")

def bfs_with_goal(currentNode, graph ,visited,queue,goal): 
  visited.append(currentNode)
  queue.append(currentNode)
  if currentNode == goal: return 1
  while queue:
    currentVisiting = queue.pop(0) 
    print (currentVisiting, end = " ") 

    #row expansion
    for node in graph[currentVisiting]:
      if not node in visited:
        visited.append(node)
        queue.append(node)
        if node == goal: return 1

main()