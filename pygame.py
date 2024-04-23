import pygame
import sys

class Cell:
    def __init__(self, value, row, col, width, height, font, editable=True):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.font = font
        self.editable = editable
        self.selected = False

    def draw(self, win):
        x = self.col * self.width
        y = self.row * self.height
        pygame.draw.rect(win, pygame.Color('black'), (x, y, self.width, self.height), 1)
        
        if self.value != 0:
            text_surface = self.font.render(str(self.value), True, pygame.Color('blue'))
            win.blit(text_surface, (x + (self.width - text_surface.get_width()) / 2,
                                    y + (self.height - text_surface.get_height()) / 2))
        
        if self.selected:
            pygame.draw.rect(win, pygame.Color('red'), (x, y, self.width, self.height), 3)

class Board:
    def __init__(self, board_size, cell_size, win, font):
        self.rows = board_size
        self.cols = board_size
        self.cell_size = cell_size
        self.win = win
        self.font = font
        self.cells = [[Cell(0, i, j, cell_size, cell_size, font) for j in range(self.cols)] for i in range(self.rows)]
        self.selected = None

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw(self.win)

    def select_cell(self, mouse_pos):
        if self.selected:
            self.selected.selected = False
        col = mouse_pos[0] // self.cell_size
        row = mouse_pos[1] // self.cell_size
        self.selected = self.cells[row][col]
        self.selected.selected = True

    def set_value(self, value):
        if self.selected and self.selected.editable:
            self.selected.value = value

pygame.init()
window_size = 600
win = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Advanced Sudoku")
font = pygame.font.Font(None, 40)

board = Board(9, window_size // 9, win, font)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.select_cell(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key in range(pygame.K_1, pygame.K_9 + 1):
                board.set_value(event.key - pygame.K_0)

    win.fill(pygame.Color('white'))
    board.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
