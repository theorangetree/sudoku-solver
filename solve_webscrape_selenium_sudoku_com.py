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

def solve_random_browser_board():
    with webdriver.Chrome() as browser:
        browser.get('https://sudoku.com/')
        html_page = browser.find_element(by=By.TAG_NAME, value='html')
        hint_button = browser.find_element(by=By.CLASS_NAME, value='game-controls-hint')

        current_key = Keys.RIGHT
        waiting_key = Keys.LEFT
        for i in range(81):
            hint_button.click()

            if i % 9 == 8:
                html_page.send_keys(Keys.DOWN)
                current_key, waiting_key = waiting_key, current_key # Swap active key
            else:
                html_page.send_keys(current_key)

            time.sleep(0.025)

        time.sleep(5)
        browser.quit()

if __name__ == '__main__':
    solve_random_browser_board()
