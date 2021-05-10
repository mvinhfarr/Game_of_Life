# import sys
import pygame
import numpy as np

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 215, 215, 215
GREEN = 102, 255, 102
RED = 255, 77, 77
GREY_GREEN = 159, 186, 133
GREY_RED = 180, 128, 128


def draw_grid(disp, grid, size):
    """
    Draw the board to the pygame display.

    :param disp: pygame.display
    :param grid: numpy array of 1's and 0's representing the board
    :param size: size of each square cell
    :return: None
    """

    for (i, j), cell in np.ndenumerate(grid.grid):
        pygame.draw.rect(disp, BLACK, (j * size, i * size, size, size), width=(0 if cell else 1))


class BooleanButton:
    def __init__(self, disp, font, text='', pos=(0, 0), size=None, color_true=BLACK, color_false=GREY):
        """
        Builds a button with two states, true or false, with two corrresponding colors.
        A True/False state represents if the button can be clicked or not respectively.

        :param disp: pygame.display
        :param font: pygame.font
        :param text: string of button text
        :param pos: tuple of x, y coords of center of button
        :param size: tupe of width, height of the button
        :param color_true: color when button can be clicked
        :param color_false: color when button is unavailable
        """

        self.disp = disp
        self.font = font

        self.xpos, self.ypos = pos
        self.size = self.width, self.height = size

        self.text, self.text_pos, self.rect = self.build_button(text)

        # Tuple representing the two colors which are selected using a boolean state variable
        # In this orientation because false == 0 and true == 1
        self.color = color_false, color_true

        # Set the border width to 1 if the color is black to draw just the outline of the rectangle
        # Otherwise set the border width to 0 to fill the rectangle with the provided color
        self.border_width = 1 if color_false == BLACK else 0, 1 if color_true == BLACK else 0

    def build_button(self, label):
        """
        Construct the button text and rectangle pygame objects.

        :param label: string of button text
        :return: text: font object with text, text_rect: rectangle defining location of text,
                 rect: Rect object for the button
        """

        text = self.font.render(label, True, BLACK, None)
        text_rect = text.get_rect()
        rect = pygame.Rect(0, 0, self.width, self.height)
        text_rect.center = rect.center = self.xpos, self.ypos

        return text, text_rect, rect

    def draw(self, state):
        """
        Draw the button onto the display.

        :param state: Bool setting button color
        :return: None
        """

        pygame.draw.rect(self.disp, self.color[state], self.rect, width=self.border_width[state])
        self.disp.blit(self.text, self.text_pos)


class RadioButtons:
    def __init__(self, disp, font, opts, pos=(0, 0), xpad_factor=3, ypad_factor=1.5):
        """
        Builds a set of radio buttons that are stored in a dictionary.

        :param disp: pygame.display
        :param font: pygame.font
        :param opts: list of strings used to make options
        :param pos: tuple of left, top of the position of the sting for the first option
        :param xpad_factor: number of radii between the left of the struing and center of the irlce
        :param ypad_factor: number of character heights between the top of each option
        """

        self.disp = disp
        self.font = font

        if len(opts) < 1:
            raise ValueError('Must have at least one Radio Button')
        self.opts = opts

        self.left, self.top = pos
        self.xpad_factor = xpad_factor
        self.ypad_factor = ypad_factor
        self.radius = font.get_height() // 4  # Radius of the radio button

        self.buttons = self.build_buttons()

        # When 0 the button fills, when 1 the button is just a circle of width 1px
        self.width = lambda key, selected: 0 if key == selected else 1

    def build_buttons(self):
        """
        Create dictionary of the set of radio buttons with each button's text as its key.

        :return: dict of radio buttons
        """

        buttons = {}
        for n in range(len(self.opts)):
            text = self.font.render(self.opts[n], True, BLACK, None)
            text_pos = self.left, self.top + self.ypad_factor * self.font.get_height() * n
            circle_center = (self.left - self.xpad_factor * self.radius,
                             self.top + self.ypad_factor * self.font.get_height() * n + self.font.get_height() // 2)
            # Rectangle where the button can be clicked - includes the circle and text
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

    def draw(self, selected):
        """
        Draw the radio buttons to the display.

        :param selected: key of the radio button that is currently selected
        :return: None
        """
        for key, btn in self.buttons.items():
            pygame.draw.circle(self.disp, BLACK, btn['circle_pos'], self.radius, width=self.width(key, selected))
            self.disp.blit(btn['text'], btn['text_pos'])
