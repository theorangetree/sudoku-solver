# Sudoku solver
I attempted to make a Sudoku solver that doesn't use trial and error.
Eventually, I learned that this is too difficult for the hardest puzzles.

### Performance
Currently, the solver can solve most puzzles without guessing.
However, if the solver gets stuck, it uses recursion to find the final answer.

### Setting up the 9x9 grid
First, the board takes as input a list of 9 lists, each with 9 cells.
Each empty cell is represented as a set of 9 possible integers (1 through 9)

Second, link the original input to 3 representations of the same board:
* 9 lists of rows
* 9 lists of columns
* 9 lists of 3x3 regions

### Human-like strategies
* Same zone -> eliminate possibilities based on what is already soved in their zone
* Only possibility -> fill cells with sets of size 1, i.e. one possible number
* Only location -> fill cells if it is the only place where a number can go in its zone
* Naked chain -> identify when n cells (in a zone) share the same set of n possible numbers
* Hidden chain -> identify when n possible numbers share the same n possible cell locations in a zone
* Line in region -> identify unsolved numbers within a row/column whose only possible locations are in the same region
* Region in line -> identify unsolved numbers within a region whose only possible locations are in the same row or column

Zone refers to either a row, column, or 3x3 region

### Recursion strategy
If the human-like strategies fail, perform a depth first search for the solution using recursion.