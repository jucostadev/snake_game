# UFCD: Projeto de tecnologias e programação de sistemas de informação
# Código: 5425
# Formandos: Júlia Costa, Lisandra Nair
# Data: 31.05.2024

import pygame
from random import randint
from sys import exit
import time

# start Pygame library
pygame.init()

# screen features
pygame.display.set_caption("Game - Snake")
pygame.display.set_icon(pygame.image.load("icon_snake.jpeg"))
WIDTH = 700
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# set color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (35, 142, 35)

# set variables
pixel_size = 20
game_speed = 10 # in milliseconds

# import images
apple = pygame.image.load("apple.png")
kiwi = pygame.image.load("Kiwi.png")

# set functions
def set_apple():
    apple_x = int(randint(0, WIDTH - apple.get_width()))
    apple_y = int(randint(0, HEIGHT - apple.get_height()))
    return apple_x, apple_y

def set_kiwi():
    kiwi_x = int(randint(0, WIDTH - kiwi.get_width()))
    kiwi_y = int(randint(0, HEIGHT - kiwi.get_height()))
    return kiwi_x, kiwi_y

# initial state of the game
score = 0
kiwi_timer = 0
game_over = False

# set game text fonts
score_font = pygame.font.Font("OCRAEXT.TTF", 25)
game_over_font = pygame.font.Font("OCRAEXT.TTF", 50)

# set game sounds
score_sound = pygame.mixer.Sound("coin.wav")
game_over_sound = pygame.mixer.Sound("game_over_sound.wav")
pygame.mixer.music.load("background_music.mp3")

# play background music
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.30)

# initial position and speed of the snake
pos_x_snake = WIDTH / 2
pos_y_snake = HEIGHT / 2
x_speed = 0
y_speed = 0
snake_size = 1 # number of pixels in the snake
pixels = []

# starting position of game foods
apple_x, apple_y = set_apple()
kiwi_x, kiwi_y = set_kiwi()

# main loop
while game_over == False:
    window.fill(BLACK)

    # game ending
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # interaction with pressing the keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        x_speed = 0
        y_speed = - pixel_size
    elif keys[pygame.K_DOWN]:
        x_speed = 0
        y_speed = pixel_size
    elif keys[pygame.K_LEFT]:
        X_speed = - pixel_size
        y_speed = 0
    elif keys[pygame.K_RIGHT]:
        x_speed = pixel_size
        y_speed = 0

    # redesign the game's foods
    replace_apple = window.blit(apple, (apple_x, apple_y))
    replace_kiwi = window.blit(kiwi, (kiwi_x, kiwi_y))

    # update snake position
    pos_x_snake += x_speed
    pos_y_snake += y_speed

    # update snake size
    pixels.append([pos_x_snake, pos_y_snake])
    if len(pixels) > snake_size:
        del pixels[0]

    # check collision with the snake itself
    for pixel in pixels[:-1]:
        if pixel == [pos_x_snake, pos_y_snake]:
            game_over = True

    # redesign the snake
    for pixel in pixels:
        snake = pygame.draw.rect(window, GREEN, [pixel[0], pixel[1], pixel_size, pixel_size])

    # check collision with screen boundaries
    if (pos_x_snake < 0 or pos_x_snake + pixel_size > WIDTH or pos_y_snake < 0 or pos_y_snake + pixel_size > HEIGHT):
        game_over = True

    # check collision with apple
    if snake.colliderect(replace_apple):
       apple = pygame.image.load("hide.png")
       apple_x, apple_y = set_apple()
       apple = pygame.image.load("apple.png")
       snake_size += 1
       score += 1
       score_sound.play()

    # check collision with kiwi
    if snake.colliderect(replace_kiwi):
       kiwi = pygame.image.load("hide.png")
       kiwi_x, kiwi_y = set_kiwi()
       kiwi = pygame.image.load("Kiwi.png")
       score_sound.play()
       snake_size += 1
       score += 2
       game_speed += 10
       kiwi_timer = time.time()

    # speed increase timer when eat kiwi
    if kiwi_timer > 0 and time.time() - kiwi_timer >= 5:
        game_speed = 15
        kiwi_timer = 0    

    # set score text fonts
    score_text = score_font.render(f"Pontuação:{score}", True, WHITE)
    window.blit(score_text, (10, 10))

    # set screen update
    pygame.display.update()
    clock.tick(game_speed)

# set "game over" screen
if game_over == True:
    window.fill(BLACK)
    game_over_text = game_over_font.render("FIM DO JOGO!", True, WHITE)
    window.blit(game_over_text, (175, 175))
    final_score_text = score_font.render(f"Pontuação final: {score}", True, WHITE)
    window.blit(final_score_text, (220, 250))
    game_over_sound.play()
    pygame.mixer.music.stop()

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
