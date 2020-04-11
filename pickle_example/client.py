import pygame
import pickle_example.config as config



def gameloop():
    screen = pygame.display.set_mode((config.window_width, config.window_height))
    rungame = True
    while rungame:
        draw_game(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                pygame.quit()

def draw_game(window):
    window.fill((125,125,125))
    pygame.display.update()








if __name__ == '__main__':
    pygame.init()
    gameloop()