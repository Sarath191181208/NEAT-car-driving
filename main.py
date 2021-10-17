import pygame
import os
from car import Car

(WIN_WIDTH, WIN_HEIGHT) = (700, 600)
MAP_IMAGE = pygame.image.load(os.path.join("assets", "map.png"))
GENERATION = 0

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

class Label():
    def __init__(self, x, y, pre="", initial_val=0) -> None:
        self.val = initial_val
        self.x, self.y = x, y
        self.pre = pre
        self.font_size = 16
    def draw(self,win):
        txt = PYtxt(self.pre+str(self.val), self.font_size)
        win.blit(txt, (self.x-txt.get_width()/2, self.y-txt.get_height()/2) )



def main():
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('')
    FPS = 60
    # Labels
    global GENERATION
    generation_label = Label(60,30, "Generation : ", GENERATION)
    alive_label = Label(WIN_WIDTH-50,30, "Alive : ",0)

    # cars, tracks
    car = Car(300, 500)
    track = Map()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw(WIN, track, car, generation_label, alive_label)

    pygame.quit()
    quit()
if __name__ == '__main__':
    main()