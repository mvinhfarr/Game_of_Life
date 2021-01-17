import sys
import numpy as np
import pygame
import life

# board_size = board_rows, board_cols = 80, 80
# cell_size = 100
# size = width, height = board_cols*cell_size, board_rows*cell_size

size = width, height = 800, 800
cell_size = 80
board_size = board_rows, board_cols = width // cell_size, height // cell_size

font_size = 24
font_height, font_width = font_size, int(font_size * 0.55 + 0.5)

green = 102, 255, 102
greyed_green = 159, 186, 133
red = 255, 77, 77
greyed_red = 180, 128, 128
black = 0, 0, 0
white = 255, 255, 255
grey = 215, 215, 215

SIMULATEGENERATION = pygame.USEREVENT + 1
sim_speed = 200


def build_control_buttons(disp, font):
    button_xpos = width + (disp.get_width() - width) // 2  # x position for the center of all the buttons
    button_ypos = 10 + int(font_height * 1.5)  # y position of the center of the top button (start)
    button_ypad_factor = 2

    control_button_text = 'Start', 'Stop', 'Reset'
    colors_sim = greyed_green, red, grey
    colors_not_sim = green, greyed_red, black

    control_buttons = {}
    for n in range(len(control_button_text)):
        button_text = font.render(control_button_text[n], True, black, None)
        text_rect = button_text.get_rect()
        text_rect.center = button_xpos, button_ypos + button_ypad_factor * font_height * n
        button_rect = pygame.Rect(0, 0, font_width * 8, font_height * 1.2)
        button_rect.center = text_rect.center
        button_color = colors_not_sim[n], colors_sim[n]
        button_width = 1 if button_color[0] == black else 0, 1 if button_color[1] == black else 0
        button = {'text': button_text, 'text_pos': text_rect, 'rect': button_rect,
                  'color': button_color, 'width': button_width}
        control_buttons[control_button_text[n]] = button

    bottom_rect = control_buttons[control_button_text[-1]]['rect']
    return control_buttons, bottom_rect


def build_strategy_buttons(disp, font, grid, top_align):
    strat_txt_left = width + (disp.get_width() - width) // 4
    strat_txt_top = top_align + 50
    strat_ypad_factor = 1.5
    strat_xpad_factor = 3

    strat_radius = font_height // 4

    strat_opts = {}
    for n in range(len(grid.strats)):
        strat_text = font.render(grid.strats[n], True, black, None)
        strat_text_pos = strat_txt_left, strat_txt_top + strat_ypad_factor * font_height * n
        strat_circle_center = (strat_txt_left - strat_xpad_factor * strat_radius,
                               strat_txt_top + strat_ypad_factor * font_height * n + font_height // 2)
        strat_hitbox = pygame.Rect(strat_circle_center[0] - strat_radius, strat_text_pos[1],
                                   strat_text.get_size()[0] + (strat_xpad_factor + 1) * strat_radius, font_height)

        strat = {
            'text': strat_text,
            'text_pos': strat_text_pos,
            'circle_pos': strat_circle_center,
            'radius': strat_radius,
            'hitbox': strat_hitbox
        }
        strat_opts[grid.strats[n]] = strat

    bottom_rect = strat_opts[grid.strats[-1]]['hitbox']
    return strat_opts, bottom_rect


def draw_grid(disp, grid):
    # will need to add how to draw grid when edge strategy is finite+1
    for (i, j), cell in np.ndenumerate(grid.grid):
        pygame.draw.rect(disp, black, (j * cell_size, i * cell_size, cell_size, cell_size), width=(0 if cell else 1))


def change_grid(grid, mousex, mousey):
    row, col = mousey // cell_size, mousex // cell_size
    grid.swap_cell_state(row, col)


# def which_button(mousex, mousey, ):


def main(grid):
    # Initialize the pygame window. Size is the size of the grid plus a menu bar on the right
    pygame.init()
    disp = pygame.display.set_mode((int(width * 1.25), height))
    pygame.display.update()
    pygame.display.set_caption('Game of Life -- MVF')
    disp.fill(white)

    # Initialize font
    font = pygame.font.SysFont('consolas', size=font_size)

    control_buttons, control_bottom = build_control_buttons(disp, font)
    strat_opts, strat_bottom = build_strategy_buttons(disp, font, grid, control_bottom.bottom)

    # MORE BUTTONS:
    #   - tick speed

    simulate = False
    clock = pygame.time.Clock()

    while True:
        clock.tick(1000)
        mousex, mousey = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if (control_bottom.left <= mousex <= control_bottom.right) and (mousey <= control_bottom.bottom):
                    if control_buttons['Start']['rect'].top <= mousey <= control_buttons['Start']['rect'].bottom:
                        simulate = True
                        pygame.time.set_timer(SIMULATEGENERATION, sim_speed)
                    elif control_buttons['Stop']['rect'].top <= mousey <= control_buttons['Stop']['rect'].bottom:
                        simulate = False
                        pygame.time.set_timer(SIMULATEGENERATION, 0)
                    elif control_buttons['Reset']['rect'].top <= mousey <= control_buttons['Reset']['rect'].bottom:
                        if not simulate:
                            grid.reset_grid()
                elif (strat_bottom.left <= mousex) and (control_bottom.bottom <= mousey <= strat_bottom.bottom):
                    new_strat = [key for key, strat in strat_opts.items() if (strat['hitbox'].left <= mousex <= strat['hitbox'].right) and (strat['hitbox'].top <= mousey <= strat['hitbox'].bottom)]
                    if not new_strat:
                        continue
                    elif len(new_strat) > 1:
                        raise Exception('Program error, two button strats clicked simultaneously?')
                    else:
                        grid.set_edge_strat(new_strat[0])
                elif (0 <= mousex <= width) and (0 <= mousey <= height):  # Handle all mouse clicks on the grid
                    if not simulate:
                        change_grid(grid, mousex, mousey)
            elif event.type == SIMULATEGENERATION:
                grid.turn()

        disp.fill(white)
        pygame.draw.line(disp, black, (width, 0), (width, height))

        for button in control_buttons.values():
            pygame.draw.rect(disp, button['color'][simulate], button['rect'], width=button['width'][simulate])
            disp.blit(button['text'], button['text_pos'])

        for key, strat in strat_opts.items():
            pygame.draw.circle(disp, black, strat['circle_pos'], strat['radius'],
                               width=0 if grid.edge_strat == key else 1)
            disp.blit(strat['text'], strat['text_pos'])

        draw_grid(disp, grid)

        if not grid.grid.any():
            simulate = False
            pygame.time.set_timer(SIMULATEGENERATION, 0)

        pygame.display.update()


if __name__ == '__main__':
    board = life.Grid(board_size)
    main(board)
