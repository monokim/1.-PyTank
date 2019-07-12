import Object
import Util
import Network
import pygame
screen_width = 1200
screen_height = 800

def play_pytank():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)

    done = False
    my_tank = Object.Tank(0, screen)
    my_tank.speed = 0
    enemy = Object.Tank(1, screen)
    bullet = None

    game_speed = 30
    hit_count = 0
    fire_count = 0

    model = Network.TwoLayerNet(3, 5, 3)
    model.load_model()
    while not done:
        # Check input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    game_speed -= 30
                elif event.key == pygame.K_PAGEUP:
                    game_speed += 30
                if game_speed < 0:
                    game_speed = 0
                if game_speed > 150:
                    game_speed = 150
    
        
        data = [Util.get_distance(my_tank.position, enemy.position), 
                my_tank.angle, 
                enemy.angle, 
                Util.get_angle(enemy.position.copy(), my_tank.position.copy())]

        p = model.predict(data)
        i = p.index(max(p))
        print(p)
        print()
        if i == 0:
            #print("fire")
            if my_tank.is_fire == False:
                bullet = Object.Bullet(screen, [my_tank.c_x, my_tank.c_y], my_tank.angle)
                my_tank.is_fire = True
                fire_count += 1
        elif i == 1:
            #print("angle left")
            my_tank.angle += 3
        elif i == 2:
            #print("angle right")
            my_tank.angle -= 3
    
        my_tank.update_status()
        enemy.update_status()
        if my_tank.is_fire:
            bullet.update_status()
    
        
        # check Status
        if my_tank.is_fire:
            if Util.check_collision(enemy, bullet):
                hit_count += 1
                bullet.alive = False
                del enemy
                enemy = Object.Tank(1, screen)

        if my_tank.is_fire:
            if bullet.alive == False:
                del bullet
                my_tank.is_fire = False

        # Update display
        screen.fill((255, 255, 255))
        text = font.render("hit : " + str(hit_count) + "/" + str(fire_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        screen.blit(text, text_rect)

        text = font.render("Speed : " + str(game_speed / 30) + 'X', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (100, 50)
        screen.blit(text, text_rect)

        my_tank.draw()
        enemy.draw()
        if my_tank.is_fire:
            if bullet.alive:
                bullet.draw()
    
        pygame.display.flip()
        clock.tick(game_speed)

def play_pytank_v2():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)

    done = False
    my_tank = Object.Tank(0, screen)
    my_tank.speed = 0
    enemy = Object.Tank(1, screen)
    bullet = None

    game_speed = 30
    hit_count = 0
    fire_count = 0

    model = Network.TwoLayerNet(4, 5, 3)
    model.load_model()
    while not done:
        # Check input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    game_speed -= 30
                elif event.key == pygame.K_PAGEUP:
                    game_speed += 30
                if game_speed < 0:
                    game_speed = 0
                if game_speed > 150:
                    game_speed = 150
    
        abs_angle = Util.get_angle(enemy.position.copy(), my_tank.position.copy())
        a1 = (my_tank.angle - abs_angle + 360) % 360
        a2 = (abs_angle - my_tank.angle + 360) % 360
        is_right = 0
        is_left = 0
        is_range = 0
        if a1 > a2:
            is_right = 1 
            big = a1
            small = a2
        else:
            is_left = 1 
            big = a2
            small = a1

        if small <= 10 and big >= 350:
            is_range = 1

        data = [is_left, is_right, is_range, (abs_angle - 180.0) / 360]
        #print(data)

        p = model.predict(data)
        i = p.index(max(p))
        print(p)
        if i == 0:
            #print("angle left")
            my_tank.angle -= 3
        elif i == 1:
            #print("angle right")
            my_tank.angle += 3
        if p[i] >= 0.3:
            #print("fire")
            if my_tank.is_fire == False:
                bullet = Object.Bullet(screen, [my_tank.c_x, my_tank.c_y], my_tank.angle)
                my_tank.is_fire = True
                fire_count += 1
    
        my_tank.update_status()
        enemy.update_status()
        if my_tank.is_fire:
            bullet.update_status()
    
        if fire_count >= 30:
            break

        # check Status
        if my_tank.is_fire:
            if Util.check_collision(enemy, bullet):
                hit_count += 1
                bullet.alive = False
                del enemy
                enemy = Object.Tank(1, screen)

        if my_tank.is_fire:
            if bullet.alive == False:
                del bullet
                my_tank.is_fire = False

        # Update display
        screen.fill((255, 255, 255))
        text = font.render("hit : " + str(hit_count) + "/" + str(fire_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        screen.blit(text, text_rect)

        text = font.render("Speed : " + str(game_speed / 30) + 'X', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (100, 50)
        screen.blit(text, text_rect)

        my_tank.draw()
        enemy.draw()
        if my_tank.is_fire:
            if bullet.alive:
                bullet.draw()
    
        pygame.display.flip()
        clock.tick(game_speed)


def control_pytank():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)

    done = False
    my_tank = Object.Tank(0, screen)
    my_tank.speed = 0
    enemy = Object.Tank(1, screen)
    bullet = None

    game_speed = 30
    hit_count = 0
    fire_count = 0

    while not done:
        # Check input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    game_speed -= 30
                elif event.key == pygame.K_PAGEDOWN:
                    game_speed += 30
                if game_speed < 0:
                    game_speed = 0
                if game_speed > 150:
                    game_speed = 150
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    my_tank.speed = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            my_tank.angle -= 5
        if keys[pygame.K_RIGHT]:
            my_tank.angle += 5
        if keys[pygame.K_UP]:
            my_tank.speed = 10
        if keys[pygame.K_DOWN]:
            my_tank.speed = -10
        if keys[pygame.K_SPACE]:
            if my_tank.is_fire == False:
                bullet = Object.Bullet(screen, [my_tank.c_x, my_tank.c_y], my_tank.angle)
                my_tank.is_fire = True
                fire_count += 1
        
        my_tank.update_status()
        enemy.update_status()
        if my_tank.is_fire:
            bullet.update_status()
        
        # check Status
        if my_tank.is_fire:
            if Util.check_collision(enemy, bullet):
                hit_count += 1
                bullet.alive = False
                del enemy
                enemy = Object.Tank(1, screen)

        if my_tank.is_fire:
            if bullet.alive == False:
                del bullet
                my_tank.is_fire = False

        # Update display
        screen.fill((255, 255, 255))
        text = font.render("hit : " + str(hit_count) + "/" + str(fire_count), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        screen.blit(text, text_rect)

        text = font.render("Speed : " + str(game_speed / 30) + 'X', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (100, 50)
        screen.blit(text, text_rect)

        my_tank.draw()
        enemy.draw()
        if my_tank.is_fire:
            if bullet.alive:
                bullet.draw()
    
        pygame.display.flip()
        clock.tick(game_speed)
