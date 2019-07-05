import pygame
import Tank
import pyautogui
screen_width = 1200
screen_height = 800

def check_status(tanks):
    count = 0
    for t in tanks:
        count += t.alive
    return count

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)


done = False
tanks = []
my_tank = Tank.Tank(0, screen)
num_tanks = 10
for i in range(num_tanks):
    tanks.append(Tank.Tank(1, screen))

while not done:
    # Check input
    m_x, m_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        my_tank.fire()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_UP:
                pass
            if event.key == pygame.K_DOWN:
                pass

    # set screen
    screen.fill((255, 255, 255))
    text = font.render("Remain : " + str(len(tanks)), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (1000, 50)
    screen.blit(text, text_rect)

    my_tank.draw()
    my_tank.draw_cannon(m_x, m_y)
    for t in tanks:
        t.draw()
    
            

    # Do something
    for t in tanks:
        if t.alive:
            t.move()


    # check Status
    for i in range(len(tanks)-1, -1, -1):
        if my_tank.check_collision(tanks[i].get_rect()):
            del tanks[i]
    
    if len(tanks) == 0:
        print("no tanks")
        for i in range(num_tanks):
            tanks.append(Tank.Tank(1, screen))
    
    my_tank.update_status()
    for t in tanks:
        t.update_status()

    # Update display
    pygame.display.flip()
    clock.tick(60)
