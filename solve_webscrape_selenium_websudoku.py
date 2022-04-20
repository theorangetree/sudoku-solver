#! python3
"""
Solve random board generated on nine.websudoku.com

See board_solver.py        -> for details on the SudokuPuzzle object
See strategies.py          -> for details on non-recursive solving strategies
See solve_preset_boards.py -> for examples of the solver working in Pythoon
"""
import time
from selenium import webdriver # Location of chromedriver.exe
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from board_solver import SudokuPuzzle

def solve_random_browser_board(level=4):
    """Solve a Sudoku on nine.websudoku.com in Chrome using Selenium"""
    # Available difficulty levels
    difficulty = {1: 'EASY', 2: 'MEDIUM', 3: 'HARD', 4: 'EVIL'}

    # Start webdriver and find starting HTML elements
    with webdriver.Chrome() as browser:
        url = f'https://nine.websudoku.com/?level={level}'
        browser.get(url)
        puzzle      = browser.find_element (by=By.ID      , value='puzzle_grid')
        start_state = puzzle .find_elements(by=By.TAG_NAME, value='input'      )

        # Input starting values from HTML onto a board (list of lists)
        board = [[0]*9 for _ in range(9)]
        for cell in start_state:
            x = int(cell.get_attribute('id')[1])
            y = int(cell.get_attribute('id')[2])
            if cell.get_attribute('value') == "":
                board[y][x] = 0
            else:
                board[y][x] = int(cell.get_attribute('value'))

        # Solve the given board
        print(f'Solving {difficulty[level]} Sudoku board from {url}')
        sudoku_solver = SudokuPuzzle(board)
        solved_board  = sudoku_solver.solve()

        # Fill in the blank spaces
        print('\nEntering solution into Chrome browser...')
        for cell in start_state:
            if cell.get_attribute('value') == "":
                x = int(cell.get_attribute('id')[1])
                y = int(cell.get_attribute('id')[2])
                cell.send_keys(solved_board[y][x])

        # Check validity of answer
        time.sleep(2)
        submit = browser.find_element(by=By.XPATH, value = '//input[@name="submit"]')
        submit.click()
        time.sleep(5)

if __name__ == '__main__':
    solve_random_browser_board()
