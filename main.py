import sys
import pygame
import random
import os
from player import Player
from coin import Coin
from enemy import Enemy

#initialize and setup screen
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('The Official Salmon Friends Game')

black_color = pygame.Color(0, 0, 0)
white_color = pygame.Color(255, 255, 255)
blue_color = pygame.Color(0, 0, 255)
bg_color = pygame.Color(64, 179, 214)
red_color = pygame.Color(255, 0, 0)

font = pygame.font.SysFont('arial', 36)

#create player sprite and add to player group
sam = Player(os.path.join('assets', 'salmonsam.png'), os.path.join('assets', 'salmonsamleft.png'), 0, height, 100, width, height)
player = pygame.sprite.Group()
player.add(sam)

#create coin and enemy groups
coin_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()

speed = 150
tsangmod = 3
score = 0
high_score = 0

#create booleans so that the game knows to create an enemy and coin upon startup
enemy_exists = False
coin_exists = False
new_game = False
tsanger = False

enemy_sound = pygame.mixer.Sound(os.path.join('assets', 'bear.wav'))
coin_sound = pygame.mixer.Sound(os.path.join('assets', 'coin.wav'))
bonus_sound = pygame.mixer.Sound(os.path.join('assets', 'bonus.wav'))
tsang_sound = pygame.mixer.Sound(os.path.join('assets', 'tsanger.wav'))


while True:
    if not tsanger:
        screen.fill(bg_color)
    else:
        screen.fill(red_color)
    dt = clock.tick(60)
    dt = 1 / float(dt)

    scoreboard = font.render("Score: " + str(score), False, black_color)
    score_rect = scoreboard.get_rect()
    score_rect.topleft = 25, 0
    screen.blit(scoreboard, score_rect)

    highscoreboard = font.render("Hi: " + str(high_score), False, black_color)
    highscore_rect = highscoreboard.get_rect()
    highscore_rect.topleft = 26, (score_rect.bottom + 2)
    screen.blit(highscoreboard, highscore_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #Quit on escape press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            #search for keys pressed down to initiate movement
            if event.key == pygame.K_UP:
                sam.move_up = True
            if event.key == pygame.K_RIGHT:
                sam.move_right = True
            if event.key == pygame.K_LEFT:
                sam.move_left = True
            if event.key == pygame.K_DOWN:
                sam.move_down = True

            #restart game on R press
            if event.key == pygame.K_r:
                score = 0
                for enemy in enemy_group:
                    enemy.kill()
                for coin in coin_group:
                    coin.kill()
                enemy_exists = False
                coin_exists = False
                tsanger = False
                sam.speed = speed
                enemy.speedx = speed
                enemy.speedy = speed
                screen.fill(bg_color)


        #search for keys released to stop movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                sam.move_up = False
            if event.key == pygame.K_LEFT:
                sam.move_left = False
            if event.key == pygame.K_RIGHT:
                sam.move_right = False
            if event.key == pygame.K_DOWN:
                sam.move_down = False

    #if no enemy exists, create one with random x and y position
    if not enemy_exists:
        enemy_x = random.randint(0, width)
        enemy_y = random.randint(0, height)
        enemy = Enemy(os.path.join('assets', 'bear.png'), enemy_x, enemy_y, 150, 150, width, height)
        enemy_group.add(enemy)
        enemy_exists = True

    #if no coin exists, create one with random x and y position
    if not coin_exists:
        random.seed()
        coin_x = random.randint(0, width)
        coin_y = random.randint(0, height)
        coin_num = random.randint(1, 10)
        coin_exists = True
        if coin_num == 10:
            phil = Coin(os.path.join('assets', 'phil.png'), coin_x, coin_y)
            coin_group.add(phil)
            phil.tsang = True
        elif coin_num == 9:
            regi = Enemy(os.path.join('assets', 'regi.png'), coin_x, coin_y, 200, 200, width, height)
            bonus_group.add(regi)
        else:
            coin = Coin(os.path.join('assets', 'coin{}.png'.format(str(coin_num))), coin_x, coin_y)
            coin_group.add(coin)
            coin.tsang = False


    #check for coin hits
    coin_hits = pygame.sprite.spritecollide(sam, coin_group, True)
    for coin in coin_hits:
        #play sound and add 10 to score for every hit, change boolean to tell game to create new coin
        #sam = sam.grow(1.2)
        coin_exists = False
        score += 10
        if coin.tsang:
            tsang_sound.play()
            tsanger = True
            sam.speed *= tsangmod
            enemy.speedx *= tsangmod
            enemy.speedy *= tsangmod
        else:
            coin_sound.play()
            sam.speed = speed
            if tsanger:
                enemy.speedx /= tsangmod
                enemy.speedy /= tsangmod
                tsanger = False
        if score > high_score:
            high_score = score

    #check for bonus hits
    bonus_hits = pygame.sprite.spritecollide(sam, bonus_group, True)
    for bonus in bonus_hits:
        #play sound and add 50 points, change booleans
        #sam = sam.grow(1.2)
        bonus_sound.play()
        coin_exists = False
        score += 50
        if tsanger:
            enemy.speedx /= tsangmod
            enemy.speedy /= tsangmod
            tsanger = False
        if score > high_score:
            high_score = score

    #check for enemy hits
    enemy_hits = pygame.sprite.spritecollide(sam, enemy_group, True)
    for enemy in enemy_hits:
        #if we hit an enemy, play sound and end game
        enemy_sound.play()
        for coin in coin_group:
            coin.kill()
        for bonus in bonus_group:
            bonus.kill()
        if tsanger:
            enemy.speedx /= tsangmod
            enemy.speedy /= tsangmod
            tsanger = False
        new_game = False

    player.update(dt)
    player.draw(screen)

    coin_group.draw(screen)

    bonus_group.update(dt)
    bonus_group.draw(screen)


    enemy_group.update(dt)
    enemy_group.draw(screen)

    pygame.display.update()

