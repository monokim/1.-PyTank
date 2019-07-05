import random
import math
import pygame
screen_width = 1200
screen_height = 800
class Tank:
    size = (50, 50)
    alive = True
    is_fire = False
    bullet = None
    def __init__(self, side, screen):
        self.side = side
        self.speed = 3
        if side == 0:
            self.position = [screen_width / 2, screen_height / 2]
            self.direction = [0, 0]
            self.color = (0, 0, 255)
        else:
            self.position = [random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)]
            self.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
            self.color = (255, 0, 0)
       
        self.shoot_delay = 0
        self.shoot_timer = 0
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.get_rect())
        if self.is_fire == True:
            self.bullet.draw()

    def draw_cannon(self, m_x, m_y):
        # draw cannon
        len = 50
        radians = math.degrees(math.atan2(m_y - self.position[1], m_x - self.position[0]))
        self.c_x = self.position[0] + 25 + math.cos(math.radians(radians)) * len
        self.c_y = self.position[1] + 25 + math.sin(math.radians(radians)) * len
        self.b_x = (self.c_x - (self.position[0] + 25)) / len
        self.b_y = (self.c_y - (self.position[1] + 25)) / len
        pygame.draw.line(self.screen, (0, 0, 0), (self.position[0] + 25, self.position[1] + 25), (self.c_x,self.c_y), 10)
    
    def move(self):
        if self.position[0] <= 0 or self.position[0] >= screen_width - 50:
            self.direction[0] *= -1
        if self.position[1] <= 0 or self.position[1] >= screen_height - 50:
            self.direction[1] *= -1
            
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed


    def fire(self):
        if self.is_fire == False:
            self.bullet = Bullet(self.screen, self.c_x, self.c_y, self.b_x, self.b_y)
            self.is_fire = True

    def get_rect(self):
        rect = pygame.Rect(self.position, self.size)
        return rect

    def update_status(self):
        if self.is_fire:
            if self.bullet.alive == False:
                del self.bullet
                self.is_fire = False

    def check_collision(self, rect):
        if self.is_fire:
            if rect.colliderect(self.bullet.rect):
                self.bullet.alive = 0
                return True
        return False

class Bullet:
    speed = 5
    alive = 1
    collision = 0
    def __init__(self, screen, x, y, d_x, d_y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.screen = screen
        self.direction = d_x * 10, d_y * 10

    def move(self):
        self.rect.move_ip(self.direction)
        self.check_status()

    def draw(self):
        self.move()
        pygame.draw.rect(self.screen, (0, 0, 255), self.rect)

    def check_status(self):
        if self.rect[0] <= 0 or self.rect[0] >= screen_width or \
            self.rect[1] <= 0 or self.rect[1] >= screen_height or self.collision:
            self.alive = 0   