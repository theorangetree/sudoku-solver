#! python3
"""
Solve random board generated on nine.websudoku.com

See board_solver.py -> for details on the SudokuPuzzle object
See strategies.py   -> for details on non-recursive solving strategies
See main.py         -> for examples of the solver working in Pythoon
"""
import requests
from bs4 import BeautifulSoup
from board_solver import SudokuPuzzle

def solve_random_online_board(level=4):
    """Web scrape and solve a random sudoku board from nine.websudoku.com"""
    # Available difficulty levels
    difficulty = {1: 'EASY', 2: 'MEDIUM', 3: 'HARD', 4: 'EVIL'}

    # Retrieve HTML text
    url  = f'https://nine.websudoku.com/?level={level}'
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')

    # Input starting values from HTML text onto a board (list of lists)
    board = [[0]*9 for _ in range(9)]
    for cell in soup.find_all('table')[3].find_all('input'):
        try:
            x = int(cell['id'][1])
            y = int(cell['id'][2])
            board[y][x] = int(cell['value'])
        except KeyError:
            pass

    # Solve the given board
    print(f'Solving {difficulty[level]} Sudoku board from {url}')
    sudoku_solver = SudokuPuzzle(board)
    sudoku_solver.solve()

if __name__ == '__main__':
    solve_random_online_board()
