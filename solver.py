import time
import functools
import math
import sys

from game_state import GameState

MAX_SOLUTION_LENGTH = 200
MAX_STACK_SIZE = 100000
FIND_SHORTEST = True


def main():
    intro_print()

    filename = None
    # Get filename from command line
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    # Load game state from file
    # Or get it from user input
    if filename != None:
        input_data=load_game_state(filename)
    else:
        input_data = get_input()
    
    print("Initial state:")
    print(input_data)
    print("Solving...")

    solve(input_data)


def intro_print():
    """
    Prints introductory test of the program's features
    """
    print("Launching...")
    print(flush=True)

def get_input():
    return input("Enter a game state: ")

def load_game_state(filename):
    with open(filename, "r") as file:
        return "".join(file.readlines()).replace("\n", "")

def solve(input_data):
    # Initialize the beginning game state
    state = GameState()
    state.populate(input_data)

    # Setup lookups and other structures for the main solving loop
    state_history = {}
    search_stack = []

    # Initialize the search stack
    search_stack.append((state, [], 0))
    highest_heuristic_solution = []
    shortest_solution = [0 for i in range(MAX_SOLUTION_LENGTH+1)]

    original_state = state.clone()
    highest_heuristic = -999

    # DEBUG
    print_highest_heuristic = 0
    print_interval = 1000
    print_since = 0
    print_state_interval = 10000
    print_state_since = 0

    # Start the main solving loop
    states_searched = 0

    while True:
        if states_searched > MAX_STACK_SIZE:
            print(str(MAX_STACK_SIZE) + " stack limit reached, applying actions of highest found heuristic score")
            break
        if len(search_stack) == 0 and len(state_history) > 0:
            print("Unable to find solution")
            break

        # Take state from the end of stack
        current_search_item = search_stack.pop()
        current_state = current_search_item[0]
        current_history = current_search_item[1]

        # DEBUG
        if (
            current_search_item[2] > print_highest_heuristic
            or print_since > print_interval
        ):
            print(
                "Top heuristic",
                highest_heuristic,
                "Heuristic",
                current_search_item[2],
                "Stack size",
                len(search_stack),
                "Searched",
                states_searched,
                flush=True,
                sep=('\t')
            )

        if print_state_since > print_state_interval:
            print("Current state", current_state)

        if current_search_item[2] > print_highest_heuristic:
            print_highest_heuristic = current_search_item[2]
        if print_since > print_interval:
            print_since = 0
        if print_state_since > print_state_interval:
            print_state_since = 0
        print_since += 1
        print_state_since += 1

        # End searches that run too deep
        if len(current_history) > MAX_SOLUTION_LENGTH:
            continue

        # End searches that are longer than the shortest solution
        actions_needed = current_state.actions_needed_at_least()
        if len(current_history) + actions_needed > len(shortest_solution):
            continue

        if current_state.is_won():
            print("New solution")
            print("Length:", len(current_history))
            print("States searched:", states_searched)
            print("Stack size:", len(search_stack))
            print(flush=True)
            if FIND_SHORTEST:
                if len(current_history) < len(shortest_solution):
                    shortest_solution = current_history
                continue # Find shortest
            else:
                break

        current_actions = current_state.get_legal_actions()

        for action in current_actions:
            clone = current_state.clone()
            clone.apply_action(action)

            # Hash the state, make sure we don't revisit a state
            clone_hash = hash(clone)
            if clone_hash in state_history:
                if state_history[clone_hash] == clone:
                    continue
            state_history[clone_hash] = clone

            heuristic_score = clone.get_heuristic_value()

            if heuristic_score >= highest_heuristic:
                highest_heuristic = heuristic_score
                highest_heuristic_solution = current_history + [action]

            new_history = list(current_history)
            new_history += [action]

            search_stack.append((clone, new_history, heuristic_score))
            states_searched += 1

        # Sort the search stack such that the latest action has the highest heuristic score
        search_stack.sort(key=lambda item: item[2])

    print(original_state)
    for action in shortest_solution:
        print(action)
        original_state.apply_action(action)
        print(original_state)
        print()


if __name__ == "__main__":
    main()
