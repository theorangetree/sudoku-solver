#! python3
"""
Basic Sukdoku solver that uses recursion.

Solving strategies:
    - elim_row(): eliminate possibilities based on existing numbers in the row
    - elim_col(): eliminate possibilities based on existing numbers in the column
    - elim_3x3(): eliminate possibilities based on existing numbers in the 3x3
    - fill_board(): input a value in a cell if there is only one remaining possibility for that cell

Class: SudokuBoard()
    Requires a Sudoku board to be passed as an argument at initiation
    This class contains utility methods and the solve() method, which solves self.board
"""

# Import modules
import copy

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
# Remember, a blank board is 9 lists of 9 sets, each containing the possible numbers 1 to 9

def elim_row(board):
    """Eliminate possibilities that have already occured in the same row"""

    for row in board:
        eliminate = set([col for col in row if isinstance(col, int)])

        for col in row:
            if isinstance(col, set):
                col -= eliminate
                # check for an error
                if len(col) == 0:
                    return False

def elim_col(board):
    """Eliminate possibilities that have already occured in the same column"""

    for col in range(9):
        eliminate = set()
        for row in range(9):
            if isinstance(board[row][col], int):
                eliminate.add(board[row][col])

        for row in range(9):
            if isinstance(board[row][col], set):
                board[row][col] -= eliminate
                # check for an error
                if len(board[row][col]) == 0:
                    return False

def elim_3x3(board):
    """Eliminate possibilities that have already occured in the same 3x3 square"""

    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            eliminate = set()

            for row3x3 in [0, 1, 2]:
                for col3x3 in [0, 1, 2]:
                    if isinstance(board[row + row3x3][col + col3x3], int):
                        eliminate.add(board[row + row3x3][col + col3x3])

            for row3x3 in [0, 1, 2]:
                for col3x3 in [0, 1, 2]:
                    
                    if isinstance(board[row + row3x3][col + col3x3], set):
                        board[row + row3x3][col + col3x3] -= eliminate
                        # check for an error
                        if len(board[row + row3x3][col + col3x3]) == 0:
                            return False

def fill_board(board):
    """Fill squares with only 1 possibility remaining"""
    
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if isinstance(col, set) and len(col) == 1:
                board[y][x] = col.pop()

# Create and solve the sudoku board
class SukokuBoard():
    """ Create a sudoku board with utility and solver methods

    Utility functions:
        - print_board()
        - count_possibilities()
        - check_error()
        - check_complete()
    Solving functions:
        - apply_strategies() - solve using the deductive strategies Sudoku until stuck
        - recursive_solve() - use trial and error to guess through possibilities
        - solve() - method that calls the other solving functions
    """
    def __init__(self, board = []):
        self.board = board # board with 9 rows of 9 cells, each containing a set of 9 possibilities
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col == 0:
                    self.board[y][x] = set(range(1,10))
        self.original_board = copy.deepcopy(self.board)

    def print_board(self, board):
        """Prints a sudoku board with filled numbers displayed."""

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

    def count_possibilities(self, board):
        """Count total number of possibilities remaining on sudoku board"""
    
        total = 0
        for row in board:
            for col in row:
                if isinstance(col, set) and len(col) > 1:
                    total += len(col)
        return total       

    def check_error(self, board):
        """Check for unique values in each row and column"""

        # Columns should not have repeating values
        col_values = {x:set() for x in range(0,9)}
        for y, row in enumerate(board):
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

    def check_complete(self, board):
        """Check if the solution is complete"""

        # Check repeating numbers in rows and columns
        if self.check_error(board) is True:
            return False

        # Check for nine occurences of each number
        int_dict = {number:0 for number in range(1,10)}    
        for row in board:
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
    
        starting_possibilities = self.count_possibilities(board)
        while True:
            # Add below all Sudoku strategy functions for eliminating possibilities
            elim_row(board)
            elim_col(board)
            elim_3x3(board)

            fill_board(board)

            self.total_loops += 1

            ending_possibilities = self.count_possibilities(board)

            if starting_possibilities == ending_possibilities:
                # No more progress can be made using current strategies
                return None
            else:
                starting_possibilities = ending_possibilities
            
            if self.check_error(board) is True:
                # Error found in the solution
                return False

    def recursive_solve(self, board):
        """Use recursion (aka. DFS / trial and error) to find a solution"""

        for y, row in enumerate(board):
            for x, col in enumerate(row):
                if isinstance(col, set):
                    # try each value in the set of possible numbers for a cell
                    for value in col:
                        print(f'{"*"*10} Trying {value} at position ({x+1},{9-y}) {"*"*10}')
                        temp_board = copy.deepcopy(board)
                        temp_board[y][x] = value
                        self.trials += 1
                        
                        if self.apply_strategies(temp_board) is False:
                            # if error is found, try next number in the set
                            continue
                        elif self.check_complete(temp_board) is True:
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
        self.print_board(self.board)

        # Initiate tracking attributes to 0
        self.total_loops        = 0
        self.pre_recursion_loops = 0
        self.trials             = 0

        # Solve Sudoku without trial and error, unless and until it gets stuck
        if self.apply_strategies(self.board) is None:
            if self.check_complete(self.board) is False:
                self.pre_recursion_loops = self.total_loops
                print('Got this far without trial and error:')
                self.print_board(self.board)
                print('Solving recursively using trial and error...')
                self.board = copy.deepcopy(self.recursive_solve(self.board))
                self.print_board(self.board)

        if self.check_complete(self.board) == True:
            print('This solution is valid!')
            print(f'Non-recursion loops: {self.pre_recursion_loops}')
            print(f'Recursion loops: {self.total_loops - self.pre_recursion_loops}')
            print(f'Numbers of trials: {self.trials}')
        else:
            print('Check: Something is wrong.')
        return self.board

easy   = SukokuBoard(easyBoard1)
medium = SukokuBoard(mediumBoard1)
hard   = SukokuBoard(hardBoard1)
evil   = SukokuBoard(evilBoard1)
worlds = SukokuBoard(worldsHardestBoard)

easy  .solve()
medium.solve()
hard  .solve()
evil  .solve()
worlds.solve()
