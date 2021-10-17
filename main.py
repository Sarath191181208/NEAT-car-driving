import pygame
import os
from car import Car

(WIN_WIDTH, WIN_HEIGHT) = (700, 600)
MAP_IMAGE = pygame.image.load(os.path.join("assets", "map.png"))

def PYtxt(txt: str, fontSize: int = 16, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


def draw(win, *args):
    win.fill((255,255,255))

    for arg in args:
        arg.draw(win)
    pygame.display.update()

class Map():
    def __init__(self):
        self.img = pygame.transform.scale(MAP_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
    def draw(self, win):
        win.blit(self.img, (0,0))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('')
    FPS = 60

    car = Car(300, 500)
    track = Map()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw(WIN, track, car)

    pygame.quit()
    quit()
if __name__ == '__main__':
    main()