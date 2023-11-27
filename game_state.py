import math

COLUMNS = 9
ACTION_MATCH = "Match"
ACTION_REFRESH = "Refresh"
REFRESHES_MAX = 5

class GameState:
    def __init__(self):
        self.actions_taken = 0
        self.refreshes = REFRESHES_MAX
        self.board = []

    def populate(self, input_data):
        """
            Populates the state from the given input data.
            Converts the input from a string to lists of integers based on the columns count
        """
        for i in range(0, len(input_data), COLUMNS):
            self.board.append([int(x) for x in input_data[i : i + COLUMNS]])

        self.clean_board()

    def clone(self):
        """
            Clones the given GameState object
        """
        clone = GameState()

        clone.board = [row[:] for row in self.board]

        clone.actions_taken = self.actions_taken
        clone.refreshes = self.refreshes

        return clone

    def is_won(self):
        """
            Determine if the current state is the won end state.
            The state is won when the board is clear of numbers.
        """

        return len(self.board) == 0
    
    def actions_needed_at_least(self):
        """
            Returns the minimum number of actions needed to win the game.
            This is the number of nonzero numbers on the board divided by two, rounded up.
        """
        nonzero_filter = lambda x: x != None and x > 0
        
        nonzero_numbers = [number for row in self.board for number in row if nonzero_filter(number)]
        return math.ceil(len(nonzero_numbers) / 2)

    def clean_board(self):
        """
            Removes all rows that are full of zeroes
        """
        # Remove Nones from the end of the last row
        if len(self.board) > 0:
            while self.board[-1][-1] is None:
                self.board[-1].pop()

        # Remove rows that are all zeroes
        self.board = [row for row in self.board if sum(row) > 0]

        # Adds Nones to the end of the last row to fill it up
        if len(self.board) > 0:
            self.board[-1] += [None for i in range(COLUMNS - len(self.board[-1]))]

    def refresh_numbers(self):
        """
            Goes through the board and copies every non-zero number and appends
            them to the end of the board
        """
        # First remove all Nones from the end of the last row
        if len(self.board) > 0:
            while self.board[-1][-1] is None:
                self.board[-1].pop()

        # Flatten the board into one list and add it one-by-one
        all_values = [number for row in self.board for number in row if number > 0]
        for number in all_values:
            if len(self.board[-1]) == COLUMNS:
                self.board.append([number])
            else:
                self.board[-1].append(number)

        self.clean_board()

        self.refreshes -= 1

    def get_legal_actions(self):
        """
            Returns all legal actions as 3-tuple of "Match" + indices that are matched,
            or "Add" + None, None when more numbers are added by "refreshing"
        """
        actions = []

        # Add actions for matching
        # Two numbers can be matched on the board if they are the same, or if their sum adds to 10
        # The numbers can be on the same row or column, or diagonally, any distance from each other,
        # and must see each other (only zeroes in between the two).
        # The numbers can be matched also if they connect through the end of the previous row and the beginning of the next row

        # Loop through the board and check for matches
        for row_index, row in enumerate(self.board):
            for column_index, number in enumerate(row):
                # If the number is zero, skip it
                if number == 0 or number == None:
                    continue

                # Check for matches diagonally up right
                for i in range(1, COLUMNS):
                    check_row_index = row_index - i
                    check_column_index = column_index + i
                    if check_row_index < 0:
                        break
                    if check_column_index >= COLUMNS:
                        break
                    check_number = self.board[check_row_index][check_column_index]
                    if check_number == 0 or check_number == None:
                        continue
                    if number + check_number == 10 or number == check_number:
                        actions.append((ACTION_MATCH, (row_index, column_index), (check_row_index, check_column_index)))
                    break # Found non matching blocking number

                # Check for matches right on the same row
                for i in range(column_index + 1, len(row)):
                    if row[i] == 0 or row[i] == None:
                        continue
                    if number + row[i] == 10 or number == row[i]:
                        actions.append((ACTION_MATCH, (row_index, column_index), (row_index, i)))
                    break # Found non matching blocking number

                # Check for matches diagonally down right
                for i in range(1, COLUMNS):
                    check_row_index = row_index + i
                    check_column_index = column_index + i
                    if check_row_index >= len(self.board):
                        break
                    if check_column_index >= COLUMNS:
                        break
                    check_number = self.board[check_row_index][check_column_index]
                    if check_number == 0 or check_number == None:
                        continue
                    if number + check_number == 10 or number == check_number:
                        actions.append((ACTION_MATCH, (row_index, column_index), (check_row_index, check_column_index)))
                    break # Found non matching blocking number

                # Check for matches down on the same column
                for i in range(row_index + 1, len(self.board)):
                    check_number = self.board[i][column_index]
                    if check_number == 0 or check_number == None:
                        continue
                    if number + check_number == 10 or number == check_number:
                        actions.append((ACTION_MATCH, (row_index, column_index), (i, column_index)))
                    break # Found non matching blocking number

        # Check for matches through the end of the previous row and the beginning of the next row
        # Only consider the last non-zero number on the previous row and the first non-zero number on the next row
        for row_index, row in enumerate(self.board):
            if row_index == len(self.board) - 1:
                break

            next_row = self.board[row_index + 1]

            nonzero_filter = lambda x: x[1] != None and x[1] > 0
            
            last_non_zero = list(filter(nonzero_filter, enumerate(row)))[-1]
            first_non_zero = list(filter(nonzero_filter, enumerate(next_row)))[0]

            if last_non_zero[1] + first_non_zero[1] == 10 or last_non_zero[1] == first_non_zero[1]:
                actions.append((ACTION_MATCH, (row_index, last_non_zero[0]), (row_index + 1, first_non_zero[0])))

        # Add actions for refreshing
        if self.refreshes > 0:
            actions.append((ACTION_REFRESH, None, None))

        return actions

    def apply_action(self, action):
        """
            Applies the given action to this state. Assumes that the action is valid.
            First is the action type, then the indices of the numbers to be matched
        """
        self.actions_taken += 1

        if action[0] == ACTION_MATCH:
            self.board[action[1][0]][action[1][1]] = 0
            self.board[action[2][0]][action[2][1]] = 0
        elif action[0] == ACTION_REFRESH:
            self.refresh_numbers()

        self.clean_board()

    def get_heuristic_value(self):
        """
            Returns a heuristic value for choosing a state over another
        """
        score = 0

        # The score is increased by the number of actions taken
        score += self.actions_taken * 3

        # The score is increased by the number of zeroes on the board
        for row in self.board:
            score += row.count(0) * 1

        # The score is decreased by the number of rows on the board
        score -= len(self.board) * 10

        # The score is decreased by the number of refreshes used
        score -= (REFRESHES_MAX - self.refreshes) * 50

        return score

    def __eq__(self, other):
        if len(self.board) != len(other.board):
            return False

        for row_index, row in enumerate(self.board):
            if len(row) != len(other.board[row_index]):
                return False

            for column_index, number in enumerate(row):
                if number != other.board[row_index][column_index]:
                    return False

        return True

    def hash_string(self):
        return "".join([str(number) for row in self.board for number in row]) + "-refreshes" + str(self.refreshes)

    def __hash__(self):
        return hash(self.hash_string())

    def __str__(self):
        return "Board:\n" + "Refreshes:" + str(self.refreshes) + "\n" + "\n".join(["".join(map(lambda x: str(x) if x != None and x > 0 else ".", row)) for row in self.board])
