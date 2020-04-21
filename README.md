# Sudoku solving algorithm

## Introduction

This algorithm has the aim of eliminating the number of possible values for each cell by satisfying a number of constraints until only one possible number remains in the cell. Once this state is reached, it fills out the cell with the remaining number and continues the process until all cells have been filled out.

The Algorithm built successfully solves all Sudokus from difficulties 'Easy' to 'Hard' form [sudoku.com]('https://sudoku.com/') applying this logic. For puzzles of the difficulty level: 'Expert' the constraints implemented might not always be sufficient. Should the constraint based approach not be able to fill out all cells, the algorithm applies a backtracking approach to fill out the remaining cells testing only the numbers that remain possible for a given cell due to the constraints tested in the previous step. Therefore, the algorithm achieves to solve all puzzles from various sudoku websites or newspapers in a fraction of a second.

## Puzzle Description

Sudokus' are logic based puzzles with a 9 * 9 grid consisting of 9 non-overlapping 3 * 3 sub-grids. Every cell in the grid can hold a number between 1-9. When starting a puzzle, it usually consists of 17-30 prefilled cells. The goal of the puzzle is to fill each of the remaining (empty) cells with a number between 1-9 not breaking the following constraints:

1. Each row of the grid contains all numbers between 1-9.
2. Each column of the grid contains all numbers between 1-9.
3. Each sub-grid of the puzzle contains all numbers between 1-9.
4. Each cell only holds one number.

These rules enforce that no row, column or sub-grid is allowed to have multiple cells with the same number. Additionally, one have to note, that a good Sudoku yields only one possible solution.

## The algorithm

### Constraint based solving approach

The following list briefly describes the different steps the algorithm runs through and which functions in the script are written for which step.

1. Initialize the solving process by creating an empty grid, that can later hold all possible numbers for each cell and initialize a variable that holds a full set of each possible number (1-9). Additionally, create two copies of the input game to not have to change the input at all time. This is done by the function 'initialize_solver()'

2. Loop through each cell of the Sudoku puzzle and check, if the cell already holds a number or not. If not, take the full set of possible numbers and then:
  - Subtract the numbers, that are already present in the same row,
  - Subtract the numbers, that are already present in the same column,
  - And Subtract the numbers, that are already present in the same sub-grid

  The set of numbers left after these three subtractions are the once, that still satisfy all constraints for the given cell. Take these numbers, and store them in the empty 'possibilities' grid. This process is done by the function 'create_possible_values()'

3. Sole candidates: Loop through every cell in the 'possibilities' grid. Should a cell only hold one possible number, then this has to be the result. Write this number in the result_grid and delete it as a possible number in each cell of the same row, column or sub-grid. Repeat this process, until you can not find any new sole candidates. This process is performed by the 'check_single' function.

4. Unique candidates: For each row, column, and sub-grid check, if there is any number, that only appears in one cell. If that is the case, this number have to be the result for this cell, as each row, column, and sub-grid must hold all numbers from 1-9. Thus, add this number to the result grid and then repeat step 2. and 3. This id done by the function 'check_unique()'.

5. Naked subset: If a pair of numbers only appears to be possible in two cells of a row, column or sub-grid, these two numbers have to be in these two cells. Thus, we can remove them as possibilities for all other cells within a row, column, or sub-grid and repeat steps two to 4. This process is performed by the function 'remove_pairs()'. <em>(Note that the function is always called when creating possible new values. However, for hard sudokus it only starts impacting the results once the unique candidates are found. Thats why it is step 5 in the process. Additionally note, that the 'remove_pairs()' function calls another function itself. The 'find_pairs()' function. This basic function adds all cells that contain exactly two possible numbers in a row, column or sub-grid to a list and tries to find a perfect pair in this list. </em>

As stated above, looping through these five steps is sufficient to solve most 'easy' to 'hard' rated sudoku puzzles. Once, a solution is found, the algorithm checks again, if each row, column and sub-grid holds all numbers from 1-9. If that's the case, it deletes all variables and grids except 'grid_input' (holding the initial grid) and 'grid_output' (holding the valid solution).

If no valid solution is found, means that not all cells have been filled yet, it switches to the rule based backtracking approach to fill up the remaining cells.

### Backtracking approach

The rule based backtracking algorithm loops through each cell and checks if it is already filled with a number. If yes, it skips to the next cell. If not (means the cell holds a 0), the algorithm goes through each number found to be possible for a cell by the constraint based solving approach and applies it. It then repeats the process and checks the next cell. If no number could be placed in the next cell, the algorithm knows that the number it placed in the previous cell was wrong. It backtracks to the previous cell and tries a new number there. This process goes on until the final cell has been filled.

To do so, this algorithm only uses two functions. The 'bf_solve()' function to look up empty cells and place different numbers there as well as the 'is_possible()' helper function. The 'is_possible' helper function works very similarly to step two of the constraint based solving approach. But instead of getting returning all numbers possible for a given cell, it only tests one input number and returns 'True' if the number can placed in the cell or 'False', if the number violates one of the constraints of the puzzle.

Even though, the backtracking approach is computationally more expensive, it helps to find the correct solution, once the constraint based algorithm is stuck. Also, as it only tries out the values found to be possible for a cell by the constraint based algorithm in the first step, the computational expense is reduced to a minimal level.

## Conclusion
Most Sudoku puzzles published in newspapers or on different websites can be solved applying only the constraint based solving approach and thus mimicking human like behaviour. This process, on a normal laptop, only takes fractions of a second. Once the Puzzles become to complex for the constraint based solving approach, the backtracking approach helps out and 'guesses' the remaining cells. Therefore, the algorithm built is able to solve every solvable Sudoku puzzle. Also complex puzzles of the 'Expert' level take only fractions of a second to solve. However, trying the algorithm on the <em>'hardest sudoku ever'</em> published by [gizmodo.com]('https://gizmodo.com/can-you-solve-the-10-hardest-logic-puzzles-ever-created-1064112665') yields a solving time of over one minute.
