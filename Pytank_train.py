import pygame
import Object
import Util
import Network
import math
import random

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return

screen_width = 1200
screen_height = 800
"""
def train_pytank():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)

    done = False
    my_tank = Object.Tank(0, screen)
    my_tank.speed = 0
    enemy = Object.Tank(1, screen)

    trained_count = 0
    game_speed = 15
    num_bullet = 100
    bullets = []
    flag_get_train_data = False
    train_input_data = [None] * num_bullet
    train_result_data = [None] * num_bullet
    model = Network.TwoLayerNet(4, 5, 3)

    enemy_was_at = []
    enemy_was_angle = 0
    while not done:
        # Check input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    game_speed -= 30
                    if game_speed < 0:
                        game_speed = 0
                elif event.key == pygame.K_PAGEUP:
                    game_speed += 30
                    if game_speed > 600:
                        game_speed = 600
                elif event.key == pygame.K_s:
                    model.save()
    
        if my_tank.is_fire == False:
            my_tank.fire()
            flag_get_train_data = True
            abs_angle = Util.get_angle(enemy.position.copy(), my_tank.position.copy())
            for i in range(num_bullet):
                b = Object.Bullet(screen, my_tank.position.copy())
                a1 = (b.angle - abs_angle + 360) % 360
                a2 = (abs_angle - b.angle + 360) % 360
                if a1 > a2:
                    big = a1
                    small = a2
                else:
                    big = a2
                    small = a1
                while small > 45 and big < 315:
                    b.set_new_direction()
                    a1 = (b.angle - abs_angle + 360) % 360
                    a2 = (abs_angle - b.angle + 360) % 360
                    if a1 > a2:
                        big = a1
                        small = a2
                    else:
                        big = a2
                        small = a1
                #print(abs_angle, b.angle, abs_angle - b.angle)
                bullets.append(b)
                data = [Util.get_distance(my_tank.position, enemy.position.copy()), 
                        bullets[i].angle, 
                        enemy.angle, 
                        abs_angle]
                train_input_data[i] = data
    
    
        my_tank.update_status()
        enemy.update_status()
        for i in range(len(bullets)):
            bullets[i].update_status()

        # check Status
        for i in range(len(bullets)):
            if Util.check_collision(enemy, bullets[i]):
                bullets[i].hit = True

        if flag_get_train_data and my_tank.is_fire:
            for i in range(len(bullets)):
                dist = Util.get_distance(bullets[i].position, enemy.position)
                if dist < bullets[i].min_dist:
                    bullets[i].min_dist = dist

        
        # update Status
        if flag_get_train_data:
            count = 0
            for i in range(len(bullets)):
                if train_result_data[i] != None:
                    count += 1
                elif bullets[i].alive == False:
                    abs_angle = Util.get_angle(enemy.position, my_tank.position)
                    p1 = (bullets[i].angle - abs_angle + 360) % 360
                    p2 = (abs_angle - bullets[i].angle + 360) % 360
                    left, right = 0, 0
                    if bullets[i].hit == 0:
                        if p1 > p2:
                            right = 1
                        else :
                            left = 1
                    data = [int(bullets[i].hit), left, right]
                    train_result_data[i] = data
                    count += 1
            if count == num_bullet:
                model.save_data(train_input_data, train_result_data)
                if model.data_count >= 10000:
                    break
                # init
                train_input_data = [None] * num_bullet
                train_result_data = [None] * num_bullet
                bullets.clear()
                trained_count += 1
                del enemy
                enemy = Object.Tank(1, screen)
                flag_get_train_data = False
                my_tank.is_fire = False
    

        # Update display
        screen.fill((255, 255, 255))
        text = font.render("Trained : " + str(trained_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        screen.blit(text, text_rect)

        text = font.render("Speed : " + str(game_speed / 30) + 'X', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (100, 50)
        screen.blit(text, text_rect)


        my_tank.draw()
        enemy.draw()
        for b in bullets:
            if b.alive:
                b.draw()

        pygame.display.flip()
        clock.tick(game_speed)
"""

def train_pytank_v2():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)

    done = False
    my_tank = Object.Tank(0, screen)
    my_tank.speed = 0
    enemy = Object.Tank(1, screen)

    trained_count = 0
    game_speed = 15
    num_bullet = 100
    bullets = []
    flag_get_train_data = False
    train_input_data = [None] * num_bullet
    train_result_data = [None] * num_bullet
    model = Network.TwoLayerNet(3, 10, 10, 3)
    is_start = False
    enemy_was_at = []
    enemy_was_angle = 0
    threshold = 30
    
    while not done:
        # Check input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    game_speed -= 30
                    if game_speed < 0:
                        game_speed = 0
                elif event.key == pygame.K_PAGEUP:
                    game_speed += 30
                    if game_speed > 300:
                        game_speed = 300
                elif event.key == pygame.K_SPACE:
                    is_start = True
    
        if is_start == False:
            continue

        if my_tank.is_fire == False:
            my_tank.fire()
            flag_get_train_data = True
            abs_angle = Util.get_angle(enemy.position.copy(), my_tank.position.copy())
            is_left = 0
            is_right = 0
            for i in range(num_bullet):
                b = Object.Bullet(screen, my_tank.position.copy())
                a1 = (b.angle - abs_angle + 360) % 360
                a2 = (abs_angle - b.angle + 360) % 360
                if a1 > a2:
                    big = a1
                    small = a2
                else:
                    big = a2
                    small = a1
                while small >= threshold and big <= 360 - threshold:
                    b.set_new_direction()
                    a1 = (b.angle - abs_angle + 360) % 360
                    a2 = (abs_angle - b.angle + 360) % 360
                    if a1 > a2:
                        big = a1
                        small = a2
                    else:
                        big = a2
                        small = a1
                bullets.append(b)
                is_left = 0
                is_right = 0
                if a1 > a2:
                    is_right = 1
                else :
                    is_left = 1
                
                data = [#Util.get_distance(my_tank.position, enemy.position), 
                        Util.normalize_angle(my_tank.angle), 
                        Util.normalize_angle(enemy.angle), 
                        Util.normalize_angle(Util.get_angle(enemy.position.copy(), my_tank.position.copy()))]

                #print(data)
                train_input_data[i] = data
    
    
        my_tank.update_status()
        enemy.update_status()
        for i in range(len(bullets)):
            bullets[i].update_status()

        # check Status
        for i in range(len(bullets)):
            if Util.check_collision(enemy, bullets[i]):
                bullets[i].hit = True

        # update Status
        if flag_get_train_data:
            count = 0
            for i in range(len(bullets)):
                if train_result_data[i] != None:
                    count += 1
                elif bullets[i].alive == False:
                    abs_angle = Util.get_angle(enemy.position, my_tank.position)
                    p1 = (bullets[i].angle - abs_angle + 360) % 360
                    p2 = (abs_angle - bullets[i].angle + 360) % 360
                    left, right = 0, 0
                    if bullets[i].hit == 0:
                        if p1 > p2:
                            right = 1
                        else :
                            left = 1
                    data = [left, right, int(bullets[i].hit)]
                    train_result_data[i] = data
                    count += 1
            if count == num_bullet:
                model.save_data(train_input_data, train_result_data)
                if model.data_count >= 10000:
                    break
                # init
                train_input_data = [None] * num_bullet
                train_result_data = [None] * num_bullet
                bullets.clear()
                trained_count += 1
                del enemy
                enemy = Object.Tank(1, screen)
                #if model.data_count >= 4000:
                    #enemy.speed = 0
                flag_get_train_data = False
                my_tank.is_fire = False
    
        """
        # Update display
        screen.fill((255, 255, 255))
        text = font.render("Trained : " + str(trained_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        screen.blit(text, text_rect)

        text = font.render("Speed : " + str(game_speed / 30) + 'X', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (100, 50)
        screen.blit(text, text_rect)


        my_tank.draw()
        enemy.draw()
        for b in bullets:
            if b.alive:
                b.draw()

        pygame.display.flip()
        clock.tick(game_speed)
        """

def train_pytank_avoid():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)

    done = False
    my_tank = Object.Tank(0, screen)
    my_tank.speed = 0
    enemy = Object.Tank(1, screen)

    trained_count = 0
    game_speed = 15
    num_bullet = 100
    bullets = []
    flag_get_train_data = False
    train_input_data = [None] * num_bullet
    train_result_data = [None] * num_bullet
    model = Network.TwoLayerNet(2, 10, 2)
    is_start = False
    is_fire = False
    threshold = 30
    
    while not done:
        # Check input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    game_speed -= 30
                    if game_speed < 0:
                        game_speed = 0
                elif event.key == pygame.K_PAGEUP:
                    game_speed += 30
                    if game_speed > 300:
                        game_speed = 300
                elif event.key == pygame.K_SPACE:
                    is_start = True
    
        if is_start == False:
            continue

        
        if is_fire == False:
            random_position = [random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)]
            my_tank.position = random_position
            for i in range(num_bullet):
                # random position
                random_position = [random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)]
                b = Object.Bullet(screen, random_position)
                b.set_new_direction()
                abs_angle = Util.get_angle(b.position.copy(), my_tank.position.copy())
                is_left = 0
                is_right = 0
                a1 = (b.angle - abs_angle + 360) % 360
                a2 = (abs_angle - b.angle + 360) % 360
                if a1 > a2:
                    big = a1
                    small = a2
                else:
                    big = a2
                    small = a1
                while small >= threshold and big <= 360 - threshold:
                    b.set_new_direction()
                    a1 = (b.angle - abs_angle + 360) % 360
                    a2 = (abs_angle - b.angle + 360) % 360
                    if a1 > a2:
                        big = a1
                        small = a2
                    else:
                        big = a2
                        small = a1

                b.angle -= 180
                bullets.append(b)
            
                # direction_bullet, abs_angle, distance, my_angle
                data = [Util.normalize_angle(Util.get_angle(my_tank.position.copy(), b.position.copy())),
                        Util.get_distance(my_tank.position.copy(), b.position.copy()) / 1400]
                train_input_data[i] = data
                is_fire = True
                flag_get_train_data = True
    
    
        my_tank.update_status()
        for i in range(len(bullets)):
            bullets[i].update_status()

        # check Status
        for i in range(len(bullets)):
            if Util.check_collision(my_tank, bullets[i]):
                bullets[i].hit = True

        # update Status
        if flag_get_train_data:
            count = 0
            for i in range(len(bullets)):
                if train_result_data[i] != None:
                    count += 1
                elif bullets[i].alive == False:
                    hit = int(bullets[i].hit)
                    avoid = 0
                    if hit == 0:
                        avoid = 1
                    data = [int(bullets[i].hit), avoid]
                    train_result_data[i] = data
                    count += 1
            if count == num_bullet:
                model.save_data(train_input_data, train_result_data)
                if model.data_count >= 500:
                    break
                if model.data_count == 250:
                    threshold = 3
                # init
                train_input_data = [None] * num_bullet
                train_result_data = [None] * num_bullet
                bullets.clear()
                trained_count += 1
                flag_get_train_data = False
                is_fire = False
    

        # Update display
        screen.fill((255, 255, 255))
        text = font.render("Trained : " + str(trained_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        screen.blit(text, text_rect)

        text = font.render("Speed : " + str(game_speed / 30) + 'X', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (100, 50)
        screen.blit(text, text_rect)


        my_tank.draw()
        for b in bullets:
            if b.alive:
                b.draw()

        pygame.display.flip()
        clock.tick(game_speed)
