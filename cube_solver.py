import sys
import random
import time

#          -------
#         | 16 17 |
#         |   Y   |
#         | 18 19 |
#  ------- ------- ------- -------
# | 12 13 | 00 01 | 04 05 | 08 09 |
# |   X   |   Z   |   X   |   Z   |
# | 14 15 | 02 03 | 06 07 | 10 11 |
#  ------- ------- ------- -------
#         | 20 21 |
#         |   Y   |
#         | 22 23 |
#          -------


SOLVED_STATE = "WWWWYYYYRRRRBBBBGGGGOOOO"

MOVES = {
    "CW_X": [0, 21, 2, 23, 6, 4, 7, 5, 19, 9, 17, 11, 12, 13, 14, 15, 16, 1, 18, 3, 20, 10, 22, 8], # X turn clock-wise
    "CW_Y": [0, 1, 14, 15, 4, 5, 2, 3, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 18, 19, 22, 20, 23, 21], # Y turn clock-wise
    "CW_Z": [2, 0, 3, 1, 18, 5, 19, 7, 8, 9, 10, 11, 12, 20, 14, 21, 16, 17, 15, 13, 6, 4, 22, 23], # Z turn clock-wise
    "CCW_X": [0, 17, 2, 19, 5, 7, 4, 6, 23, 9, 21, 11, 12, 13, 14, 15, 16, 10, 18, 8, 20, 1, 22, 3], # X turn counter clock-wise
    "CCW_Y": [0, 1, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13, 2, 3, 16, 17, 18, 19, 21, 23, 20, 22], # Y turn counter clock-wise
    "CCW_Z": [1, 3, 0, 2, 21, 5, 20, 7, 8, 9, 10, 11, 12, 19, 14, 18, 16, 17, 4, 6, 13, 15, 22, 23], # Z turn counter clock-wise
}

def perform_move(state, move):
    assert move in MOVES, f"Unrecognized move {move}"
    # return tuple([state[idx] for idx in MOVES[move]]) 
    return ''.join([state[idx] for idx in MOVES[move]])

def is_solved(state):
    for i in range(0, 24, 4):
        if len(set(state[i:i+4])) > 1:
            return False
    return True

def scramble(state, show_move = False):
    moves = []
    
    for _ in range(random.randint(1, 20)): 
        moves.append(random.choice(list(MOVES.keys())))
        state = perform_move(state, moves[-1])
        
    if show_move:
        move_string = f"\nScrambling @_@\": {moves[0]}"
        for m in moves[1:]:
            move_string += f"-->{m}"
        print(move_string, "\n")
        
    return state

def pretty_print(state):
    print(
        (
            f"         -------                 \n"
            f"        | {state[16]}   {state[17]} |                \n"
            f"        |   Y   |                \n"
            f"        | {state[18]}   {state[19]} |                \n"  
            f" ------- ------- ------- ------- \n"
            f"| {state[12]}   {state[13]} | {state[0]}   {state[1]} | {state[4]}   {state[5]} | {state[8]}   {state[9]} |\n"
            f"|   X   |   Z   |   X   |   Z   |\n"
            f"| {state[14]}   {state[15]} | {state[2]}   {state[3]} | {state[6]}   {state[7]} | {state[10]}   {state[11]} |\n"
            f" ------- ------- ------- ------- \n"
            f"        | {state[20]}   {state[21]} |                \n"
            f"        |   Y   |                \n"
            f"        | {state[22]}   {state[23]} |                \n"
            f"         -------                 \n"
        )
    )

def _solve(state,  moves, depth, visited_state):
    """
    A method to check if a solved state can be reached from the input state within a given depth.

    ARGUMENT:

    states(str): starting exploration state.
    moves(List[str]): a list (history) of moves from initial state to the starting exploration state.
    depth(int): maximum depth to explore.
    visited_state(Dict[str, int]): all the states (and its depth) visited so far

    SUMMARY:

    - First check if the starting exploration state is a solved state or not. If yes, then a solution
    is found and return the moves.
    - Then we check, and only continue the exploration, if the depth is greater than zero.
    - [KEY STEP!!] Next, we check if the starting  state is already visited before and if previously
    visitation has depth greater then the current depth. If so, then can stop the exploration of this
    starting stage because it means we have already explore the same starting state before and explored
    with greater depth. If we did not find soulution previously (with greater depth) then we won't find
    a solution this time with less depth.
    - We continue the exploration if either we have never seen (explore) the given starting state or
    we will explore the starting state again but with a greater depth.
    - We apply all possible moves to the starting state to get the next state, update (add) the moves
    with the new move and recursively call _solve again with the new state and decresing the depth by 1.
    (the application of each possible moves consumes one depth)
    
    """
    
    if is_solved(state):
        return list(moves)
    if depth <= 0:
        return
    if visited_state.get(state, -1) >= depth:
        return
    visited_state[state] = depth
    for move in list(MOVES.keys()):
        next_state = perform_move(state, move)
        next_moves = moves + [move]
        # moves.append(move)
        result = _solve(next_state, next_moves, depth - 1, visited_state)
        # moves.pop()
        if result:
            return result
    return

def method_1(state):
    """
    A method for solving 2x2 Rubik's cube

    ARGUMENT:

    state: initial (scramble) state.

    DEFINITION:
    
    Depth: the number of moves (with possible repeats) from initial state to current state

    SUMMARY:

    Itereating through an increasing number of depth one at a time and check if a solved
    state can be reached from the initial (scramble) state for a given depth or less.
    If a solution is found, a list of solution steps is returned; othereise, an empty
    list is returned. We hard coded the maximum depth exploration to be 100.
    """
    
    visited_state = {}
    state = tuple(state)
    start_time = time.time()
    for depth in range(1, 100):
        print(f"Think~~ing... (working on Depth {depth})")
        moves = _solve(state, [], depth, visited_state)
        if moves:
            end_time = time.time() - start_time
            print(f"\nYeah! solution found!! (took {end_time:.2f} seconds, visited {len(visited_state)} states)\n")
            return moves


def method_2(state):
    """
    A method for solving 2x2 Rubik's cube

    ARGUMENT:

    state: initial (scramble) state.

    SUMMARY:

    A breadth-first-search (BFS) approach where we maintain two data structure:
    
    - 'to_explore': A FIFO queue of states and their moves fromt the initial scram state.
    Initialize with the initial scramble state.
    
    - 'visited_state': A hash table of all visited state. Initiailly empty.

    Repeatly take the first element ('current_state', 'current_moves') from the front of the
    'to_explore' queue and check if it is a solved state. If yes, a solution is found and
    return the solution 'current_moves'. If not, apply all possible moves to the the
    'current_state' to arrive at set of 'next_state's and update with their corresponding moves,
    called 'next_moves'. For each 'next_state', check if it is in the 'visited_state',
    if yes then it means we have already visited this state before and don't need to explore again.
    If not, then this is a new state and we will add this 'next_state' to the 'visited_state' set
    and add this ('next_state', 'next_moves') to the back of the 'to_explore' queue.
    """
    
    visited_state = set()
    to_explore = [(state, [])] # format: [(state_0, []), ..., (state_i, [moves from state_0 to state_i]), ...]
    print("Think~~ing...")
    start_time = time.time()
    while to_explore:
        current_state, current_moves = to_explore.pop(0)

        if is_solved(current_state):
            end_time = time.time() - start_time
            print(f"\nYeah! solution found!! (took {end_time:.2f} seconds, visited {len(visited_state)} states)\n")
            return current_moves
        
        for move in list(MOVES.keys()):
            next_state = perform_move(current_state, move)
            next_moves = current_moves + [move]
            if next_state not in visited_state:
                visited_state.add(next_state)
                to_explore.append((next_state, next_moves))

    print("No solution found :(")
    return

def main():
    args = sys.argv[1:]

    if args:
        state = args[0]
    else:
        state = scramble(SOLVED_STATE, show_move=True)

    print(f'Solve the following 2x2 Rubik\'s cube (state: {state}): \n')
    pretty_print(state)
        
    moves = method_1(state)

    if not moves:
        return
    
    print("Here are the steps:\n")    
    for i, move in enumerate(moves):
        print(f"Step {i+1}: {move}")
        state = perform_move(state, move)
        pretty_print(state)
    print("There you have it, you're welcome!!")

if __name__ == '__main__':
    main()
