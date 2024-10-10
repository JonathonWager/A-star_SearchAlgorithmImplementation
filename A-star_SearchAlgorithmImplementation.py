#Jonathon Wager
#COIS 4550
#Assignment 1
#A* algorithm implimentation with 8 puzzle problems

import heapq
import copy
from random import randrange
import time
import tracemalloc

#puzzle class to store a given state, its cost, its hueristic + cost score and its parent
class puzzle:
    def __init__(self, state, cost, score, parent):
        self.state = state
        self.cost = cost
        self.score = score
        self.parent = parent
    #this is simply for the heapq when it has to compare the objects if score and cost are equal to others
    def __lt__(self, other):
        # If priorities are equal, compare by cost, or choose another attribute
        return self.score < other.score if self.score != other.score else self.cost < other.cost

#adds state to the priority queue
def add_to_queue(queue, state,cost, priority):
    heapq.heappush(queue, (priority, cost, state))

#gets highest priority state from the queue
def pop_from_queue(queue):
    # Popping and returning the tuple (priority, cost, state)
    priority, cost,state = heapq.heappop(queue)
    return priority, state

#this is the misplaced tiles hueristic scoring function
def misplaced_tiles(state, goal_state):
    misplaced_tiles = 0
    for x in range(3):
        for y in range(3):
            if(state[x][y] != goal_state[x][y] and state[x][y]!= 0):
                misplaced_tiles += 1
    return misplaced_tiles

#this is the custom manhatten heuristic with adjusted weights
def weighted_corners(state, goal_state):
    score = 0
    for x in range(3):
        for y in range(3):
            input_val = state[x][y]
            # Exclude the blank tile from the calculation
            if input_val == 0:
                continue
            # Find the goal position of the current tile
            for gx in range(3):
                for gy in range(3):
                    if goal_state[gx][gy] == input_val:
                        # Add the Manhattan distance for this tile to the total score
                        if(gx != 1 and gy != 1):
                            score += abs(gx - x) + abs(gy - y)
                        else:
                            score += (abs(gx - x) + abs(gy - y))/2
    return score
#manhatten distance heurisitic scoring calculation
def manhattan_distance(state, goal_state):
    score = 0
    for x in range(3):
        for y in range(3):
            input_val = state[x][y]
            # Exclude the blank tile from the calculation
            if input_val == 0:
                continue
            # Find the goal position of the current tile
            for gx in range(3):
                for gy in range(3):
                    if goal_state[gx][gy] == input_val:
                        # Add the Manhattan distance for this tile to the total score
                        score += abs(gx - x) + abs(gy - y)
    return score

#this function given a node and a list of all previously visited states returns the next nodes/states that are possible and not allready visited
def find_new_states(current_puzzle, visited_states):
    current_state = current_puzzle.state
    states = []
    #find where 0 is in the given state and save the x and y values
    for t in range(3):
        for z in range(3):
            if(current_state[t][z] == 0):
                x=t
                y=z
                break
    #given where 0 is calcualte what moves are possible and create a copy of the orginal state and modify it so it is the new possible state
    #also checking if the newly generated state has been visited. if so do not add it to the states to be returned
    if((x+1) <= 2):
        new_state = copy.deepcopy(current_state)
        new_state[x+1][y] = 0
        new_state[x][y] = current_state[x+1][y]
        if(check_visited(new_state,visited_states)):
            states.append(new_state)
    if((x-1) >= 0):
        new_state = copy.deepcopy(current_state)
        new_state[x-1][y] = 0
        new_state[x][y] = current_state[x-1][y]
        if(check_visited(new_state,visited_states)):
            states.append(new_state)
    if((y+1) <= 2):
        new_state = copy.deepcopy(current_state)
        new_state[x][y+1] = 0
        new_state[x][y] = current_state[x][y+1]
        if(check_visited(new_state,visited_states)):
            states.append(new_state)
    if((y-1) >= 0):
        new_state = copy.deepcopy(current_state)
        new_state[x][y-1] = 0
        new_state[x][y] = current_state[x][y-1]
        if(check_visited(new_state,visited_states)):
            states.append(new_state)
    
    #once all possible states are created we need to add them to visited states because we have seen them now
    puzzlestates = []
    for state in states:
        #add to visited states
        visited_states.add(convert_to_immutable(state))
        #create a node object and add that to new list to be returned
        puzzlestates.append(puzzle(state,0,0,current_puzzle))
    return puzzlestates

#checks if state has been visited allready
def check_visited(state, visited_states):
    if convert_to_immutable(state) not in visited_states:
        return True
    else:
        return False

#converts state to tuple so it can be hashed and searched for quickly
def convert_to_immutable(state):
    return tuple(tuple(row) for row in state)

#generates a random state and returns it
def state_generator():
    tiles = [1,2,3,4,5,6,7,8]

    init_state = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]  
    ]
    for tile in tiles:
        placed = False
        while(placed == False): 
            x = randrange(3)
            y = randrange(3)
            if(init_state[x][y] == 0):
                placed = True
                init_state[x][y] = tile

    return init_state

#function to check how many inversions a state has
def getInvCount(arr):
    inv_count = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != 0 and arr[i] != 0 and arr[i] > arr[j]:
                inv_count += 1
    return inv_count
 
     
# This function returns true
# if given 8 puzzle is solvable.
def isSolvable(puzzle) :
    # Count inversions in given 8 puzzle
    inv_count = getInvCount([j for sub in puzzle for j in sub])
    # return true if inversion count is even.
    return (inv_count % 2 == 0)

#when passed a state node this function will print out the most optimal path to that state
def get_path(finished_puzzle):
    cost = 0
    while(finished_puzzle.parent != None):
        cost += 1
        for row in finished_puzzle.state:
           print(row)
        print("\n")
        finished_puzzle = finished_puzzle.parent
    print(cost)

#this function takes a state and preforms the a* algorithm to test the heurisitcs of the assignment
def test_huristics(start_state):
    #goal state
    goal_state= [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]  
    ]
    #list of heurisitc funcitons to test
    functions = [weighted_corners , manhattan_distance, misplaced_tiles]
    #list to return when optimal solution is found
    return_scores = []
    #printing starting state
    for row in start_state:
        print(row)

    print("\n")
    #loop through each of the heurisitics
    for func in functions:
        #getting start time and starting memory tracking
        start_time = time.time()
        tracemalloc.start()

        #creaeting priority queue
        priority_queue = []
        #creating a set of visited states
        visited_states = set() 
        print(func.__name__)
        print("Initial Heuristic score = " + str(func(start_state,goal_state)))

        #creating starting node with the starting state
        s_state = puzzle(start_state,0,func(start_state,goal_state),None)
        #adding the node to the priority queue
        add_to_queue(priority_queue,s_state,0,s_state.score)
        #also adding it to visited states
        visited_states.add(convert_to_immutable(start_state))  
        #while the priority queue is not empty
        while(priority_queue):     
            #get the current node  
            current_puzzle = pop_from_queue(priority_queue)
            #get the state from that node
            current_state = current_puzzle[1] 

            #check to see if current node is solved
            if(current_state.state == goal_state):
                #if it is solved print all stats of the current heurisitc 
                end_time = time.time()
                time_required = end_time - start_time
                current,peak = tracemalloc.get_traced_memory()
                print("Peak Memory Usage = " + str(round(peak/1024/1024,2)) + "MB")
                tracemalloc.stop()
                print(f"Time required: {time_required} seconds")
                print("Nodes Generated = " + str(len(visited_states)))
                print("Solution found in " + str(current_state.cost) + " moves")
                #return the cost scores
                #this was for testing hueristic admisablity
                return_scores.append(str(current_state.cost))
                print("\n")
                #break because we have found optimal solution
                break
            #get new possible states given the current state
            states = find_new_states(current_state,visited_states)
            #for each of the new possible states
            for s in states:
                #calcualte their new cost and score and assign the node the values
                s.cost = current_state.cost + 1
                s.score =func(s.state,goal_state)+ s.cost 
                #add node to the prioirty queue
                add_to_queue(priority_queue,s, s.cost ,s.score)
    return return_scores

#program to test and run A* algorithm
user_input = input("Please Enter 1 to enter your own states or Enter 2 to randomly generate states: ")
user_input = int(user_input)
#if the user wants to enter their own states
if(user_input == 1):
        end_loop = 0
        while(end_loop == 0):
            tiles = [1,2,3,4,5,6,7,8,0]
            count = 0
            blank_state= [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]  
            ]
            #get user input for each tile to create a state to test
            while count< 9:
                tile_selection = input("Please enter Tile " + str(count) + ":")
                print(str(int(tile_selection)))
                if(int(tile_selection) in tiles):
                    #if they selected a tile that has not been placed yet. Remove it from the list and add it to the blank state
                    tile_selection = int(tile_selection)
                    tiles.remove(tile_selection)
                    if count < 3:
                        blank_state[0][count] = tile_selection
                    elif count >= 3 and count < 6:
                        blank_state[1][count-3] = tile_selection
                    elif count >= 6 and count < 9:
                        blank_state[2][count-6] = tile_selection
                    count +=1 
                else:
                    #they entered a tile that has allready been placed or is not 1 of the 9 accepted
                    print("Invalid puzzle peice 0,1,2,3,4,5,6,7,8 are accepted, Or you have allready selected this peice. Please Try Again!")
            #check if solvable
            if(isSolvable(blank_state)):
                test_huristics(blank_state)
            else:
                print("The puzzle you entered is unsolvable!\n")
            user_input = input("Would you like to enter another state? If so enter 1. To end the loop eneter 0: ")
            #clause to end the loop
            if(int(user_input)==0):
                print("exiting loop")
                end_loop = -1
#if the user wants to randomly generate states
if(user_input == 2):
    amount_of_states = input("Please enter how many states you would like to generate: ")
    amount_of_states = int(amount_of_states)
    print("starting to generate " + str(amount_of_states) + " states!")
    #this problems variable was used for testing huerisitcs over thousands of states. It kept track of the times any of the 3 heuristics did not keep track of eachother
    problems = 0
    x = 0
    w = 0
    #this was for printing the % of states finished
    interval = int(amount_of_states/ 10)
    #loop through number of states provided
    while x < amount_of_states:
        #get random state
        state = state_generator()
        printed = False
        scores = []
        #check if the state is solvable and if it is preform the test
        if(isSolvable(state)):
            scores = test_huristics(state)
        #if scores are returned
        if(len(scores) > 0):
            #print % completed
            if(w == interval):
                print(str(int((x/amount_of_states)*100)) + "%")
                w = 0
            x += 1
            w += 1
            tester = scores[0]
            #check if the scores returned have any problems. if so print the problems
            for y in range(2):
                if(scores[y+1] != tester):
                    if(printed == False):
                        print("Weighted Corners= " + str(scores[0]))  
                        print("Manhat = " + str(scores[1]))  
                        print("Misplaced = " + str(scores[2]))  
                        print(state)
                        print("\n")
                        problems += 1
                        printed = True
    print("Problems = " + str(problems) + " out of " + str(amount_of_states) + " states")

