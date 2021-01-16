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
red = 255, 77, 77
black = 0, 0, 0
white = 255, 255, 255


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
    start_text = font.render('Start', True, black, green)
    stop_text = font.render('Stop', True, black, red)
    reset_text = font.render('Reset', True, black, white)

    # Generate rectangles representing the position of the ubttons
    button_xpos = width + (disp.get_width() - width) // 2  # x position for the center of all the buttons
    button_ypos = 10 + int(font_height*1.5)  # y position of the center of the top button (start)

    start_rect = start_text.get_rect()  # Get the rectangle that describes each button's text
    stop_rect = stop_text.get_rect()
    reset_rect = reset_text.get_rect()

    start_rect.center = button_xpos, button_ypos  # Set the coordinates of the center of each rectangle
    stop_rect.center = button_xpos, button_ypos + 2*font_height  # Include spacing of one button height
    reset_rect.center = button_xpos, button_ypos + 4*font_height

    # MORE BUTTONS:
    #   - edge strategy
    #   - tick speed

    simulate = False
    clock = pygame.time.Clock()
    tick_speed = 40

    while True:
        clock.tick(tick_speed)
        mousex, mousey = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if (start_rect.left <= mousex <= start_rect.right) and (start_rect.top <= mousey <= start_rect.bottom):
                    simulate = True
                    tick_speed = 2
                elif (stop_rect.left <= mousex <= stop_rect.right) and (stop_rect.top <= mousey <= stop_rect.bottom):
                    simulate = False
                    tick_speed = 40
                elif (reset_rect.left <= mousex <= reset_rect.right) and (reset_rect.top <= mousey <= reset_rect.bottom):
                    grid.reset_grid()
                elif (0 <= mousex <= width) and (0 <= mousey <= height):
                    change_grid(grid, mousex, mousey)

        disp.fill(white)
        pygame.draw.line(disp, black, (800, 0), (800, 800))

        disp.blit(start_text, start_rect)
        disp.blit(stop_text, stop_rect)
        disp.blit(reset_text, reset_rect)

        if simulate:
            grid.turn()

        draw_grid(disp, grid)

        pygame.display.update()


if __name__ == '__main__':
    board = life.Grid(board_size)
    main(board)
