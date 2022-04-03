#! python3
"""
Sudoku solving strategies:
    - fill_one_possibility(board)     : fill cells with only 1 possible number remaining
    - fill_only_location(board)       : fill a cell if it is the only cell in a row/col/region where a number can go
    - elim_placed_nums(board_repr)    : eliminate possibilities based on solved numbers in the row, column or region
    - elim_naked_chain(board_repr, n) : eliminate possibilities based on n cells that share same n possible numbers
    - elim_hidden_chain(board_repr, n): eliminate possibilities based on n numbers that share the same n possible cell locations
    - elim_line_in_region(board)      : unsolved numbers within a row/column whose only possible locations are in the same region
    - elim_region_in_line(board)      : unsolved numbers within a region whose only possible locations are in the same row or column

board     : refers to the SudokuBoard object
board_repr: refers to one of three board representations (i.e. board.rows, board.cols, or board.regions)
"""
import itertools

def row_to_region_map():
    """Create dictionary that maps a Sudoku board stored as lists of rows, to a board stored as lists of 3x3 regions

    The transformation actually works symmetrically in both directions:
        Key: standard row-basis cell coordinates (y, x) -> Value: region-basis cell coordinates (region, cell)
        Key: region-basis cell coordinates (region, cell) -> Value: standard row-basis cell coordinates (y, x)

    Example of row-basis indices:
        [0] [1] [2] [3] [4] [5] [6] [7] [8]

    Example of 3x3 region-basis indices:
        [0] [1] [2]
        [3] [4] [5]
        [6] [7] [8]
    """
    rtr_map = {}
    for row_or_region in range(9):
        for cell in range(9):
            rtr_map[(row_or_region, cell)] = ((row_or_region // 3) * 3 + (cell // 3), (row_or_region % 3) * 3 + (cell % 3))

    return rtr_map

ROWS_TO_REGIONS = row_to_region_map()

# Solving strategies

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

def elim_placed_nums(board_repr): # Single board of any representation
    """Eliminate possibilities that have already occured in the same row/column/region (depending on representation passed)"""

    for row in board_repr:
        eliminate = {number for number in row if isinstance(number, int)}

        for col in row:
            if isinstance(col, set):
                col -= eliminate

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
        # Otherwise, test all combinations of potential chain members (cells) for a naked chain
        if len(potential_chain_members) >= n:
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
        # Otherwise, test all combinations of unsolved integers for a hidden chain
        if len(number_locations) > n:
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
                    # Remove the number as a possiblility from unsolved cells in the region
                    # Ignore cells that are in the original row of interest
                    if isinstance(cell, set) and ROWS_TO_REGIONS[ (region_index, c) ][0] != y:
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
                    # Remove the number as a possiblility from unsolved cells in the region
                    # Ignore cells that are in the original column of interest
                    if isinstance(cell, set) and ROWS_TO_REGIONS[ (region_index, c) ][1] != x:
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
                    # Remove the number as a possibility from unsolved cells in the row
                    # Ignore cells that are in the original region of interest
                    if isinstance(cell, set) and ROWS_TO_REGIONS[ (row_index, c) ][0] != r:
                        cell.discard(k)

                # Possibilities cannot also be in the same column
                number_cols.pop(k, None)

        for k, v in number_cols.items():
            # Identify numbers whose possibilities are in the same column
            if len(v) == 1:
                col_index = v.pop()
                for c, cell in enumerate(board.cols[ col_index ]):
                    # Remove the number as a possibility from unsolved cells in the column
                    # Ignore cells that are in the original region of interest
                    if isinstance(cell, set) and ROWS_TO_REGIONS[ (c, col_index) ][0] != r:
                        cell.discard(k)
