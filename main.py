import sys
import numpy as np
import pygame
import game

size = width, height = 800, 800
cell_size = 10
font_size = 24
font_height, font_width = font_size, int(font_size*0.55 + 0.5)

green = 102, 255, 102
red = 255, 77, 77
black = 0, 0, 0
white = 255, 255, 255


def main():
    pygame.init()
    disp = pygame.display.set_mode((int(width*1.25), height))
    pygame.display.update()
    pygame.display.set_caption('Game of Life -- MVF')
    disp.fill(white)

    font = pygame.font.SysFont('consolas', size=font_size)
    start_text = font.render('Start', True, black, green)
    stop_text = font.render('Stop', True, black, red)
    reset_text = font.render('Reset', True, black, white)

    button_xpos = width + (disp.get_width() - width) // 2
    button_ypos = 10 + int(font_height*1.5)
    start_rect = start_text.get_rect()
    stop_rect = stop_text.get_rect()
    reset_rect = reset_text.get_rect()

    start_rect.center = button_xpos, button_ypos
    stop_rect.center = button_xpos, button_ypos + 2*font_height
    reset_rect.center = button_xpos, button_ypos + 4*font_height

    while True:
        mousex, mousey = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if (start_rect.left <= mousex <= start_rect.right) and (start_rect.top <= mousey <= start_rect.bottom):
                    print('start')
                elif (stop_rect.left <= mousex <= stop_rect.right) and (stop_rect.top <= mousey <= stop_rect.bottom):
                    print('stop')
                elif (reset_rect.left <= mousex <= reset_rect.right) and (reset_rect.top <= mousey <= reset_rect.bottom):
                    print('reset')

        pygame.draw.rect(disp, green, (15, 45, 60, 90))
        pygame.draw.line(disp, black, (800, 0), (800, 800))
        pygame.draw.line(disp, black, (0, 45), (1000, 45))

        disp.blit(start_text, start_rect)
        disp.blit(stop_text, stop_rect)
        disp.blit(reset_text, reset_rect)

        pygame.display.update()


if __name__ == '__main__':
    main()
