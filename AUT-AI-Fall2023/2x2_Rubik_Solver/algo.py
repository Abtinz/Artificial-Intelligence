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
        #why set? because wee do not want to check repeated explored sets
        already_explored = set()

        # Priority queue for A*
        frontier = [(
                0,#priority key and cost
                init_state, #different states of graph will be saved here
                init_location,#different states of graph will be saved here -> will be used for huristic function
                actions
            )
        ]
        
        while frontier:
        
            cost, current_state, current_location, current_actions = heapq.heappop(frontier)

            #have we reached the answer?
            if np.array_equal(current_state, solved_state()):
                return current_actions
            
            #adding new state to set
            already_explored.add(hash(np.array(current_state).tobytes()))

            for action in possible_actions:
                
                #huristic calculation with new location based on this action
                new_location = next_location(current_location, action)
                new_cost = cost  + heuristic_manhattan(
                    new_location=new_location
                )  

                # cost of the action + heuristic cost
                new_state = next_state(
                    state=current_state, 
                    action=action
                )
                
                #if we have this action and state on our set its an error to get it push without cost evaluation
                if hash(new_state.tobytes()) not in already_explored:
                    heapq.heappush(
                        frontier,
                        (new_cost, new_state.tolist(), new_location.tolist(), current_actions + [action])
                    )
                else:
                    pass
        return [] 

    elif method == 'BiBFS':
        
        actions = []
        forward_actions = []
        forward_explored_states = set()
        forward_frontier = [(
            0, 
            init_state, 
            init_location,
            forward_actions
        )]
        
        backward_actions = []
        backward_explored_states = set()
        backward_frontier = [(
            0, 
            solved_state, 
            solved_location,
              backward_actions
        )]
        
        while forward_frontier and backward_frontier:

            actions = bidirectional_search(
                forward_frontier = forward_frontier, 
                forward_explored_states = forward_explored_states,
                backward_frontier = backward_frontier,
                backward_explored_states = backward_explored_states
            )

            if not actions is None:
                return actions
            else:
                actions = []

        return actions
    
    else:
        return []
    
def iddfs_repeating_depths(current_state, current_depth ,explored_nodes_count,actions,limit):
    
    if np.array_equal(current_state, solved_state()):
        return actions,True
    else:
            explored_nodes_count[0] += 1

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
                    
def bidirectional_search(forward_frontier, forward_explored_states, backward_frontier, backward_explored_states):

    
    final_common_point = common_point_founder(
        forward_frontier= forward_frontier,
        backward_explored_states= backward_explored_states
    )

    if final_common_point is not None:

        forward_actions = []
        for _, state, location,  actions in forward_frontier:
            for action in actions:
                if np.array_equal(final_common_point, state):
                    forward_actions.append(action) 

        backward_actions = []
        for _, state, location,  actions in backward_frontier:
            for action in actions:
                if np.array_equal(final_common_point, state):
                    backward_actions.append(action) 

        return forward_actions + backward_actions

    bibfs_backward_forward_process(
        frontier = backward_frontier,
        explored_states=backward_explored_states
    )

    

    bibfs_backward_forward_process(
        frontier = forward_frontier,
        explored_states=forward_explored_states
    )
        
    return None
    
def common_point_founder(forward_frontier,backward_explored_states):
    for __, state, ___ , _ in forward_frontier:
        if hash(state.tobytes()) in backward_explored_states:
            return state
    return None
        
def bibfs_backward_forward_process(frontier,explored_states):

    temp_frontier = []
    
    for cost, state, locations, actions in frontier:
 
        for action in possible_actions:
            print(action)
            new_state = next_state(
                state = state, 
                action = action
            )

            if not hash(new_state.tobytes()) in explored_states:
                
                explored_states.add(hash(new_state.tobytes()))
                temp_frontier.append(
                    (
                        cost + 1, 
                        new_state,
                        next_location(
                            location=locations, 
                            action = action
                        ), 
                        actions + [action]
                    )
                )

               
    frontier[:] = temp_frontier
                

def heuristic_manhattan(new_location):
    
    #this function will calculates the manhattan heuristic value of current state.
    #Arg:  new_location (numpy.array): Current location of the little cubes.
    #Returns: The manhattan heuristic value.
    return np.sum(np.abs(new_location - solved_location))
