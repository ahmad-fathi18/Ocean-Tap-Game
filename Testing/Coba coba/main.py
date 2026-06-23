import pygame
import time
import os
import random
from sys import exit


# Game variabel
GAME_WIDTH = 360  
GAME_HEIGHT = 640  

# bird class
bird_x = GAME_WIDTH / 8
bird_y = GAME_HEIGHT / 2
bird_width = 34
bird_height = 24


class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img


# Pipe class
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512


class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False


# Game images
backround_image = pygame.image.load("asset/bg.png")
bird_image = pygame.image.load("asset/flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load("asset/toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bot_pipe_image = pygame.image.load("asset/bottompipe.png")
bot_pipe_image = pygame.transform.scale(bot_pipe_image, (pipe_width, pipe_height))


# game logic
bird = Bird(bird_image)
pipes = []
velocity_x = -2  # Untuk memindahkan koordinat dari pipa seolah olah embuat burungnya bergerak padahal pipanya yang geser ke kiri
velocity_y = 0  # Menggerakkan burung ke atas dan ke bawah
gravity = 0.4
score = 0
game_over = False


def draw():
    window.blit(backround_image, (0, 0))  # (0, 0) posisi awal
    window.blit(bird_image, bird)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    text_str = str(int(score))
    if game_over:
        text_str = "Game Over: " + text_str

    text_font = pygame.font.SysFont("comic sans MS", 45)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))


def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > GAME_HEIGHT:
        game_over = True
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and bird.x > pipe.x + pipe_width:
            score += 0.5
            pipe.passed = True

        if bird.colliderect(pipe):
            game_over = True
            return

    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(
            0
        )  # Menghilangkan pipa yang sudah melewati burung untuk mengurangi beban kerja computer


def Create_Pipes():
    random_pipe_y = pipe_y - pipe_height / 4 - random.random() * (pipe_height / 2)
    opening_space = GAME_HEIGHT / 4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bot_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)

    print(len(pipes) / 2)


pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy bird")  # Judul
clock = pygame.time.Clock()  # Variabel waktu dengan memanfaatkan fungsi pygame

Create_Pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(Create_Pipes_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Tombol "X" diatas
            pygame.quit()  # Menutup semua program di pygame
            exit()  # Close jendela

        if event.type == Create_Pipes_timer and not game_over:
            Create_Pipes()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                velocity_y = -6

                # Reset game over
                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    game_over = False

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60)  # Set 60 fps
