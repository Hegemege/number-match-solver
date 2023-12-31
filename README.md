# number-match-solver

Solver for https://play.google.com/store/apps/details?id=com.easybrain.number.puzzle.game

Each level presents a vertically scrolling grid with 9 columns. The first 35 cells (4 rows minus one cell) contain a number. The goal is to clear the whole grid by matching two numbers per turn, given the following rules:

- Numbers can be matched in the main cardinal directions and diagonally.
- Two numbers can match only when there is no unmatched numbers between them
- The two numbers must add up to 10, or must be the same number
- The last unmatched number on a row, and the first unmatched number on the next row can match, even if they are not on the same column or diagonal.
- The player can at any time add more numbers on the board by copying all existing unmatched numbers in order starting from the topleft corner going right, and adding them without any gaps to the end of the grid. The player can only do this a given number of times (5).
- When all numbers on a row have been matched, the row is removed and the rows below it are moved up.
- When the player has exhausted all legal moves and has ran out of times they can add more numbers to the grid, the game is lost.

## Usage

```
python solver.py [filename]
```

If a filename is given, reads the input game state from the given file. See the example files.

Without the filename parameter, the user is prompted to enter the initial game state as a continuous string of numbers.

The solver can be configured to output the first found solution immediately, instead of looking for the shortest solution. The solver also has a configuration for the maximum number of game states it will evaluate before exiting, see the beginning of `solver.py`

## About

In order to assist the search, a simple heuristic function is used to evaluate each game state. I did some initial testing to get the solver to find a solution quickly, but the heuristic could be optimized. For example, it could reward removing a number completely from the board, as it makes matching the remaining numbers easier. Also technically a 5 is a more difficult number to match, so it could reward removing the fives over other numbers.

Currently the heuristic rewards a depth-first approach, as otherwise the search space explodes quite easily. For example, there are rarely cases where player should add more numbers without clearing all existing matches, but it can happen near the endgame.

Some game states might conclude early, dooming the player to play an unbeatable game, which also makes the solver slow down, possibly unable to solve a given state. It's unclear to me yet whether all boards generated by the game can be solved, how they are generated, or whether the developers use similar heuristics for determining the difficulty of levels, and adjust the gameplay experience. Based on my intuition, they might generate content that is always winnable.

## License

See LICENSE
