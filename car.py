import os 
import math
import pygame
from timer import Timer

CAR_WIDTH, CAR_HEIGHT = 20, 20
(WIN_WIDTH, WIN_HEIGHT) = (600, 600)
OUTER_COLOR = (255, 255, 255, 255)


CAR_IMAGE = pygame.image.load(os.path.join("assets", "car.png"))
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))

def calc_dis(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1)**2)

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))/2)

def colors_are_similar(c1, c2):
    # return c1 == c2
    try:
        r1, g1, b1, _ = c1
        r2, g2, b2, _ = c2 
        leenance = 5
        if (abs(r1 - r2) < leenance) and (abs(g1 - g2) < leenance) and (abs(b1 -b2) < leenance):
            return True
        else:
            return False
    except TypeError as e:
        print(e)
        return False

class Car:
    def __init__(self, x, y):
        self.pos_ = [x, y]
        self.previous_pos_ = [x, y]

        self.image_ = CAR_IMAGE
        self.blit_img_ = self.image_
        self.center_ = (self.pos_[0] +(CAR_HEIGHT/2), self.pos_[1]+(CAR_HEIGHT/2))

        self.alive_ = True
        self.speed_set_ = False
    
        self.angle = 0 
        self.vel = 5
        self.radars = []

        self.distance_covered = 0 
        self.time_alive = 0
        self.score_timer = Timer(time=0.1, func=lambda : self.add_score(), loop=True)
        self.score_timer.start_timer()

        self.score = 0
        self.score_points = None
        self.passed_point = 0

    def draw(self, win):
        win.blit(self.blit_img_, self.pos_)
        # self.draw_radar(win) 

    def draw_radar(self, win):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(win, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(win, (0, 255, 0), position, 5)
    
    def check_collision(self, track):
        # self.alive = True
        for point in self.corners:
            if colors_are_similar(track.get_at((int(point[0]), int(point[1]))) ,OUTER_COLOR):
                self.alive_ = False

    def is_alive(self):
        return self.alive_

    def update_radar(self, degree, track):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not colors_are_similar( track.get_at((x, y)), OUTER_COLOR) and length < WIN_WIDTH/2:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self, track, win):
        # Set The Speed To 20 For The First Time
        # Only When Having 4 Output Nodes With Speed Up and Down
        if not self.speed_set_:
            self.speed = 3
            self.speed_set_ = True

        # Get Rotated Sprite And Move Into The Right X-Direction
        # Don't Let The Car Go Closer Than 20px To The Edge
        self.blit_img_= self.rotate_center(self.image_, self.angle)
        self.pos_[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos_[0] = max(self.pos_[0], 20)
        self.pos_[0] = min(self.pos_[0], WIN_WIDTH - CAR_WIDTH)

        self.pos_[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.pos_[1] = max(self.pos_[1], 20)
        self.pos_[1] = min(self.pos_[1], WIN_WIDTH-CAR_HEIGHT)

        #updating score 
        self.score_timer.update()
        # self.distance_covered += self.vel
        (x2, y2),(x3, y3) = self.score_points[self.passed_point]
        x1, y1 = self.pos_ 
        # ar = area(x1, y1, x2, y2, x3, y3)
        d1 = calc_dis(x1, y1, x2, y2)
        d2 = calc_dis(x1, y1, x3, y3)
        d3 = calc_dis(x3, y3, x2, y2)

        dis = 1.414*d3-(d1+d2)
        # print(dis)

        pnts = [(x1,y1), (x2,y2), (x3,y3)]
        # ar = area(x1, y1, x2, y2, x3, y3)
        # pygame.draw.polygon(surface=win, color=(255,0,0), points=pnts)
        # print(ar)
        if dis >0:
            self.score += 10 
            self.passed_point += 1
            self.passed_point %= len(self.score_points)


        # Calculate New Center
        self.center = [int(self.pos_[0]) + CAR_WIDTH / 2, int(self.pos_[1]) + CAR_HEIGHT / 2]

        # Setting corners
        length = CAR_WIDTH/2
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision(track)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 45):
            self.update_radar(d, track)

    def rotate_center(self, image, angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image
    
    def add_time(self):
        self.time_alive += 1
    
    def get_dis(self):
        out = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            out[i] = radar[1]

        return out
        # return [radar[1]/30 for radar in self.radars]
    
    def get_score(self):
        return self.score
        # return self.score
    
    def add_score(self):
        # x,y = self.pos_
        # xprev, yprev = self.previous_pos_

        # dis = calc_dis(x,y, xprev,yprev)

        # # self.prev_pos_ = self.pos_
        # self.score += dis
        # self.distance_covered += int(dis)
        self.distance_covered = self.score