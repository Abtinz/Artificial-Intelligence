import heapq
import numpy as np
from state import next_state, solved_state
from location import next_location,solved_location


solved_location = solved_location()
possible_actions = [i for i in range(0, 12)]


def solve(init_state, init_location, method,max_depth):
    """
    Solves the given Rubik's cube using the selected search algorithm.
 
    Args:
        init_state (numpy.array): Initial state of the Rubik's cube.
        init_location (numpy.array): Initial location of the little cubes.
        method (str): Name of the search algorithm.
 
    Returns:
        list: The sequence of actions needed to solve the Rubik's cube.
    """

    #current statuses
    current_location = init_location
    current_state = init_state


    # instructions and hints:
    # 1. use 'solved_state()' to obtain the goal state.
    # 2. use 'next_state()' to obtain the next state when taking an action .
    # 3. use 'next_location()' to obtain the next location of the little cubes when taking an action.
    # 4. you can use 'Set', 'Dictionary', 'OrderedDict', and 'heapq' as efficient data structures.

    if method == 'Random':
        return list(np.random.randint(1, 12+1, 10))
    
    elif method == 'IDS-DFS':

        actions = []
        already_expanded = []
        explored_nodes_count = [0]
        
        if max_depth is None:
            max_depth = 20
        
        if np.array_equal(solved_state , current_state):
            print("its already solved and no need to thanks ...")
            return actions
            
        for current_limitation in range(0,int(max_depth)):
            
            actions, isComplete = iddfs_repeating_depths(
                current_state = current_state,
                current_depth= 0,
                limit = current_limitation,
                explored_nodes_count = explored_nodes_count,
                actions= actions
            )

            if isComplete:
                print(f"expanded nodes:{already_expanded}")
                print(f"explored nodes:{explored_nodes_count[0]}")
                return actions
        return actions
            

        
    
    elif method == 'A*':

        actions = []
        frontier = [(0, init_state, init_location, actions)]
        already_explored = set()

        while frontier:

            cost, current_state, current_location, current_actions = heapq.heappop(frontier)

            if np.array_equal(current_state, solved_state()):
                return current_actions
            
            already_explored.add(hash(np.array(current_state).tobytes()))

            for action in possible_actions:

                new_state = next_state(
                    state = current_state, 
                    action =action
                )
                
                new_location = next_location(current_location, action)
                new_cost = cost + heuristic_manhattan(
                    new_location = new_location
                )

                new_entry = (new_cost, new_state, new_location, current_actions + [action])
                print(new_entry)
                if any(hash(new_state.tobytes()) == hash_state for hash_state in already_explored):
                    heapq.heappush(frontier, new_entry)

        return [] 

    elif method == 'BiBFS':
        ...
    
    else:
        return []
    
def iddfs_repeating_depths(current_state, current_depth ,explored_nodes_count,actions,limit):
    
    if np.array_equal(current_state, solved_state()):
        return actions,True
    else:
            explored_nodes_count[0] += 1
            print(explored_nodes_count)
            if(current_depth <= limit):
                for action in possible_actions:
                    
                    new_actions = actions + [action]
                
                    new_actions , isComplete = iddfs_repeating_depths(
                        current_state = next_state(current_state, action),
                        current_depth = current_depth + 1, 
                        limit= limit,
                        explored_nodes_count = explored_nodes_count,
                        actions = new_actions
                    )
                    #print(f"{new_actions},{isComplete},{limit},{current_depth}",end="---")

                    if isComplete:
                        return new_actions,isComplete
            return actions , False
                    
    
def heuristic_manhattan(new_location):
    
    #this function will calculates the manhattan heuristic value of current state.
    #Arg:  new_location (numpy.array): Current location of the little cubes.
    #Returns: The manhattan heuristic value.
    return np.sum(np.abs(new_location - solved_location)) // 4