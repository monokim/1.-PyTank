import pygame
import Object
import Util
import Network


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
    enemy.speed = 0

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
            is_left = 0
            is_right = 0
            is_range = 0
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
                while small > 15 and big < 345:
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
                if a1 > a2:
                    is_right = 1
                else :
                    is_left = 1
                if small <= 10 and big >= 350:
                    is_range = 1
                data = [is_left, is_right, is_range, (abs_angle - 180.0) / 360]
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
                if model.data_count >= 1000:
                    break
                # init
                train_input_data = [None] * num_bullet
                train_result_data = [None] * num_bullet
                bullets.clear()
                trained_count += 1
                del enemy
                enemy = Object.Tank(1, screen)
                enemy.speed = 0
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
