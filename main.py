import pygame as pg
import sys
import os
from random import randint

WIN_SIZE = (600, 600)
FPS = 60

COLORS = [
    (0, 0, 0),
    (245, 66, 66),
    (54, 214, 203),
    (213, 54, 224),
    (54, 224, 71),
    (229, 232, 49)
]
FPS = 50
pg.init()
size = WIDTH, HEIGHT = 600, 600
screen = pg.display.set_mode(size)
FPS = 50
clock = pg.time.Clock()


def terminate():
    pg.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('Data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    return image


def end_screen(points):
    pg.display.set_caption('the end')
    intro_text = [f'Your points: {points}', " ",
                  "\t \t GAME OVER",
                  " ",
                  "[PRESS ANY BUTTON TO REPLAY]"]
    fon = pg.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pg.font.Font(None, 33)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pg.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 170
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pg.display.flip()
        clock.tick(FPS)


def start_screen():
    pg.display.set_caption('hello hello')
    intro_text = ["LINES GAME", "",
                  "",
                  "",
                  "[PRESS ANY BUTTON TO START]"]
    fon = pg.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pg.font.Font(None, 33)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pg.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 170
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pg.display.flip()
        clock.tick(FPS)


start_screen()

screen.fill(pg.Color(0, 0, 0))
pg.display.flip()
clock.tick(FPS)
###


class Lines:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode(WIN_SIZE)
        self.width = 9
        self.height = 9
        self.left = 30
        self.top = 30
        self.cell_size = 60
        self.running = True
        self.player_points = 0
        self.set_matrix()
        self.add_circles_to_matrix()
        self.is_circle_active = False
        self.active_circle_color = None
        self.active_circle_coords = None

    def set_matrix(self):
        pg.display.set_caption(f'Your points: {self.player_points}')

        self.cells_matrix = [
            [
                {
                    'rect': pg.Rect(
                        row_index * self.cell_size + self.left,
                        col_index * self.cell_size + self.top,
                        self.cell_size,
                        self.cell_size
                    ),
                    'color': 0,
                    'is_active': False
                } for col_index in range(self.height)
            ] for row_index in range(self.width)
        ]

    def has_path(self, start_coords, target_coords):
        checked_cells = []

        def recursive_step(y, x):
            if (
                y < 0 or y > 8 or x < 0 or x > 8 or
                self.cells_matrix[y][x]['color'] != 0 or
                f'{y}{x}' in checked_cells
            ):
                return False

            if y == target_coords[0] and x == target_coords[1]:
                return True

            checked_cells.append(f'{y}{x}')

            return (
                recursive_step(y - 1, x) or
                recursive_step(y + 1, x) or
                recursive_step(y, x - 1) or
                recursive_step(y, x + 1)
            )

        return (
            recursive_step(start_coords[0] - 1, start_coords[1]) or
            recursive_step(start_coords[0] + 1, start_coords[1]) or
            recursive_step(start_coords[0], start_coords[1] - 1) or
            recursive_step(start_coords[0], start_coords[1] + 1)
        )

    def user_action(self, row_index, col_index):
        if self.cells_matrix[row_index][col_index]['color'] != 0 and not self.is_circle_active:
            self.active_circle_coords = row_index, col_index
            self.active_circle_color = self.cells_matrix[row_index][col_index]['color']
            self.cells_matrix[row_index][col_index]['is_active'] = True
            self.is_circle_active = True
            return

        if self.is_circle_active:
            if row_index == self.active_circle_coords[0] and col_index == self.active_circle_coords[1]:
                self.is_circle_active = False
                self.cells_matrix[row_index][col_index]['is_active'] = False
                return
            if self.cells_matrix[row_index][col_index]['color'] != 0:
                return

            if not self.has_path(self.active_circle_coords, (row_index, col_index)):
                return

            self.cells_matrix[row_index][col_index]['color'] = self.active_circle_color
            self.cells_matrix[self.active_circle_coords[0]
                              ][self.active_circle_coords[1]]['color'] = 0
            self.cells_matrix[row_index][col_index]['is_active'] = False
            self.cells_matrix[self.active_circle_coords[0]
                              ][self.active_circle_coords[1]]['is_active'] = False
            self.is_circle_active = False
            self.check_lines()
            self.add_circles_to_matrix()

    def check_lines(self):
        def recursive_step(y, x, direction, color, cells=[]):
            if not color:
                return

            if direction == 'down':
                y += 1
            if direction == 'right':
                x += 1
            if direction == 'downright':
                y += 1
                x += 1
            if direction == 'downleft':
                y += 1
                x -= 1

            if y < 0 or y > 8 or x < 0 or x > 8 or self.cells_matrix[y][x]['color'] != color:
                if (len(cells) >= 5):
                    self.clear_cells(cells)
                return

            if self.cells_matrix[y][x]['color'] == color:
                recursive_step(y, x, direction, color, [*cells, (y, x)])

        for col_index in range(self.height):
            for row_index in range(self.width):
                recursive_step(col_index, row_index, 'down',
                               self.cells_matrix[col_index][row_index]['color'], [(col_index, row_index)])
                recursive_step(col_index, row_index, 'right',
                               self.cells_matrix[col_index][row_index]['color'], [(col_index, row_index)])
                recursive_step(col_index, row_index, 'downright',
                               self.cells_matrix[col_index][row_index]['color'], [(col_index, row_index)])
                recursive_step(col_index, row_index, 'downleft',
                               self.cells_matrix[col_index][row_index]['color'], [(col_index, row_index)])

    def clear_cells(self, cells):
        for coords in cells:
            self.cells_matrix[coords[0]][coords[1]]['color'] = 0

        self.player_points += len(cells)
        pg.display.set_caption(f'Your points: {self.player_points}')

    def logic(self):
        self.check_lines()

        if not any([any([cell['color'] == 0 for cell in row]) for row in self.cells_matrix]):

            end_screen(self.player_points)
            self.set_matrix()
            self.add_circles_to_matrix()
            self.is_circle_active = False
            self.active_circle_color = None
            self.active_circle_coords = None
            self.player_points = 0

    def add_circles_to_matrix(self):
        for _ in range(3):
            if not any([any([cell['color'] == 0 for cell in row]) for row in self.cells_matrix]):
                return

            while True:
                x, y = randint(0, self.height - 1), randint(
                    0, self.width - 1)

                if (self.cells_matrix[y][x]['color'] == 0):
                    self.cells_matrix[y][x]['color'] = randint(1, 5)
                    break

    def render(self):
        self.display.fill((0, 0, 0))
        for col_index in range(self.height):
            for row_index in range(self.width):
                pg.draw.circle(
                    self.display, COLORS[self.cells_matrix[row_index]
                                         [col_index]['color']],
                    (self.cells_matrix[row_index][col_index]['rect'].x + 30,
                     self.cells_matrix[row_index][col_index]['rect'].y + 30),
                    25
                )
                pg.draw.rect(
                    self.display, (255, 255, 255),
                    self.cells_matrix[row_index][col_index]['rect'],
                    1
                )

                if self.cells_matrix[row_index][col_index]['is_active']:
                    pg.draw.circle(
                        self.display, (255, 255, 255),
                        (self.cells_matrix[row_index][col_index]['rect'].x + 30,
                         self.cells_matrix[row_index][col_index]['rect'].y + 30),
                        25,
                        2
                    )
        pg.display.flip()

    def handle_mouse_click(self, x, y):
        for col_index in range(self.height):
            for row_index in range(self.width):
                rect = self.cells_matrix[row_index][col_index]['rect']
                if rect.x < x < rect.x + rect.width and rect.y < y < rect.y + rect.height:
                    self.user_action(row_index, col_index)
                    self.logic()

    def run(self):
        while self.running:
            self.events()
            self.render()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mouse_click(*pg.mouse.get_pos())


if __name__ == '__main__':
    board = Lines()
    board.run()

    pg.quit()
