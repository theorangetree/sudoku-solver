#! python3
"""
Sukdoku solver that solves without backtracking (trial and error) unless needed

See board.py      -> for details on the SudokuPuzzle object
See strategies.py -> for details on non-recursive solving strategies
"""
from board import SudokuPuzzle

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

def main():
    """Solve some puzzles!"""
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

if __name__ == '__main__':
    main()
