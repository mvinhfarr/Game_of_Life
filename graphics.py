# import sys
import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (215, 215, 215)
GREEN = (102, 255, 102)
RED = (255, 77, 77)
GREY_GREEN = (159, 186, 133)
GREY_RED = (180, 128, 128)


def draw_grid(disp, grid, size):
    # will need to add how to draw grid when edge strategy is finite+1 (or not lol)
    for (i, j), cell in np.ndenumerate(grid.grid):
        pygame.draw.rect(disp, BLACK, (j * size, i * size, size, size), width=(0 if cell else 1))


class BooleanButton:
    """
    pos: xcenter, ycenter
    size: button rect width, height
    color_true, color_false: rgb color
    """

    def __init__(self, disp, font, text='', pos=(0, 0), size=None, color_true=BLACK, color_false=GREY):
        self.disp = disp
        self.font = font

        self.xpos, self.ypos = pos
        self.size = self.width, self.height = size

        self.text, self.text_pos, self.rect = self.build_button(text)

        # in this orientation because false == 0 and true == 1
        self.color = color_false, color_true
        # self.color = lambda b: color_true if b else color_false
        # I think this is more elegant, but it's also substantially slower

        self.border_width = 1 if color_false == BLACK else 0, 1 if color_true == BLACK else 0

        # self.state = state

        # self.action = None

    def build_button(self, label):
        text = self.font.render(label, True, BLACK, None)
        text_rect = text.get_rect()
        rect = pygame.Rect(0, 0, self.width, self.height)
        text_rect.center = rect.center = self.xpos, self.ypos

        return text, text_rect, rect

    def draw(self, state):
        pygame.draw.rect(self.disp, self.color[state], self.rect, width=self.border_width[state])
        self.disp.blit(self.text, self.text_pos)

    # def set_state(self, bol):
    #     self.state = bol

    # def set_action(self, func):
    #     if callable(func):
    #         self.action = func
    #     else:
    #         raise ValueError('Invalid action, expected a callable')


class RadioButtons:
    """
    opts: list of strings used to make options
    pos: left, top of the string for the first option
    xpad_factor: number of radii between the left of the string and the center of the circle
    ypad_factor: # of character heights between the top of each option
    """

    def __init__(self, disp, font, opts, pos=(0, 0), xpad_factor=3, ypad_factor=1.5):
        self.disp = disp
        self.font = font

        if len(opts) <= 1:
            raise ValueError('Must have more than one Radio Button')
        self.opts = opts

        self.left, self.top = pos
        self.xpad_factor = xpad_factor
        self.ypad_factor = ypad_factor
        self.radius = font.get_height() // 4

        self.buttons = self.build_buttons()

        self.selected = self.opts[0]
        self.width = lambda key: 0 if key == self.selected else 1

    def build_buttons(self):
        buttons = {}
        for n in range(len(self.opts)):
            text = self.font.render(self.opts[n], True, BLACK, None)
            text_pos = self.left, self.top + self.ypad_factor * self.font.get_height() * n
            circle_center = (self.left - self.xpad_factor * self.radius,
                             self.top + self.ypad_factor * self.font.get_height() * n + self.font.get_height() // 2)
            hitbox = pygame.Rect(circle_center[0] - self.radius, text_pos[1],
                                 text.get_width() + (self.xpad_factor + 1) * self.radius, self.font.get_height())

            opt_button = {
                'text': text,
                'text_pos': text_pos,
                'circle_pos': circle_center,
                'hitbox': hitbox
            }

            buttons[self.opts[n]] = opt_button
        return buttons

    def draw(self):
        for key, btn in self.buttons.items():
            pygame.draw.circle(self.disp, BLACK, btn['circle_pos'], self.radius, width=self.width(key))
            self.disp.blit(btn['text'], btn['text_pos'])
