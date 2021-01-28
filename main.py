import sys
import timeit
import numpy as np
import pygame

import array_life
# import vector_life
import graphics

# board_size = board_rows, board_cols = 80, 80
# cell_size = 100
# size = width, height = board_cols*cell_size, board_rows*cell_size

size = width, height = 800, 800
cell_size = 20
board_size = board_rows, board_cols = height // cell_size, width // cell_size

font_size = 24
font_height, font_width = font_size, int(font_size * 0.55 + 0.5)

SIMULATEGENERATION = pygame.USEREVENT + 1
sim_speed = 10
# ~77 ms per loop with


def build_control(disp, font):
    xcenter = width + (disp.get_width() - width) // 2
    top_ycenter = 10 + int(font_height * 1.5)
    ypad = 2 * font_height

    labels = 'Start', 'Stop', 'Reset', 'Restart'
    colors_true = graphics.GREEN, graphics.RED, graphics.BLACK, graphics.BLACK
    colors_false = graphics.GREY_GREEN, graphics.GREY_RED, graphics.GREY, graphics.GREY
    # button_state = True, False, True

    control_buttons = {}
    for n in range(len(labels)):
        button = graphics.BooleanButton(disp, font, labels[n], pos=(xcenter, top_ycenter + ypad*n),
                                        size=(font_width * 8, font_height * 1.2),
                                        color_true=colors_true[n], color_false=colors_false[n])
        control_buttons[labels[n]] = button

    bottom_y = control_buttons[labels[-1]].rect.bottom

    return control_buttons, bottom_y


def build_strats(disp, font, grid, top):
    left = width + (disp.get_width() - width) // 4
    top = top + 50
    xpad = 3
    ypad = 1.5

    strats = graphics.RadioButtons(disp, font, grid.strats, pos=(left, top), xpad_factor=xpad, ypad_factor=ypad)

    bottom_y = strats.buttons[strats.opts[-1]]['hitbox'].bottom

    return strats, bottom_y

# def build_init_buttons(disp, font, grid):
#     fill_rand_text =


def change_grid(grid, mousex, mousey):
    row, col = mousey // cell_size, mousex // cell_size
    grid.swap_cell_state(row, col)


def main(grid):
    # Initialize the pygame window. Size is the size of the grid plus a menu bar on the right
    pygame.init()
    disp = pygame.display.set_mode((int(width * 1.25), height))
    pygame.display.update()
    pygame.display.set_caption('Game of Life -- MVF')
    disp.fill(graphics.WHITE)

    # Initialize font
    font = pygame.font.SysFont('consolas', size=font_size)

    control_buttons, control_bottom = build_control(disp, font)
    strat_opts, strat_bottom = build_strats(disp, font, grid, control_bottom)

    # MORE BUTTONS:
    #   - tick speed
    #   - init options

    saved_board = None

    simulate = False
    clock = pygame.time.Clock()

    print(pygame.time.get_ticks())

    while True:
        # clock.tick(10)
        print(clock.tick())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = pygame.mouse.get_pos()

                if control_buttons['Start'].rect.collidepoint(mousex, mousey):
                    saved_board = grid.grid.copy()
                    simulate = True
                    pygame.time.set_timer(SIMULATEGENERATION, sim_speed)
                elif control_buttons['Stop'].rect.collidepoint(mousex, mousey):
                    simulate = False
                    pygame.time.set_timer(SIMULATEGENERATION, 0)
                elif control_buttons['Reset'].rect.collidepoint(mousex, mousey):
                    if not simulate:
                        grid.reset_grid()
                elif control_buttons['Restart'].rect.collidepoint(mousex, mousey):
                    grid.set_grid(saved_board)
                elif (0 <= mousex <= width) and (0 <= mousey <= height):  # Handle all mouse clicks on the grid
                    if not simulate:
                        change_grid(grid, mousex, mousey)

                new_strat = [key for key, strat in strat_opts.buttons.items()
                             if strat['hitbox'].collidepoint(mousex, mousey)]

                if not new_strat:
                    continue
                elif len(new_strat) > 1:
                    raise Exception('Program error, two button strats clicked simultaneously?')
                else:
                    grid.set_edge_strat(new_strat[0])

            elif event.type == SIMULATEGENERATION:
                grid.turn()
                pygame.event.clear(SIMULATEGENERATION)

        disp.fill(graphics.WHITE)
        pygame.draw.line(disp, graphics.BLACK, (width, 0), (width, height))

        control_buttons['Start'].draw(not simulate)
        control_buttons['Stop'].draw(simulate)
        control_buttons['Reset'].draw(not simulate)
        control_buttons['Restart'].draw(True)

        strat_opts.draw(grid.edge_strat)

        graphics.draw_grid(disp, grid, cell_size)

        if not grid.grid.any():
            simulate = False
            pygame.time.set_timer(SIMULATEGENERATION, 0)

        pygame.display.update()


if __name__ == '__main__':
    board = array_life.Board(board_size)
    main(board)
