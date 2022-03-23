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
# Remember, a blank board is 9 lists of 9 sets, each containing the possible numbers 1 to 9


# TO DO:
# Sub group exclusion (remove from other 3x3 grid spaced if it has to go in a row)
# Twin (remove other posibilities in the twin square, and the twins from other squares in row/col/3x3)
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

"""
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
"""
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

# Dictionary that maps a Sudoku board stored as lists of rows, to a board that's lists of 3x3 regions
# Key: standard-basis cell coordinates -> Value: region-basis cell coordinates
ROW_TO_REGION = {}
for row in range(9):
    for col in range(9):
        ROW_TO_REGION[(row, col)] = (math.floor(row / 3) * 3 + math.floor(col / 3), (row % 3) * 3 + (col % 3))
# Example of 3x3 region-basis indices:
    # [0] [1] [2]
    # [3] [4] [5]
    # [6] [7] [8]

print(ROW_TO_REGION)

# Create, track and solve the Sudoku board 
class Board():
    """Input, track and solve a Sudoku board"""

    def __init__(self, simple_board):
        # Save the original board state
        self.original_board = copy.deepcopy(simple_board)

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
worlds.print_board(worlds.rows)
worlds.print_board(worlds.cols)
worlds.print_board(worlds.regions)
