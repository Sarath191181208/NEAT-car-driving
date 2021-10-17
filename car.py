import os 
import pygame

CAR_WIDTH, CAR_HEIGHT = 30, 30

CAR_IMAGE = pygame.image.load(os.path.join("assets", "car.png"))
CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (CAR_WIDTH, CAR_HEIGHT))

class Car:
    def __init__(self, x, y):
        self.pos_ = (x, y)

        self.image_ = CAR_IMAGE
        self.center_ = (self.pos_[0] +(CAR_HEIGHT/2), self.pos_[1]+(CAR_HEIGHT/2))
        self.angle = 0 

        self.vel = 5


        self.alive_ = True
    
    def draw(self, win):
        win.blit(self.image_, self.pos_)

    def is_alive(self):
        return self.alive_

    def rotate_center(self, image, angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image