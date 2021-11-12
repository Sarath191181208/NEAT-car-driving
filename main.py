import pygame
import os
from car import Car
import neat
import sys 
import pickle

from timer import Timer
from Fitness import WHITE, fitness_points


(WIN_WIDTH, WIN_HEIGHT) = (600, 600)
WIDGETS_WIDTH, WIDGETS_HEIGHT = (200, 600)
MAP_IMAGE = pygame.image.load(os.path.join("assets", "extreme.png"))
GENERATION = 0

def PYtxt(txt: str, fontSize: int = 16, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

def compare(x_min, x_max, y_min, y_max, num):
    new_val = (((num-x_min)/(x_max-x_min))* (y_max-y_min) ) + y_min

    return new_val


class Map():
    def __init__(self):
        self.img = pygame.transform.scale(MAP_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
    def draw(self, win):
        win.blit(self.img, (0,0))

    def get_at(self, pos):
        x,y = pos 
        if x > WIN_WIDTH-30 or x < 0 or y > WIN_HEIGHT-30 or y < 0:
            return (255,255,255,255)
        return self.img.get_at(pos)


class Label():
    def __init__(self, x, y, pre="", initial_val=0) -> None:
        self.val = initial_val
        self.x, self.y = x, y
        self.pre = pre
        self.font_size = 16
    def draw(self,win):
        txt = PYtxt(self.pre+str(self.val), self.font_size)
        # win.blit(txt, (self.x-txt.get_width()/2, self.y-txt.get_height()/2) )
        win.blit(txt , (self.x,self.y))
    def set(self,val):
        self.val = val

class Triangle():
    def __init__(self):
        self.x, self.y = 0, 0 
    def draw(self,win):
        gap = 8
        x, y = self.x, self.y
        x2, y2 = self.x-gap, self.y-gap
        x3, y3 = self.x+gap, self.y-gap
        pnts = [(x,y), (x2,y2), (x3,y3)]
        pygame.draw.polygon(surface=win, color=(255,0,0), points=pnts)


def draw(win,cars, points, *args):
    # win.fill((255,255,255))
    pygame.draw.line(win, (0,0,0), (602,0), (602,594), 2)
    for arg in args:
        arg.draw(win)
    for car in cars:
        car.draw(win)
    for point in points:
        p1 = point[0]
        p2 = point[1]
        pygame.draw.line(win, (0,255,0), p1, p2, 2)
    pygame.display.update()

def main(genomes, config):
    # initialising pygame 
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((WIN_WIDTH+WIDGETS_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('AI Car simulation')
    FPS = 60

    game_end_timer = Timer(120)
    game_end_timer.start_timer()

    # Labels
    global GENERATION
    GENERATION += 1
    generation_label = Label(630,30, "Generation : ", GENERATION)
    alive_label = Label(630,70, "Alive : ",0)
    time_label = Label(630, 110, "Time Left :", 0)
    maxdis_label = Label(630, 150, "Max Distance :", 0)
    triangle = Triangle()
    # high_score_label = Label(WIN_WIDTH-50,60, "High Score : ",0)

    # init map and score points
    track = Map()
    points = fitness_points(WIN_WIDTH, WIN_HEIGHT, track.img)

    # init cars, gens, nets
    nets = []
    cars = []
    genes = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        g.fitness = 0
        nets.append(net)
        cars.append(Car(270, 500))
        cars[-1].score_points = points
        genes.append(g)
    best_idx = 0
    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)
        track.draw(WIN)

        if not game_end_timer.start:
            break

        # Car action
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_dis())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10 # Left
            elif choice == 1:
                car.angle -= 10 # Right
            elif choice == 2:
                if(car.vel - 2 >= 12):
                    car.vel -= 2 # Slow Down
            else:
                car.vel += 2 # Speed Up

        alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                alive += 1
                car.update(track, WIN)
                genes[i].fitness = car.get_score()
            else:
                # genes[i].fitness -= 5000
                genes.pop(i)
                nets.pop(i)
                cars.pop(i)

        max_so_far = 0 
        max_dis = 0
        for idx, val in enumerate(genes):
            dis = cars[idx].distance_covered
            max_dis = max(max_dis, dis)
            if val.fitness > max_so_far:
                max_so_far = val.fitness
                if genes[best_idx].fitness > max_so_far:
                    best_idx = idx
        if len(cars) > 0:
            x,y = cars[best_idx].pos_
            triangle.x, triangle.y = x, y-10
        

        # for idx in rm_idxs:
        #     # genes[idx].fitness -= 200
        #     genes.pop(idx)
        #     nets.pop(idx)
        #     cars.pop(idx)


        maxdis_label.set(max_dis)
        alive_label.set(alive)
        time_label.set(game_end_timer.get())
        if alive == 0:
            break
        draw(WIN,cars,points, generation_label, alive_label, time_label, maxdis_label, triangle)
        game_end_timer.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit(0)
            # End the current generation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    break
                if event.key == pygame.K_s:
                    with open('best.pickle', 'wb') as f:
                        pickle.dump(genes[best_idx], f)

if __name__ == "__main__":
    
    # Load Config
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"./assets/config.txt")

    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(main, 1000)