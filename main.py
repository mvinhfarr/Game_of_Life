import sys
import numpy as np
import pygame
import life

# board_size = board_rows, board_cols = 80, 80
# cell_size = 100
# size = width, height = board_cols*cell_size, board_rows*cell_size

size = width, height = 800, 800
cell_size = 100
board_size = board_rows, board_cols = width // cell_size, height // cell_size

font_size = 24
font_height, font_width = font_size, int(font_size*0.55 + 0.5)

green = 102, 255, 102
greyed_green = 159, 186, 133
red = 255, 77, 77
greyed_red = 180,128,128
black = 0, 0, 0
white = 255, 255, 255
grey = 215, 215, 215


def draw_grid(disp, grid):
    # will need to add how to draw grid when edge strategy is finite+1
    for (i, j), cell in np.ndenumerate(grid.grid):
        pygame.draw.rect(disp, black, (j*cell_size, i*cell_size, cell_size, cell_size), width=(0 if cell else 1))


def change_grid(grid, mousex, mousey):
    row, col = mousey//cell_size, mousex//cell_size
    grid.swap_cell_state(row, col)


def main(grid):
    # Initialize the pygame window. Size is the size of the grid plus a menu bar on the right
    pygame.init()
    disp = pygame.display.set_mode((int(width*1.25), height))
    pygame.display.update()
    pygame.display.set_caption('Game of Life -- MVF')
    disp.fill(white)

    # Initialize font and render text for buttons
    font = pygame.font.SysFont('consolas', size=font_size)
    start_text = font.render('Start', True, black, None)
    stop_text = font.render('Stop', True, black, None)
    reset_text = font.render('Reset', True, black, None)

    # Generate rectangles representing the position of the buttons
    button_xpos = width + (disp.get_width() - width) // 2  # x position for the center of all the buttons
    button_ypos = 10 + int(font_height*1.5)  # y position of the center of the top button (start)
    button_rect = 0, 0, font_width*8, font_height*1.2
    button_ypad_factor = 2

    start_text_rect = start_text.get_rect()  # Get the rectangle that describes each button's text
    stop_text_rect = stop_text.get_rect()
    reset_text_rect = reset_text.get_rect()

    start_text_rect.center = button_xpos, button_ypos  # Set the coordinates of the center of each rectangle
    stop_text_rect.center = button_xpos, button_ypos + button_ypad_factor*font_height  # Include spacing of one button height
    reset_text_rect.center = button_xpos, button_ypos + button_ypad_factor*2*font_height

    start_button, stop_button, reset_button = pygame.Rect(button_rect), pygame.Rect(button_rect), pygame.Rect(button_rect)
    start_button.center = start_text_rect.center
    stop_button.center = stop_text_rect.center
    reset_button.center = reset_text_rect.center

    # MORE BUTTONS:
    #   - edge strategy
    #   - tick speed

    simulate = False
    clock = pygame.time.Clock()

    while True:
        clock.tick(100)
        mousex, mousey = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if (start_button.left <= mousex <= start_button.right) and (start_button.top <= mousey <= start_button.bottom):
                    simulate = True
                elif (stop_button.left <= mousex <= stop_button.right) and (stop_button.top <= mousey <= stop_button.bottom):
                    simulate = False
                elif (reset_button.left <= mousex <= reset_button.right) and (reset_button.top <= mousey <= reset_button.bottom):
                    if not simulate:
                        grid.reset_grid()
                elif (0 <= mousex <= width) and (0 <= mousey <= height):  # Handle all mouse clicks on the grid
                    if not simulate:
                        change_grid(grid, mousex, mousey)

        disp.fill(white)
        pygame.draw.line(disp, black, (800, 0), (800, 800))

        if simulate:
            pygame.draw.rect(disp, greyed_green, start_button)
            pygame.draw.rect(disp, red, stop_button)
            pygame.draw.rect(disp, grey, reset_button)
        else:
            pygame.draw.rect(disp, green, start_button)
            pygame.draw.rect(disp, greyed_red, stop_button)
            pygame.draw.rect(disp, black, reset_button, width=1)

        disp.blit(start_text, start_text_rect)
        disp.blit(stop_text, stop_text_rect)
        disp.blit(reset_text, reset_text_rect)

        if simulate:
            grid.turn()

        draw_grid(disp, grid)

        if not grid.grid.any():
            simulate = False

        pygame.display.update()


if __name__ == '__main__':
    board = life.Grid(board_size)
    main(board)
