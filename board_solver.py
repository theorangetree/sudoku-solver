#! python3
"""
Class: SudokuBoard()
    Takes a 9x9 board as an argument (represented as a list of 9 lists/rows with 9 cells each)
        - 0 represents an empty cell, while numbers 1-9 are solved cells

    The SudokuBoard.solve() method will:
        - print the solution
        - print the number of loops needed using strategies in strategies.py
        - print whether trial and error (through recursion) was needed
"""
import copy
import strategies

# Dictionary that maps a Sudoku board stored as lists of rows, to a board stored as lists of 3x3 regions
# The transformation actually works symmetrically in both directions:
    # Key: standard row-basis cell coordinates (y, x) -> Value: region-basis cell coordinates (region, cell)
    # Key: region-basis cell coordinates (region, cell) -> Value: standard row-basis cell coordinates (y, x)
ROWS_TO_REGIONS = strategies.row_to_region_map()

def count_possibilities(board_repr):
    """Count total number of possibilities remaining on sudoku board"""
    total = 0
    for row in board_repr:
        for col in row:
            if isinstance(col, set) and len(col) > 1:
                total += len(col)
    return total

def check_error(board):
    """Check for unique values in each row, column, and region"""
    # Columns should not have repeating values
    col_values = {x:set() for x in range(0,9)}
    for row in board.rows:
        # Rows should not have repeating values
        row_values = set()
        for x, col in enumerate(row):
            if isinstance(col, int):
                if col in row_values or col in col_values[x]:
                    # Found repeating value within the same row or column
                    return True
                row_values.add(col)
                col_values[x].add(col)

    for region in board.regions:
        # Regions should not have repeating values
        region_values = set()
        for cell in region:
            if isinstance(cell, int):
                if cell in region_values:
                    # Found repeating value with the same region
                    return True
                region_values.add(cell)

    return False

def check_complete(board):
    """Check if board contains valid solution"""
    # Check for repeating numbers in rows and columns
    if check_error(board) is True:
        return False

    # Check for nine occurences of each number
    int_dict = {number:0 for number in range(1,10)}
    for row in board.rows:
        for col in row:
            if not isinstance(col, int):
                return False
            int_dict[col] += 1

    return bool( all(count == 9 for count in int_dict.values()) )

class SudokuPuzzle():
    """Input, track and solve a 9x9 Sudoku board"""

    def __init__(self, simple_board):
        # Save the original board state
        self.original_board = copy.deepcopy(simple_board)

        # Initiate tracking attributes to 0
        self.total_loops         = 0 # Loops to solve
        self.pre_recursion_loops = 0 # Loops before recursion
        self.trials              = 0 # Guesses

        # Replace 0's with sets of {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for y, row in enumerate(simple_board):
            for x, col in enumerate(row):
                if col == 0:
                    simple_board[y][x] = set(range(1,10))

        self.rows    = [[0]*9 for _ in range(9)]
        self.cols    = [[0]*9 for _ in range(9)]
        self.regions = [[0]*9 for _ in range(9)] # Indexed from left to right, and then top to bottom

        # Construct the three representations of the Sudoku board
        for y, row in enumerate(simple_board):
            for x, col in enumerate(row):
                self.rows[y][x] = col
                self.cols[x][y] = col
                self.regions[ ROWS_TO_REGIONS[(y, x)][0] ][ ROWS_TO_REGIONS[(y, x)][1] ] = col

    def update(self, x, y, value):
        """Update a cell at indices (x, y) with a given value, across all three board representations
        Remove that value as a possibility from cells in the same row/column/region
        """
        # Update value
        self.rows[y][x] = value
        self.cols[x][y] = value
        self.regions[ ROWS_TO_REGIONS[(y, x)][0] ][ ROWS_TO_REGIONS[(y, x)][1] ] = value

        # Remove possibilities from row
        for cell in self.rows[y]:
            if isinstance(cell, set):
                cell.discard(value)
        # Remove possiblities from column
        for cell in self.cols[x]:
            if isinstance(cell, set):
                cell.discard(value)
        # Remove possibilites from 3x3 region
        for cell in self.regions[ ROWS_TO_REGIONS[(y, x)][0] ]:
            if isinstance(cell, set):
                cell.discard(value)

    def print_board(self, board = False):
        """Prints a sudoku board with filled numbers displayed."""
        if board is False:
            board = self.rows

        for y in range(9):
            row = ""

            for x in range(9):
                if x % 3 == 0: # vertical borders
                    row += '| '
                if isinstance(board[y][x], int): # check if square is filled or blank
                    row += str(board[y][x]) + " "
                elif isinstance(board[y][x], set):
                    row += "  "
                else:
                    raise TypeError("Excpected an int or set")

            row += '|' # rightmost vertical border

            if y == 0: # topmost horizontal border
                print('-' * len(row))
            elif y % 3 == 0:
                print(('+' + '-'*7 + '+').center(len(row), '-')) # horizontal borders
            print(row)

            if y == 8:
                print('-' * len(row)) # bottommost horizontal border

    def apply_strategies(self, board):
        """Apply Sudoku strategies until no further possibilities can be eliminated"""

        starting_possibilities = count_possibilities(board.rows)

        # Eliminate possibilites based on numbers already placed on the board
        strategies.elim_placed_nums(board.rows)
        strategies.elim_placed_nums(board.cols)
        strategies.elim_placed_nums(board.regions)
        while True:
            # Apply Sudoku solving strategies defined in strategies.py
            strategies.fill_one_possibility(board)
            strategies.fill_only_location(board)
            strategies.elim_line_in_region(board)
            strategies.elim_region_in_line(board)
            for n in range(2, 6):
                strategies.elim_hidden_chain(board.rows   , n)
                strategies.elim_hidden_chain(board.cols   , n)
                strategies.elim_hidden_chain(board.regions, n)
            for n in range(2, 6):
                strategies.elim_naked_chain(board.rows   , n)
                strategies.elim_naked_chain(board.cols   , n)
                strategies.elim_naked_chain(board.regions, n)
            self.total_loops += 1

            # Check for progress and errors in the solution
            ending_possibilities = count_possibilities(board.rows)
            if starting_possibilities == ending_possibilities:
                # No more progress can be made using current strategies
                return None
            starting_possibilities = ending_possibilities

            if check_error(board) is True:
                # Error found in the solution
                return False

    def recursive_solve(self, board):
        """Use recursion (aka. DFS / trial and error) to find a solution
        Guesses in cells with the least possibilities first
        """

        # Sort unsolved cells by least number of possibilities
        unsolved_cells = []
        for y, row in enumerate(board.rows):
            for x, cell in enumerate(row):
                if isinstance(cell, set):
                    unsolved_cells.append( ( cell, y, x ) )
        unsolved_cells.sort(key=lambda x: len(x[0]))

        # Try possibilities
        for cell, y, x in unsolved_cells:
            for value in cell:
                print(f'{"*"*10} Trying {value} at position ({x+1},{9-y}) {"*"*10}')
                temp_board = copy.deepcopy(board)
                temp_board.update(x, y, value)
                self.trials += 1

                if self.apply_strategies(temp_board) is False:
                    # If error is found, try next number in the set
                    continue
                elif check_complete(temp_board) is True:
                    # If solution is found, return the board
                    return temp_board
                else:
                    complete_board = self.recursive_solve(temp_board)
                    if complete_board is not False:
                        # recursive_solve() either returns False or the completed board
                        # If it does not return False, we have found the solution!
                        return complete_board

            # If no possible values in the set works, this branch of the recursion has failed
            return False

    def solve(self):
        """Solve the Sudoku board stored in self.board"""

        print("\nStarting board:")
        self.print_board(self.rows)

        # Solve Sudoku without trial and error, unless and until it gets stuck
        if self.apply_strategies(self) is None:
            if check_complete(self) is False:
                self.pre_recursion_loops = self.total_loops
                print('Got this far without trial and error:')
                self.print_board(self.rows)
                print(f'Possibilities remaining: {count_possibilities(self.rows)}')
                print('Solving recursively using trial and error...')
                solved = copy.deepcopy(self.recursive_solve(self))
                # Update the current object instance with the solution
                for y, row in enumerate(solved.rows):
                    for x, value in enumerate(row):
                        self.update(x, y, value)
            else:
                self.pre_recursion_loops = self.total_loops
                print('No recursion/backtracking needed!')

        self.print_board(self.rows)
        print(f'Loops to solve: {self.total_loops}')
        print(f'Loops during recursion: {self.total_loops - self.pre_recursion_loops}')
        print(f'Numbers of guesses: {self.trials}')

        return self.rows
