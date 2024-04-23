import pygame
from cells import Cell  
import math
import random

class SudokuGenerator:
    # Full implementation of SudokuGenerator is assumed here

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * self.row_length for _ in range(self.row_length)]
        self.box_length = int(math.sqrt(row_length))
        self.fill_values()

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = nums.pop()

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length or col >= self.row_length:
            return True

        if row < 3:
            if col < 3:
                col = 3
        elif row < self.row_length - 3:
            if col == int(row // 3) * 3:
                col += 3
        else:
            if col == self.row_length - 3:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % 3, col - col % 3, num))

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(self.row_length))

    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def remove_cells(self):
        count = self.removed_cells
        while count > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1

    def get_board(self):
        return self.board

class Board:
    def __init__(self, width, height, win, font, difficulty='easy'):
        self.width = width
        self.height = height
        self.win = win
        self.font = font
        self.difficulty = difficulty
        self.generate_new_board()

    def generate_new_board(self):
        removed_cells = 20 if self.difficulty == 'easy' else 30 if self.difficulty == 'medium' else 40
        generator = SudokuGenerator(9, removed_cells)
        puzzle = generator.get_board()
        self.cells = [[Cell(puzzle[i][j], i, j, self.width // 9, self.height // 9, self.font, puzzle[i][j] == 0) for j in range(9)] for i in range(9)]
        self.original = [[cell.value for cell in row] for row in self.cells]

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows + 1):
            thick = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for row in self.cells:
            for cell in row:
                cell.draw(self.win)

    def select(self, row, col):
        if hasattr(self, 'selected_cell'):
            if self.selected_cell:
                self.cells[self.selected_cell[0]][self.selected_cell[1]].selected = False
        self.selected_cell = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        if x < self.width and y < self.height:
            col = x // (self.width // 9)
            row = y // (self.height // 9)
            return (row, col)
        return None

    def clear(self):
        if self.selected_cell:
            cell = self.cells[self.selected_cell[0]][self.selected_cell[1]]
            if cell.editable:
                cell.set_value(0)
                cell.set_sketch(0)

    def place_number(self, value):
        if self.selected_cell:
            cell = self.cells[self.selected_cell[0]][self.selected_cell[1]]
            if cell.editable:
                cell.set_value(value)

    def reset_to_original(self):
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                if cell.editable:
                    cell.set_value(self.original[i][j])
                    cell.set_sketch(0)

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def update_board(self):
        for row in self.cells:
            for cell in row:
                cell.value = cell.value  # Placeholder for potential board state updating

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return (i, j)
        return None

    def check_board(self):
        # Check each row
        for row in self.cells:
            if not self._is_part_valid([cell.value for cell in row]):
                return False
        # Check each column
        for col in range(9):
            if not self._is_part_valid([self.cells[row][col].value for row in range(9)]):
                return False
        # Check each 3x3 square
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                if not self._check_square(start_row, start_col):
                    return False
        return True

    def _is_part_valid(self, part):
        part = [x for x in part if x != 0]
        return len(part) == len(set(part))

    def _check_square(self, start_row, start_col):
        values = []
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                cell_value = self.cells[r][c].value
                if cell_value != 0:
                    values.append(cell_value)
        return self._is_part_valid(values)
