import pygame
from pygame import mixer
import math
import random


pygame.init()

screen = pygame.display.set_mode((1080, 800))

background = pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 530
playerY = 700
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 1015))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

missleImg = pygame.image.load('missle.png')
missleX = 0
missleY = 700
missleX_change = 0.1
missleY_change = 1
missle_state = "ready"

score_value = 0
font = pygame.font.Font('Eracake.ttf', 64)

textX = 10
textY = 10

over_font = pygame.font.Font('Eracake.ttf', 120)

def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (175, 400))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_missle(x, y):
    global missle_state
    missle_state = "fire"
    screen.blit(missleImg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, MissleX, Missley):
    distance = math.sqrt((math.pow(enemyX - missleX, 2)) + (math.pow(enemyY - missleY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = +0.3
            if event.key == pygame.K_SPACE:
                if missle_state is "ready":
                    missle_sound = mixer.Sound('missle.wav')
                    missle_sound.play()
                    missleX = playerX
                    fire_missle(missleX, missleY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 1016:
        playerX = 1016

    for i in range(num_of_enemies):

        if enemyY[i] > 630:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1016:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], missleX, missleY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            missleY = 700
            missle_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 1015)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    if missleY <= 0:
        missleY = 700
        missle_state = "ready"
    if missle_state is "fire":
        fire_missle(missleX, missleY)
        missleY -= missleY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
