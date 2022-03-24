#! python3
"""
Sukdoku solver that does NOT need recursion -> no backtracking or trial and error.

Solving strategies:
    - elim_row(): eliminate possibilities based on existing numbers in the row
    - elim_col(): eliminate possibilities based on existing numbers in the column
    - elim_3x3(): eliminate possibilities based on existing numbers in the 3x3
    - ...
    - fill_board(): input a value in a cell if there is only one remaining possibility for that cell

Class: SudokuBoard()
    Requires a Sudoku board (list of 9 lists of rows) to be passed as an argument at initiation
    This class contains utility methods and the solve() method, which solves self.rows, self.cols, self.regions
"""

# Import modules
import copy, math, itertools, numpy

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

def fillRow(board):
# fill in spaces by looking at rows
	print("fillRow")

	boxWing   = {}
	swordfish = {}

	for y in range(9):

		# find the possible locations for numbers missing from a row.
		# locations[0] lists all possible locations along the row (left to right) for the number 1.
		locations = [''] * 9											# locations = ['index positions of 1', 'index positions of 2', ...]
		for x in range(9):
			if type(board[y][x]) == list:
				for z in board[y][x]:
					locations[int(z) - 1] += str(x)						# str(x) is a possible column index
			else:
				continue;
		print("locations")
		print(locations)

		# eliminate already inputted numbers from the locations list
		for x in range(9):
			if type(board[y][x]) == str:
				locations[int(board[y][x]) - 1] = ''
			else:
				continue;

		# COMPLEX STUFF!
		check2 = {}														# key = possible locations, value = digit candidates for the locations
		# identify numbers with 2 possible locations
		for i in range(9):
			if len(locations[i]) == 2:
				check2.setdefault(locations[i], '')
				check2[locations[i]] += str(i + 1)
		# find pairs of 2 spaces to pseudo-fill
		for k in check2.keys():
			if len(check2[k]) == 2:
				for i in range(2):
					for num in board[y][int(k[i])]:
						if num not in check2[k]:
							board[y][int(k[i])].remove(num)
			# if the pair exists in the same 3x3 square, remove them as possibilities from the rest of the 3x3 square
			if (int(k[0]) // 3) == (int(k[1]) // 3):
				for i in range(9):
					if i != (int(k[0]) % 3 + (y % 3) * 3) and i != (int(k[1]) % 3 + (y % 3) * 3):
						if type(board[(y // 3) * 3 + i // 3][(int(k[0]) // 3) * 3 + i % 3]) == list:
							for j in range(len(check2[k])):
								try:
									board[(y // 3) * 3 + i // 3][(int(k[0]) // 3) * 3 + i % 3].remove(check2[k][j])
								except:
									continue;

		print("check2")
		print(check2)
		
		# identify 2 spaces with 2 of the same possible numbers
		#http://www.sudokudragon.com/sudokustrategy.htm
		#http://www.sudokudragon.com/advancedstrategy.htm
		#http://www.websudoku.com/?level=4 Evil Puzzle 391,101,148
		
		# psuedo-fill 3 uncertain squares. This can be achieved in 4 ways:
		# 	1) 3 3 length locations in the same spot
		#	2) 2 3 length, 1 2 length locations in a triangle
		#	3) 1 3 length, 2 2 length locations in a triangle
		#	4) 0 3 length, 3 2 length locations in a triangle
		def psuedoFill3(key):
			for i in range(3):
				for num in board[y][int(key[i])]:
					# remove extra possibilities
					if num not in check3[key]:
						board[y][int(key[i])].remove(num)

		check3  = {}													# key = possible locations, value = digit candidates for the locations
		triFill = []
		for i in range(9):
			if len(locations[i]) == 3:
				check3.setdefault(locations[i], '')
				check3[locations[i]] += str(i + 1)
			else:
				continue;

		# Psuedo-fill 3 in the 4 different ways
		for k in check3.keys():
			if len(check3[k]) == 3:
				psuedoFill3(k)

			elif len(check3[k]) == 2:
				for two in check2.keys():
					if two in k:
						for digit in check2[two]:
							if digit not in check3[k]:
								check3[k] += digit
						psuedoFill3(k)

			elif len(check3[k]) == 1:
				for two in check2.keys():
					if two in k:
						for digit in check2[two]:
							if digit not in check3[k]:
								check3[k] += digit
						if len(check3[k]) == 3:
							psuedoFill3(k)

			elif len(check2) >= 3:
				for h in range(len(check2)):
					for i in range(len(check2)):
						for j in range(len(check2)):
							new3Key   = ''
							new3Value = ''
							if h != i and h != j and i != j and			\
							h[0] in i and h[1] in j and					\
							(i[0] in j or i[1] in j):
								def adjoin3(w,x,y,z):
									temp = ''
									temp += w + x + y
									for char in temp:
										if char not in z:
											new3Key += char
								adjoin3(h, i, j, new3Key)
								adjoin3(check2[h], check2[i], check2[j], new3Value)
								check3.setdefault(new3Key, new3Value)
								psuedoFill3(new3Key)

			else:
				print("Some sort of error in psuedo-fill 3 for fillRow")

		# fill spaces that contain the only possible location for a number in the row
		for i in range(9):
			if len(locations[i]) == 1:
				board[y][int(locations[i])] = str(i + 1)
			else:
				continue;

def old_hidden_twins(board):
    """Identify twins (two numbers that must go in two cells) and remove possibilties:
        - Other possibilities in the twin cells
        - Twin possibilities from other cells in same row, column, and/or region
    """
    

    # Hidden twins
    for y, row in enumerate(board.rows):
        # Track locations in the row where each unsolved integer could potentially go
        locations = {num:set() for num in range(1,10)}
        for x, cell in enumerate(row):
            if isinstance(cell, set):
                for possibility in cell:
                    locations[possibility].add(x)

        # Check if a number shares its two possible locations with another number
        for num, locs in locations.items():
            if len(locs) == 2:
                # Check if there is another number with the same locations
                count = 0
                for value in locations.values():
                    if locs == value:
                        count +=1
                if count == 2:
                    for cell in row:
                        if isinstance(cell, set) and locations[num] != locs:
                            cell.discard(nums)

# TO DO:
# Sub group exclusion (remove from other 3x3 grid spaced if it has to go in a row)
# DONE Twins (remove other posibilities in the twin square, and the twins from other squares in row/col/3x3)
    # Hidden twins didn't seem to make a difference but naked twins looks good
# DONE Triplets
# Same as twins but for n-number chains
# X-Wing (aka. box) for a box where two of the same numbers must be on opposite corners of an X-Wing
    # Identified by finding two rows where a number has pairs on top of each other (same for columns)
# Swordfish
    # Identified by finding three rows where a number has pairs (same for columns); numbers in the linking columns (rows) can be eliminated
# Alternate pairs - general rule for X-Wing and Swordfish
    # Different colours in the same col/row/region allow for eliminating all others of the same number in that col/row/region
# Alternate pairs (multi-colour) - eliminate numbers that are in the intersection of multi-coloured pairs)
# Hook - [x,y][y,z][z,x] 3 pairs, two cells in the same row and two in cells in the same region
    # Allows us to eliminate the cells in possibility from the intersect cell that is not in the same row/col

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
    """Fill squares with only 1 possibility remaining"""
    
    for y, row in enumerate(board.rows):
        for x, col in enumerate(row):
            if isinstance(col, set) and len(col) == 1:
                board.update(x, y, col.pop())

def fill_only_location(board):
    """Fill the only square in a row/col/region that has a set with the given number as a possibility"""

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

def elim_twins(board_repr):
    """Identify twins (two numbers that must go in two cells) and remove possibilties:
        - i.e. remove twin possibilities from other cells in same row, column, or region
    """
    
    # Naked twins
    for row in board_repr:
        for pair in row:
            if isinstance(pair, set):
                # Identify twins
                if len(pair) == 2 and row.count(pair) == 2:
                    # Twin found! Remove twins as possibilities from other cells in same row/column/region
                    for cell_ in row:
                        if isinstance(cell_, set) and cell_ != pair:
                            cell_.difference_update(pair) # Remove pair elements from cell_

def elim_triplets(board_repr):
    """Identify three cells that share some combination of the same three possibilities and remove possibilities:
        - i.e. remove triplet possibilities from other cells in same row, column or region
    """

    # Naked triplets
    for row in board_repr:
        # Track all pair and triple possibilities as potential members of a triplet
        potential_triplets = []
        for pair_or_triple in row:
            if isinstance(pair_or_triple, set):
                if len(pair_or_triple) == 2 or len(pair_or_triple) == 3:
                    potential_triplets.append(pair_or_triple)
        # Skip if there are less than three pairs and/or triples
        if len(potential_triplets) < 3:
            continue
        else:
        # Otherwise, test all combinations of pair/triple-cells for a potential triplet
            for t1, t2, t3 in itertools.combinations(potential_triplets, 3):
                union = t1 | t2 | t3
                if len(union) == 3:
                    # Triplet found! i.e. three possible numbers shared across three cells
                    # Remove these numbers as possibilities from other cells in same row/column/region
                    for cell_ in row:
                        if isinstance(cell_, set) and not cell_.issubset(union):
                            cell_.difference_update(union) # Remove union elements from cell_

def elim_n_chain(board_repr, n):
    """Identify n cells that share some combination of the same n possible integers
        - e.g. Simplest variation (n=2), two cells in same row have same two possible integers
    Remove those n possible integers from the other cells in the same row, column or region
    """

    # Naked triplets
    for row in board_repr:
        # Track all pair and triple possibilities as potential members of a triplet
        potential_chain_members = []
        for chain_member in row:
            if isinstance(chain_member, set):
                if len(chain_member) <= n:
                    potential_chain_members.append(chain_member)
        # Skip if there are less than three pairs and/or triples
        if len(potential_chain_members) < n:
            continue
        else:
        # Otherwise, test all combinations of pair/triple-cells for a potential triplet
            for combo in itertools.combinations(potential_chain_members, n):
                union = set().union(*combo) # Union all sets in the combination of cells
                if len(union) == n:
                    # Chain found! i.e. n possible numbers shared across n cells
                    # Remove these numbers as possibilities from other cells in same row/column/region
                    for cell_ in row:
                        if isinstance(cell_, set) and not cell_.issubset(union):
                            cell_.difference_update(union) # Remove union elements from cell_


# Dictionary that maps a Sudoku board stored as lists of rows, to a board that's lists of 3x3 regions
# The transformation actually works in both directions:
    # Key: standard row-basis cell coordinates (y, x) -> Value: region-basis cell coordinates (region, cell)
    # Key: region-basis cell coordinates (region, cell) -> Value: standard row-basis cell coordinates (y, x)
ROWS_TO_REGIONS = {}
for row_or_region in range(9):
    for cell in range(9):
        ROWS_TO_REGIONS[(row_or_region, cell)] = (math.floor(row_or_region / 3) * 3 + math.floor(cell / 3), (row_or_region % 3) * 3 + (cell % 3))

# Example of row-basis indices:
    # [0] [1] [2] [3] [4] [5] [6] [7] [8]

# Example of 3x3 region-basis indices:
    # [0] [1] [2]
    # [3] [4] [5]
    # [6] [7] [8]

print(ROWS_TO_REGIONS)
import pprint as pp

# Create, track and solve the Sudoku board 
class SudokuPuzzle():
    """Input, track and solve a Sudoku board"""

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

    @property
    def board(self):
        return [self.rows, self.cols, self.regions]

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

            for n in range(2, 6):
                elim_n_chain(board.rows, n)
                elim_n_chain(board.cols, n)
                elim_n_chain(board.regions, n)

            

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
                pp.pprint(self.rows)
                print('break')
                pp.pprint(self.cols)
                print('break')
                pp.pprint(self.regions)
                print(f'Possibilities: {self.count_possibilities(self.rows)}')
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
            print(f'Loops before recursion: {self.pre_recursion_loops}')
            print(f'Recursion loops: {self.total_loops - self.pre_recursion_loops}')
            print(f'Numbers of trials: {self.trials}')
        else:
            print('Check: Something is wrong.')
            self.print_board(self.rows)
        return self.rows

easy   = SudokuPuzzle(easyBoard1)
medium = SudokuPuzzle(mediumBoard1)
hard   = SudokuPuzzle(hardBoard1)
evil   = SudokuPuzzle(evilBoard1)
worlds = SudokuPuzzle(worldsHardestBoard)
"""
easy.apply_strategies(easy)
easy.print_board(easy.rows)
pp.pprint(easy.rows)

medium.apply_strategies(medium)
medium.print_board(medium.rows)
hard.apply_strategies(hard)
hard.print_board(hard.rows)
evil.apply_strategies(evil)
evil.print_board(evil.rows)
worlds.apply_strategies(worlds)
worlds.print_board(worlds.rows)
"""

easy  .solve()
medium.solve()
hard  .solve()
evil  .solve()
worlds.solve()
