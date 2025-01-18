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

def method_1(state):
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
