import pygame

class Cell:
    def __init__(self, value, row, col, width, height, font, editable=True):
        self.value = value  # Final value of the cell
        self.sketch = 0  # Temporary sketch value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.font = font
        self.editable = editable  # Whether the cell can be edited
        self.selected = False

    def draw(self, win):
        # Draw cell background and outline
        x = self.col * self.width
        y = self.row * self.height
        pygame.draw.rect(win, pygame.Color('white'), (x, y, self.width, self.height))
        pygame.draw.rect(win, pygame.Color('black'), (x, y, self.width, self.height), 1)

        # Draw the value or sketch
        if self.value != 0:
            text = self.font.render(str(self.value), True, pygame.Color('blue'))
            win.blit(text, (x + (self.width - text.get_width()) // 2, y + (self.height - text.get_height()) // 2))
        elif self.sketch != 0:
            text = self.font.render(str(self.sketch), True, pygame.Color('gray'))
            win.blit(text, (x + 5, y + 5))

        # Highlight if selected
        if self.selected:
            pygame.draw.rect(win, pygame.Color('red'), (x, y, self.width, self.height), 3)

    def set_value(self, value):
        if self.editable:
            self.value = value

    def set_sketch(self, value):
        if self.editable:
            self.sketch = value
