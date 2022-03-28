#! python3
"""
Sukdoku solver that does NOT need recursion for most puzzles -> no backtracking or trial and error.

Solving strategies:
    - elim_placed_nums()    : eliminate possibilities based on solved numbers in the row, column or region
    - fill_one_possibility(): fill cells with only 1 possible number remaining
    - fill_only_location()  : fill a cell if it is the only cell in a row/col/region where it can go
    - elim_naked_chain()    : eliminate possibilities based on n cells that share same n possible numbers
    - elim_hidden_chain()   : eliminate possibilities based on n numbers that share the same n possible cell locations
    - elim_line_in_region() : unsolved numbers within a row/column whose only possible locations are in the same region
    - elim_region_in_line() : unsolved numbers within a region whose only possible locations are in the same row or column
Note, recursion is used if other strategies fail.

Class: SudokuBoard()
    Requires a Sudoku board (list of 9 lists of rows) to be passed as an argument at initiation
    .solve() method prints the solution using
"""
import copy, itertools

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

def elim_placed_nums(board_repr): # Single board of any representation
    """Eliminate possibilities that have already occured in the same row/column/region (depending on representation passed)"""

    for row in board_repr:
        eliminate = set([number for number in row if isinstance(number, int)])

        for col in row:
            if isinstance(col, set):
                col -= eliminate
                # check for an error
                if len(col) == 0:
                    return False

def fill_one_possibility(board):
    """Fill cells with only 1 possibility remaining"""
    
    for y, row in enumerate(board.rows):
        for x, col in enumerate(row):
            if isinstance(col, set) and len(col) == 1:
                board.update(x, y, col.pop())

def fill_only_location(board):
    """Fill the only cell in a row/col/region that has a set with the given number as a possibility"""

    # Rows
    for y, row in enumerate(board.rows):
        # Track locations in the row where each unsolved integer could potentially go
        locations = {num:set() for num in range(1,10)}
        for x, cell in enumerate(row):
            if isinstance(cell, set):
                for possibility in cell:
                    locations[possibility].add(x)
        # If there is only one possible location in the row, then we can place the integer there
        for num, locs in locations.items():
            if len(locs) == 1:
                board.update(next(iter(locs)), y, num)  # value[0] = x location, row = y location, key = number

    # Columns
    for x, col in enumerate(board.cols):
        # Track locations in the column where each unsolved integer could potentially go
        locations = {num:set() for num in range(1,10)}
        for y, cell in enumerate(col):
            if isinstance(cell, set):
                for possibility in cell:
                    locations[possibility].add(y)
        # If there is only one possible location in the column, then we can place the integer there
        for num, locs in locations.items():
            if len(locs) == 1:
                board.update(x, next(iter(locs)), num)  # value[0] = x location, row = y location, key = number

    # 3x3 Regions
    for r, region in enumerate(board.regions):
        # Track locations in the 3x3 region where each unsolved integer could potentially go
        locations = {num:set() for num in range(1,10)}
        for c, cell in enumerate(region):
            if isinstance(cell, set):
                for possibility in cell:
                    locations[possibility].add(c)
        # If there is only one possible location in the 3x3 region, then we can place the integer there
        for num, locs in locations.items():
            if len(locs) == 1:
                board.update( ROWS_TO_REGIONS[ (r, next(iter(locs))) ][1] , ROWS_TO_REGIONS[ (r, next(iter(locs))) ][0] , num )

def elim_naked_chain(board_repr, n):
    """Identify n cells that share some combination of the same n possible integers
        - e.g. Simplest variation (n=2), two cells in same row have same two possible integers
    Remove those n possible integers from the other cells in the same row, column or region
    """

    # Naked n-chain
    for row in board_repr:
        # Track all sets of size n or less as potential members of the chain
        potential_chain_members = []
        for chain_member in row:
            if isinstance(chain_member, set):
                if len(chain_member) <= n:
                    potential_chain_members.append(chain_member)
        # Skip if there are less than n potential chain members
        if len(potential_chain_members) < n:
            continue
        else:
        # Otherwise, test all combinations of potential chain members (cells) for a naked chain
            for combo in itertools.combinations(potential_chain_members, n):
                union = set().union(*combo) # Union all sets in the combination of cells
                if len(union) == n:
                    # Chain found! i.e. n possible numbers shared across n cells
                    # Remove these numbers as possibilities from other cells in same row/column/region
                    for cell in row:
                        if isinstance(cell, set) and not cell.issubset(union):
                            cell.difference_update(union) # Remove union elements from cell_

def elim_hidden_chain(board_repr, n):
    """Identify n numbers that must go in n cells and remove all other possibilities in those cells
        - e.g. n=2 -> two integers are only in two cells. The other possibilities in those cells are removed
    """
    for row in board_repr:
        # Track locations, i.e. indices, where each unsolved integer could potentially go in the row/column/region
        number_locations = {}
        for x, cell in enumerate(row):
            if isinstance(cell, set):
                for unsolved_number in cell:
                    number_locations.setdefault(unsolved_number, set())
                    number_locations[unsolved_number].add(x)
        # Skip if there are less than (or equal to) n unsolved integers in the row/column/region
        if len(number_locations) <= n:
            continue
        else:
        # Otherwise, test all combination of unsolved integers to find a hidden chain
            for combo in itertools.combinations(number_locations.items(), n):
                combo_numbers   = set(         [k for k, v in combo])
                combo_locations = set().union(*[v for k, v in combo]) # Union all possible locations for this combo
                if len(combo_locations) == n:
                    # Hidden chain found! i.e. these n numbers must go in these n locations
                    # Remove other numbers as possibilities from these locations
                    for x, cell in enumerate(row):
                        if x in combo_locations:
                            cell.intersection_update(combo_numbers) # Only keep numbers in combo_numbers

def elim_line_in_region(board):
    """Identify unsolved numbers within a row/column whose only two/three possible locations are within the same region
        - Remove those numbers as possibilities from the other cells in the region 
    """
    for y, row in enumerate(board.rows):
        # Track possible regions where each unsolved integer in the row could potentially go
        number_regions = {}
        for x, cell in enumerate(row):
            if isinstance(cell, set):
                for unsolved_number in cell:
                    number_regions.setdefault(unsolved_number, set())
                    number_regions[unsolved_number].add( ROWS_TO_REGIONS[ (y, x) ][0] ) # Identify region

        for k, v in number_regions.items():
            # Identify numbers whose possibilities are in the same region
            if len(v) == 1:
                region_index = v.pop()
                for c, cell in enumerate(board.regions[ region_index ]):
                    # Skip cells that are solved or are cells in the original row of interest:
                    if isinstance(cell, int) or ROWS_TO_REGIONS[ (region_index, c) ][0] == y:
                        continue
                    # Otherwise, remove the number from other cells in the region
                    else:
                        cell.discard(k)

    for x, col in enumerate(board.cols):
        # Track possible regions where each unsolved integer in the col could potentially go
        number_regions = {}
        for y, cell in enumerate(col):
            if isinstance(cell, set):
                for unsolved_number in cell:
                    number_regions.setdefault(unsolved_number, set())
                    number_regions[unsolved_number].add( ROWS_TO_REGIONS[ (y, x) ][0] ) # Identify region

        for k, v in number_regions.items():
            # Identify numbers whose possibilities are in the same region
            if len(v) == 1:
                region_index = v.pop()
                for c, cell in enumerate(board.regions[ region_index ]):
                    # Skip cells that are solved or are cells in the original col of interest:
                    if isinstance(cell, int) or ROWS_TO_REGIONS[ (region_index, c) ][1] == x:
                        continue
                    # Otherwise, remove the number from other cells in the region
                    else:
                        cell.discard(k)

def elim_region_in_line(board):
    """Identify unsolved numbers within a region whose only two/three possible locations are in a single row or column
        - Remove those numbers as possibilites from the rest of the respective row or column
    """
    for r, region in enumerate(board.regions):
        # Track possible rows and columns where each unsolved integer could potentially go
        number_rows = {}
        number_cols = {}
        for c, cell in enumerate(region):
            if isinstance(cell, set):
                for unsolved_number in cell:
                    number_rows.setdefault(unsolved_number, set())
                    number_cols.setdefault(unsolved_number, set())
                    number_rows[unsolved_number].add( ROWS_TO_REGIONS[ (r, c) ][0] ) # Identify row index
                    number_cols[unsolved_number].add( ROWS_TO_REGIONS[ (r, c) ][1] ) # Identify column index

        for k, v in number_rows.items():
            # Identify numbers whose possibilities are in the same row
            if len(v) == 1:
                row_index = v.pop()
                for c, cell in enumerate(board.rows[ row_index ]):
                    # Skip cells that are solved or are cells in the original region of interest:
                    if isinstance(cell, int) or ROWS_TO_REGIONS[ (row_index, c) ][0] == r:
                        continue
                    # Otherwise, remove the number from other cells in the row
                    else:
                        cell.discard(k)

                # Possibilities cannot also be in the same column
                number_cols.pop(k, None)

        for k, v in number_cols.items():
            # Identify numbers whose possibilities are in the same column
            if len(v) == 1:
                col_index = v.pop()
                for c, cell in enumerate(board.cols[ col_index ]):
                    # Skip cells that are solved or are cells in the original region of interest:
                    if isinstance(cell, int) or ROWS_TO_REGIONS[ (c, col_index) ][0] == r:
                        continue
                    # Otherwise, remove the number from other cells in the row
                    else:
                        cell.discard(k)

# Dictionary that maps a Sudoku board stored as lists of rows, to a board stored as lists of 3x3 regions
# The transformation actually works symmetrically in both directions:
    # Key: standard row-basis cell coordinates (y, x) -> Value: region-basis cell coordinates (region, cell)
    # Key: region-basis cell coordinates (region, cell) -> Value: standard row-basis cell coordinates (y, x)
ROWS_TO_REGIONS = {}
for row_or_region in range(9):
    for cell in range(9):
        ROWS_TO_REGIONS[(row_or_region, cell)] = ((row_or_region // 3) * 3 + (cell // 3), (row_or_region % 3) * 3 + (cell % 3))

# Example of row-basis indices:
    # [0] [1] [2] [3] [4] [5] [6] [7] [8]

# Example of 3x3 region-basis indices:
    # [0] [1] [2]
    # [3] [4] [5]
    # [6] [7] [8]

# Create, track and solve the Sudoku board 
class SudokuPuzzle():
    """Input, track and solve a 9x9 Sudoku board"""

    def __init__(self, simple_board):
        # Save the original board state
        self.original_board = copy.deepcopy(simple_board)

        # Track number of loops to solve
        self.total_loops = 0

        # Replace 0's with sets of {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for y, row in enumerate(simple_board):
            for x, col in enumerate(row):
                if col == 0:
                    simple_board[y][x] = set(range(1,10))

        self.rows    = [[0]*9 for _ in range(9)]
        self.cols    = [[0]*9 for _ in range(9)]
        self.regions = [[0]*9 for _ in range(9)] # indexed from left to right, and then top to bottom

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

    def count_possibilities(self, board_repr):
        """Count total number of possibilities remaining on sudoku board"""
    
        total = 0
        for row in board_repr:
            for col in row:
                if isinstance(col, set) and len(col) > 1:
                    total += len(col)
        return total

    def check_error(self, board_rows):
        """Check for unique values in each row and column
        Requires board.rows or board.cols representations
        Cannot use board.regions representation
        """

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
        """Check if the solution is complete
        Requires board.rows or board.cols representations
        Cannot use board.regions representation
        """

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

        # Eliminate possibilites based on numbers already placed on the board
        elim_placed_nums(board.rows)
        elim_placed_nums(board.cols)
        elim_placed_nums(board.regions)

        while True:
            # Apply following Sudoku strategies functions for eliminating possibilities
            fill_one_possibility(board)
            fill_only_location(board)
            elim_line_in_region(board)
            elim_region_in_line(board)
            for n in range(2, 6):
                elim_hidden_chain(board.rows   , n)
                elim_hidden_chain(board.cols   , n)
                elim_hidden_chain(board.regions, n)
            for n in range(2, 6):
                elim_naked_chain(board.rows   , n)
                elim_naked_chain(board.cols   , n)
                elim_naked_chain(board.regions, n)

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
        
        print("\nStarting board:")
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
                print(f'Possibilities remaining: {self.count_possibilities(self.rows)}')
                print('Solving recursively using trial and error...')
                solved = copy.deepcopy(self.recursive_solve(self))
                # Update the current object instance with the solution
                for y, row in enumerate(solved.rows):
                    for x, value in enumerate(row):
                        self.update(x, y, value)
            else:
                self.pre_recursion_loops = self.total_loops
                print('No recursion/backtracking needed!')
        
        if self.check_complete(self.rows) == True:
            self.print_board(self.rows)
            print('This solution is valid!')
            print(f'Loops to solve: {self.total_loops}')
            print(f'Loops during recursion: {self.total_loops - self.pre_recursion_loops}')
            print(f'Numbers of guesses: {self.trials}')
        else:
            print('Check: Something is wrong.')
            self.print_board(self.rows)
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
