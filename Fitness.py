import pygame
import os
from queue import PriorityQueue

def PYtxt(txt: str, fontSize: int = 16, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2-x1) + abs(y2-y1)

WHITE = (255, 255,255, 255)
GREAY = (70, 70, 70)
BLACK = (0, 0, 0, 255)
BLUE = (10, 40, 100)

checksClr = BLUE
boardClr = WHITE
txtClr = GREAY

class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400,WIN = None):
        self.rows = cols
        self.cols = rows
        self.cubes = [
            [Cube(0, i, j, width, height, self.cols, self.rows,WIN)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.width = width
        self.height = height
        self.win = WIN
        self.surface = pygame.Surface((self.width,self.height))

        self.start = self.cubes[500][270]
        self.start.set((0,0,255), self.win)
        self.end = self.cubes[530][210]
        self.end.set((0,255,0), self.win)
        for i in range(20):
            for j in range(20):
                self.cubes[500+i][210+j].set((0,0,255), self.win)
                self.cubes[500+i][270+j].set((0,255,255), self.win)
    
    def barrier(self):
        # cheking top 
        i = 500
        while i > 0:
            # print(i)
            cube = self.cubes[i][260]
            i -= 1
            # print(cube.color)
            if cube.color ==WHITE:
                i = -1
            else:
                cube.barrier = True
        
        #cheking bottom
        i = 500
        while i < len(self.cubes):
            # print(i)
            cube = self.cubes[i][260]
            i += 1
            if cube.color == WHITE:
                break
            else:
                cube.barrier =True

    def draw(self, win = None):
        if win is None:
            win = self.win 
        win.blit(self.surface,(0,0))
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)
        pygame.display.update()
    

    def draw_grid(self, win):
        thick = 1
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*rowGap),(self.height, rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*colGap, 0), (colGap*i, self.width))

    def set_at(self,i, j, clr):
        self.cubes[i][j].color = clr

    def a_star(self):
        '''A* algorithm to solve the grid'''
        # traverses cubes and updates neighbours
        # we can also do the update at  the time of  placing
        for row in self.cubes:
            for cube in row:
                cube.update_neighbours(self)

        # count is kinda basically score of best path
        count = 0
        # open set stores finalscore , count , cube object
        open_set = PriorityQueue()

        # open_set[2] : class(Cube)
        open_set.put((0, count, self.start))

        # keeps track where  we came from
        came_from = {}

        self.points = []

        # key : cube
        g_score = {cube: float("inf") for row in self.cubes for cube in row}
        g_score[self.start] = 0

        # key : cube
        f_score = {spot: float("inf") for row in self.cubes for spot in row}
        f_score[self.start] = h(self.start.get_pos(), self.end.get_pos())

        # cube is saved in hash
        open_set_hash = {self.start}

        i = 0
        while not open_set.empty():

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # gets the cube current = cube

            current = open_set.get()[2]
            # removes cube from possibilities
            open_set_hash.remove(current)
            # if we reached end
            i += 1
            if i == 7000:
                # print(self.end.get_pos())
                # print(current.get_pos())
                self.points.append((current.get_pos()[1],current.get_pos()[0]))
                i = 0
            # if self.end.get_pos()==current.get_pos():
            #     print(self.end.get_pos()==current.get_pos())
            if current == self.end:
                # self.reconstruct_path(came_from)
                break
                return True

            # go trough each neighbour untill finding  an end
            for neighbour in current.neighbours:
                temp_g_score = g_score[current] + 1

            # updating/entering f score if its useful
                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + \
                        h(neighbour.get_pos(), self.end.get_pos())

                    # putting the  neighbour to  traverse while loop
                    if not (neighbour in open_set_hash):
                        count += 1

                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        # updating the neighbour
                        neighbour.set(BLUE, self.win)
            # self.draw()

            # if this node is already visited update colour
            if current != self.start:
                current.set(GREAY, self.win)

        return False


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows,win):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.centerFactor = 10
        self.win = win
        self.color = (255, 255, 255, 255)
        self.neighbours = []
        self.barrier = False


    def draw(self, win):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        if self.barrier:
            self.color = (210,200,40)
        pygame.draw.rect(win, self.color, pygame.Rect(x, y, colGap, rowGap))


    def set(self, clr, win):
        self.color = clr
        # self.draw(win)
        # pygame.display.update()
    
    def is_barrier(self):
        return (self.color == WHITE) or self.barrier

    def update_neighbours(self, grid):
        '''checks for neighbours and adds them here
        :param grid : A 2x2 matrix       
        '''
        # you can also add diagonal movement here
        # DOWN
        if self.row < self.rows - 1 and not grid.cubes[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid.cubes[self.row + 1][self.col])

        if self.row > 0 and not grid.cubes[self.row - 1][self.col].is_barrier():  # UP
            self.neighbours.append(grid.cubes[self.row - 1][self.col])

        # RIGHT
        if self.col < self.rows - 1 and not grid.cubes[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid.cubes[self.row][self.col + 1])

        # LEFT
        if self.col > 0 and not grid.cubes[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid.cubes[self.row][self.col - 1])
    
    def get_pos(self):
        return self.row, self.col

def draw(win, *args):
    win.fill(WHITE)
    for arg in args:
        arg.draw(win)
    pygame.display.update()

def fitness_points(IMG_WIDTH, IMG_HEIGHT, MAP_IMAGE):
    grid = Grid(IMG_WIDTH, IMG_HEIGHT, IMG_WIDTH, IMG_HEIGHT)

    for i in range(IMG_WIDTH):
        for j in range(IMG_HEIGHT):
            clr = MAP_IMAGE.get_at((i,j))
            grid.set_at(j, i, clr)
    
    grid.barrier()
    grid.a_star()

    pnts = []
    for pos in grid.points:
        # print(pos)

        p1, p2 = None, None
        x, y = pos
        i, j = 0, 0
        dir_x = 0
        dir_y = 0
        while p1 is None:
            i += 1 
            if (x+i) < grid.rows -1:
                if grid.cubes[y][x+i].color == WHITE:
                    p1 = (x+i, y)
                    dir_x = -1
                    break
                
            if (x-i) > 0:
                if grid.cubes[y][x-i].color == WHITE:
                    p1 = (x-i, y)
                    dir_x = 1
                    break
            if (y+i) < grid.rows -1:
                if grid.cubes[y+i][x].color == WHITE:
                    p1 = (x, y+i)
                    dir_y = -1
                    break
                
            if (y-i) > 0:
                if grid.cubes[y-i][x].color == WHITE:
                    p1 = (x, y-i)
                    dir_y = 1
                    break
        j = 0
        while p2 is None:
            j += 1 
            if 0 < x+j*dir_x < grid.rows:
                if grid.cubes[y][x+(j*dir_x)].color == WHITE:
                    p2 =(x+(j*dir_x) ,y)
                    break
            if 0 < y+j*dir_y < grid.rows:
                if grid.cubes[y+(j*dir_y)][x].color == WHITE:
                    p2 =(x, y+(j*dir_y))
                    break
            
        pnts.append([p1, p2])
    return pnts
    

def main():
    pygame.init()
    clock = pygame.time.Clock()
    (WIN_WIDTH, WIN_HEIGHT) = (600, 600)
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('')
    FPS = 60
    print("loaded map")
    MAP_IMAGE = pygame.image.load(os.path.join("assets", "easy.png"))
    MAP_IMAGE = pygame.transform.scale(MAP_IMAGE, (WIN_WIDTH, WIN_HEIGHT))

    print('clac pixels')
    grid = Grid(WIN_WIDTH, WIN_HEIGHT, WIN_WIDTH, WIN_HEIGHT)

    for i in range(WIN_WIDTH):
        for j in range(WIN_HEIGHT):
            clr = MAP_IMAGE.get_at((i,j))
            grid.set_at(j, i, clr)

    WIN.fill(WHITE)
    grid.draw(WIN)
    pygame.display.update()

    grid.barrier()
    grid.a_star()
    print("calc grid")
    # grid.draw(WIN)
    pnts = []
    for pos in grid.points:
        # print(pos)

        p1, p2 = None, None
        x, y = pos
        i, j = 0, 0
        dir_x = 0
        dir_y = 0
        while p1 is None:
            i += 1 
            if (x+i) < grid.rows -1:
                if grid.cubes[y][x+i].color == WHITE:
                    p1 = (x+i, y)
                    dir_x = -1
                    break
                
            if (x-i) > 0:
                if grid.cubes[y][x-i].color == WHITE:
                    p1 = (x-i, y)
                    dir_x = 1
                    break
            if (y+i) < grid.rows -1:
                if grid.cubes[y+i][x].color == WHITE:
                    p1 = (x, y+i)
                    dir_y = -1
                    break
                
            if (y-i) > 0:
                if grid.cubes[y-i][x].color == WHITE:
                    p1 = (x, y-i)
                    dir_y = 1
                    break
        j = 0
        while p2 is None:
            j += 1 
            if 0 < x+j*dir_x < grid.rows:
                if grid.cubes[y][x+(j*dir_x)].color == WHITE:
                    p2 =(x+(j*dir_x) ,y)
                    break
            if 0 < y+j*dir_y < grid.rows:
                if grid.cubes[y+(j*dir_y)][x].color == WHITE:
                    p2 =(x, y+(j*dir_y))
                    break
            
        pnts.append([p1, p2])
        pygame.draw.circle(WIN, (0, 255, 0), pos, 5)
    for point in pnts:
        p1, p2 = point[0], point[1]
        pygame.draw.line(WIN, (0,0,255), p1, p2)
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # draw(WIN, grid)
        pygame.display.update()

    pygame.quit()
    quit()
if __name__ == '__main__':
    main()