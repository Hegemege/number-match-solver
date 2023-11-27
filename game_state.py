
class GameState:
    def __init__(self):
        self.actions_taken = 0

    def populate(self, input_data):
        pass

    def clone(self):
        """
            Clones the given GameState object
        """
        clone = GameState()

        clone.actions_taken = self.actions_taken

        return clone

    def is_won(self):
        """
            Determine if the current state is the won end state
        """

        return True

    def get_legal_actions(self):
        """
            Returns all legal actions as 3-tuple of "Match" + indices that are matched,
            or "Add" + None, None when more numbers are added
        """
        actions = []

        return actions

    def apply_action(self, action):
        """
            Applies the given action to this state. Assumes that the action is valid.
        """
        self.actions_taken += 1

    def get_heuristic_value(self):
        """
            Returns a heuristic value for choosing a state over another
        """
        score = 0

        return score

    def __eq__(self, other):
        return True

    def hash_string(self):
        return "TODO"

    def __hash__(self):
        return hash(self.hash_string())

    def __str__(self):
        return "Board:\n" + "TODO"
