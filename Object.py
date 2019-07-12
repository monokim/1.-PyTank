import random
import math
import pygame
screen_width = 1200
screen_height = 800
class Tank:
    size = 30
    alive = True
    is_fire = False
    bullet = None
    accel = 0
    speed = 10
    c_len = 50
    def __init__(self, side, screen):
        self.side = side
        self.screen = screen
        if side == 0:
            self.position = [screen_width // 2, screen_height // 2]
            self.color = (0, 0, 255)
        else:
            self.position = [random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)]
            self.color = (255, 0, 0)
            
        self.angle = (math.degrees(math.atan2(random.uniform(-1, 1), random.uniform(-1, 1))) + 360) % 360
        self.c_x = self.position[0] + math.cos(math.radians(self.angle)) * self.c_len    # cannon_x
        self.c_y = self.position[1] + math.sin(math.radians(self.angle)) * self.c_len    # cannon_y
    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], self.size)
        if self.side == 0:
            self.draw_cannon()

    def draw_cannon(self):
        # draw cannon
        pygame.draw.line(self.screen, (0, 0, 0), (self.position[0], self.position[1]), (self.c_x,self.c_y), 10)
    
    def move(self):
        self.position[0] += math.cos(math.radians(self.angle)) * self.speed
        self.position[1] += math.sin(math.radians(self.angle)) * self.speed

    def fire(self):
        if self.is_fire == False:
            self.is_fire = True

    def check_status(self):
        self.angle = (self.angle + 360) % 360
        direction = [math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))]
        if self.position[0] <= 0 or self.position[0] >= screen_width - 50:
            direction[0] *= -1
            self.angle = (math.degrees(math.atan2(direction[1], direction[0])) + 360) % 360
        
        if self.position[1] <= 0 or self.position[1] >= screen_height - 50:
            direction[1] *= -1
            self.angle = (math.degrees(math.atan2(direction[1], direction[0])) + 360) % 360

        self.c_x = self.position[0] + math.cos(math.radians(self.angle)) * self.c_len    # cannon_x
        self.c_y = self.position[1] + math.sin(math.radians(self.angle)) * self.c_len    # cannon_y
  

    def update_status(self):
        self.check_status()
        self.move()


class Bullet:
    speed = 30
    alive = 1
    angle = 0
    size = 5

    # for train
    min_dist = 9999
    hit = False

    def set_new_direction(self):
        self.angle = (math.degrees(math.atan2(random.uniform(-1, 1), random.uniform(-1, 1))) + 360) % 360

    def __init__(self, screen, position, angle = 0):
        self.screen = screen
        self.position = position
        if angle == 0:
            self.angle = (math.degrees(math.atan2(random.uniform(-1, 1), random.uniform(-1, 1))) + 360) % 360
        else:
            self.angle = angle

    def move(self):
        self.position[0] += math.cos(math.radians(self.angle)) * self.speed
        self.position[1] += math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 0), [int(self.position[0]), int(self.position[1])], self.size)

    def check_status(self):
        if self.position[0] <= 0 or self.position[0] >= screen_width or \
            self.position[1] <= 0 or self.position[1] >= screen_height:
            self.alive = 0
    
    def update_status(self):
        self.check_status()
        self.move()
