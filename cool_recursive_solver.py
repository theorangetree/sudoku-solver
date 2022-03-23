#! python3
"""
Cool Sukdoku solver that uses recursion.

Main difference from  basic Sudoku solver is that the board is represented in 3 ways:
    - List of rows
    - List of columns
    - List of 3x3 regions
In the full solver, this enables more complex Sudoku strategies to be used

Solving strategies:
    - elim_row(): eliminate possibilities based on existing numbers in the row
    - elim_col(): eliminate possibilities based on existing numbers in the column
    - elim_3x3(): eliminate possibilities based on existing numbers in the 3x3
    - fill_board(): input a value in a cell if there is only one remaining possibility for that cell

Class: SudokuBoard()
    Requires a Sudoku board (list of 9 lists of rows) to be passed as an argument at initiation
    This class contains utility methods and the solve() method, which solves self.rows, self.cols, self.regions
"""

# Import modules
import copy, math, numpy

# Sample Sudoku boards
worldsHardestBoard = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 3, 6, 0, 0, 0, 0, 0],
                      [0, 7, 0, 0, 9, 0, 2, 0, 0],
                      [0, 5, 0, 0, 0, 7, 0, 0, 0],
                      [0, 0, 0, 0, 4, 5, 7, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 3, 0],
                      [0, 0, 1, 0, 0, 0, 0, 6, 8],
                      [0, 0, 8, 5, 0, 0, 0, 1, 0],
                      [0, 9, 0, 0, 0, 0, 4, 0, 0]]

evilBoard1 = [[0, 1, 8, 0, 0, 0, 0, 4, 0],
              [0, 0, 0, 8, 0, 0, 0, 6, 0],
              [9, 0, 0, 0, 5, 6, 0, 0, 0],
              [1, 0, 0, 0, 7, 0, 0, 0, 3],
              [0, 0, 3, 1, 0, 8, 6, 0, 0],
              [7, 0, 0, 0, 2, 0, 0, 0, 8],
              [0, 0, 0, 4, 6, 0, 0, 0, 1],
              [0, 3, 0, 0, 0, 9, 0, 0, 0],
              [0, 2, 0, 0, 0, 0, 7, 9, 0]]

hardBoard1 = [[0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 2, 1, 0, 0, 8, 0, 0, 0],
              [7, 0, 0, 0, 4, 0, 2, 0, 8],
              [0, 5, 0, 8, 0, 7, 4, 0, 0],
              [6, 0, 0, 0, 0, 0, 0, 0, 2],
              [0, 0, 2, 3, 0, 6, 0, 9, 0],
              [9, 0, 3, 0, 1, 0, 0, 0, 6],
              [0, 0, 0, 6, 0, 0, 1, 7, 0],
              [0, 6, 0, 0, 0, 0, 0, 0, 0]]

mediumBoard1 = [[1, 8, 0, 0, 0, 0, 9, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 2, 5],
                [0, 0, 5, 0, 7, 0, 0, 0, 3],
                [5, 0, 0, 0, 0, 4, 6, 7, 0],
                [0, 2, 0, 0, 6, 0, 0, 9, 0],
                [0, 9, 6, 2, 0, 0, 0, 0, 4],
                [2, 0, 0, 0, 4, 0, 7, 0, 0],
                [8, 7, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 4, 0, 0, 0, 0, 1, 6]]

easyBoard1 = [[7, 1, 0, 0, 0, 0, 8, 0, 5],
              [0, 8, 0, 0, 0, 0, 0, 4, 0],
              [0, 0, 9, 0, 0, 7, 0, 3, 0],
              [9, 3, 0, 1, 0, 5, 6, 2, 0],
              [0, 0, 7, 8, 0, 3, 5, 0, 0],
              [0, 5, 1, 6, 0, 2, 0, 7, 3],
              [0, 7, 0, 2, 0, 0, 9, 0, 0],
              [0, 4, 0, 0, 0, 0, 0, 8, 0],
              [6, 0, 2, 0, 0, 0, 0, 5, 1]]

# Functions for eliminating possibilities
# A blank cell starts with a set of possible numbers: 1 to 9

def elim_row(board):
    """Eliminate possibilities that have already occured in the same row"""

    for row in board.rows:
        eliminate = set([number for number in row if isinstance(number, int)])

        for col in row:
            if isinstance(col, set):
                col -= eliminate
                # check for an error
                if len(col) == 0:
                    return False

def elim_col(board):
    """Eliminate possibilities that have already occured in the same column"""

    for col in board.cols:
        eliminate = set([number for number in col if isinstance(number, int)])

        for row in col:
            if isinstance(row, set):
                row -= eliminate
                # check for an error
                if len(row) == 0:
                    return False

def elim_3x3(board):
    """Eliminate possibilities that have already occured in the same 3x3 square"""

    for region_3x3 in board.regions:
        eliminate = set([number for number in region_3x3 if isinstance(number, int)])

        for cell in region_3x3:
            if isinstance(cell, set):
                cell -= eliminate
                # check for an error
                if len(cell) == 0:
                    return False

def fill_board(board):
    """Fill squares with only 1 possibility remaining"""
    
    for y, row in enumerate(board.rows):
        for x, col in enumerate(row):
            if isinstance(col, set) and len(col) == 1:
                board.update(x, y, col.pop())

# Dictionary that maps a Sudoku board represented as lists of rows, to a board represented as lists of 3x3 regions
# Key: standard-basis cell coordinates -> Value: region-basis cell coordinates
# Example of 3x3 region-basis indices:
    # [0] [1] [2]
    # [3] [4] [5]
    # [6] [7] [8]
ROW_TO_REGION = {}
for row in range(9):
    for col in range(9):
        ROW_TO_REGION[(row, col)] = (math.floor(row / 3) * 3 + math.floor(col / 3), (row % 3) * 3 + (col % 3))

# Create, track and solve the Sudoku board 
class SudokuPuzzle():
    """Input, track and solve a Sudoku board"""

    def __init__(self, simple_board):
        """Takes a list of 9 lists of rows as an argument"""

        # Save original board state
        self.original_board = copy.deepcopy(simple_board)

        # Replace 0's with sets of {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for y, row in enumerate(simple_board):
            for x, col in enumerate(row):
                if col == 0:
                    simple_board[y][x] = set(range(1,10))

        # Prepare three representations of the Sudoku board
        self.rows    = [[0]*9 for _ in range(9)]
        self.cols    = [[0]*9 for _ in range(9)]
        self.regions = [[0]*9 for _ in range(9)] # indexed from left to right, and then top to bottom

        # Construct the three representations of the Sudoku board
        for y, row in enumerate(simple_board):
            for x, col in enumerate(row):
                self.rows[y][x] = col
                self.cols[x][y] = col
                self.regions[ ROW_TO_REGION[(y, x)][0] ][ ROW_TO_REGION[(y, x)][1] ] = col

    @property
    def board(self):
        return [self.rows, self.cols, self.regions]

    def update(self, x, y, value):
        """Update a cell at x, y with a given value, across all three board representations"""

        self.rows[y][x] = value
        self.cols[x][y] = value
        self.regions[ ROW_TO_REGION[(y, x)][0] ][ ROW_TO_REGION[(y, x)][1] ] = value

    def print_board(self, board = False):
        """Prints a sudoku board with filled numbers displayed."""

        if board is False:
            board = self.rows
        else:
            board = board

        for y in range(len(board)):
            row = ""

            for x in range(len(board[y])):
                if x % 3 == 0: # vertical borders
                    row += '| '
                if isinstance(board[y][x], int): # check if square is filled or blank
                    row += str(board[y][x]) + " "
                elif isinstance(board[y][x], set):
                    row += "  "
                else:
                    print(board[y][x])
                    raise TypeError("Excpected an int or set")

            row += '|' # rightmost vertical border

            if y == 0: # topmost horizontal border
                print('-' * len(row))
            elif y % 3 == 0:
                print(('+' + '-'*7 + '+').center(len(row), '-')) # horizontal borders
            print(row)

            if y == 8:
                print('-' * len(row)) # bottommost horizontal border

    def count_possibilities(self, board_rows):
        """Count total number of possibilities remaining on sudoku board"""
    
        total = 0
        for row in board_rows:
            for col in row:
                if isinstance(col, set) and len(col) > 1:
                    total += len(col)
        return total

    def check_error(self, board_rows):
        """Check for unique values in each row and column"""

        # Columns should not have repeating values
        col_values = {x:set() for x in range(0,9)}
        for y, row in enumerate(board_rows):
            # Rows should not have repeating values
            row_values = set()
            for x, col in enumerate(row):
                if isinstance(col, int):
                    if col in row_values or col in col_values[x]:
                        # Found a repeating value within the same row/column
                        return True
                    else:
                        row_values.add(col)
                        col_values[x].add(col)
        return False

    def check_complete(self, board_rows):
        """Check if the solution is complete"""

        # Check repeating numbers in rows and columns
        if self.check_error(board_rows) is True:
            return False

        # Check for nine occurences of each number
        int_dict = {number:0 for number in range(1,10)}    
        for row in board_rows:
            for col in row:
                if isinstance(col, int):
                    int_dict[col] += 1
                else:
                    return False

        if all(count == 9 for count in int_dict.values()):
            return True
        else:
            return False

    def apply_strategies(self, board):
        """Apply Sudoku strategies until no further possibilities can be eliminated"""
    
        starting_possibilities = self.count_possibilities(board.rows)

        while True:
            # Apply following Sudoku strategies functions for eliminating possibilities
            elim_row(board)
            elim_col(board)
            elim_3x3(board)

            fill_board(board)
            self.total_loops += 1

            ending_possibilities = self.count_possibilities(board.rows)

            if starting_possibilities == ending_possibilities:
                # No more progress can be made using current strategies
                return None
            else:
                starting_possibilities = ending_possibilities
            
            if self.check_error(board.rows) is True:
                # Error found in the solution
                return False

    def recursive_solve(self, board):
        """Use recursion (aka. DFS / trial and error) to find a solution"""

        for y, row in enumerate(board.rows):
            for x, col in enumerate(row):
                if isinstance(col, set):
                    # try each value in the set of possible numbers for a cell
                    for value in col:
                        print(f'{"*"*10} Trying {value} at position ({x+1},{9-y}) {"*"*10}')
                        temp_board = copy.deepcopy(board)
                        temp_board.update(x, y, value)
                        self.trials += 1
                        
                        if self.apply_strategies(temp_board) is False:
                            # if error is found, try next number in the set
                            continue
                        elif self.check_complete(temp_board.rows) is True:
                            # if solution is found, return the board
                            return temp_board
                        else:
                            complete_board = self.recursive_solve(temp_board)
                            if complete_board is not False:
                                # recursiveSolve() either returns False or the completed board
                                # if it does not return False, we have found the solution!
                                return complete_board

                    # if no possible values in the set works, this branch of the recursion has failed
                    return False

    def solve(self):
        """Solve the Sudoku board stored in self.board"""
        
        print("Starting board:")
        self.print_board(self.rows)

        # Initiate tracking attributes to 0
        self.total_loops         = 0
        self.pre_recursion_loops = 0
        self.trials              = 0

        # Solve Sudoku without trial and error, unless and until it gets stuck
        if self.apply_strategies(self) is None:
            if self.check_complete(self.rows) is False:
                self.pre_recursion_loops = self.total_loops
                print('Got this far without trial and error:')
                self.print_board(self.rows)
                print('Solving recursively using trial and error...')
                solved = copy.deepcopy(self.recursive_solve(self))
                # Update the current object instance with the solution
                for y, row in enumerate(solved.rows):
                    for x, value in enumerate(row):
                        self.update(x, y, value)

        if self.check_complete(self.rows) == True:
            self.print_board(self.rows)
            print('This solution is valid!')
            print(f'Non-recursion loops: {self.pre_recursion_loops}')
            print(f'Recursion loops: {self.total_loops - self.pre_recursion_loops}')
            print(f'Numbers of trials: {self.trials}')
        else:
            print('Check: Something is wrong.')
        return self.rows

easy   = SudokuPuzzle(easyBoard1)
medium = SudokuPuzzle(mediumBoard1)
hard   = SudokuPuzzle(hardBoard1)
evil   = SudokuPuzzle(evilBoard1)
worlds = SudokuPuzzle(worldsHardestBoard)

easy  .solve()
medium.solve()
hard  .solve()
evil  .solve()
worlds.solve()

print('\nHere\'s an example of the three different board representations:')
print('Rows:')
worlds.print_board(worlds.rows)
print('Columns:')
worlds.print_board(worlds.cols)
print('3x3 Regions:')
worlds.print_board(worlds.regions)
