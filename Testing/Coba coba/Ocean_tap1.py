import pygame
import time
import os
import random
from sys import exit

# Game variabel
GAME_WIDTH = 360
GAME_HEIGHT = 640

# Ukuran default burung
kapal_x = GAME_WIDTH / 8
kapal_y = GAME_HEIGHT / 2
kapal_width = 54
kapal_height = 44


class KapalSelam(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, kapal_x, kapal_y, kapal_width, kapal_height)
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


# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Ocean Tap")
clock = pygame.time.Clock()
pygame.mixer.init()

# AUDIO SETTING
pygame.mixer.music.load("asset/sekuora-funny-bgm-240795.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
suara_lompat = pygame.mixer.Sound("asset/bestuploadsever67aryan-jump-sound-531048.mp3")
suara_lompat.set_volume(0.5)

# Game images
backround_image = pygame.image.load("asset/background.png")
kapal_original = pygame.image.load("asset/kapalselam.png")
kapal_image = pygame.transform.scale(kapal_original, (kapal_width, kapal_height))

top_pipe_image = pygame.image.load("asset/top.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bot_pipe_image = pygame.image.load("asset/bottom.png")
bot_pipe_image = pygame.transform.scale(bot_pipe_image, (pipe_width, pipe_height))

# Font
text_font = pygame.font.SysFont("courier new", 25)
title_font = pygame.font.SysFont("courier new", 45)
game_over_font = pygame.font.SysFont("courier new", 35)
game_over_text = pygame.font.SysFont("courier new", 16)


# Game logic & States
# Status: "MAIN_MENU", "PLAYING", "GAME_OVER"
game_state = "MAIN_MENU"

kapal_selam = KapalSelam(kapal_image)
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
score = 0

# Highscore
HIGHSCORE_FILE = "highscore.txt"


def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0


def save_highscore(value):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(value))


highscore = load_highscore()

# Menu Navigasi indeks
menu_options = ["Mulai", "Keluar"]
menu_index = 0


def reset_game():
    global pipes, score, velocity_y, kapal_selam
    kapal_selam.y = kapal_y
    velocity_y = 0
    pipes.clear()
    score = 0


def Create_Pipes():
    random_pipe_y = pipe_y - pipe_height / 4 - random.random() * (pipe_height / 2)
    opening_space = GAME_HEIGHT / 4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.x = GAME_WIDTH
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bot_pipe_image)
    bottom_pipe.x = GAME_WIDTH
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)


def move():
    global velocity_y, score, game_state, highscore
    velocity_y += gravity
    kapal_selam.y += velocity_y
    kapal_selam.y = max(kapal_selam.y, 0)

    if kapal_selam.y > GAME_HEIGHT:
        game_state = "GAME_OVER"
        if int(score) > highscore:
            highscore = int(score)
            save_highscore(highscore)
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and kapal_selam.x > pipe.x + pipe_width:
            score += 0.5
            pipe.passed = True

        if kapal_selam.colliderect(pipe):
            game_state = "GAME_OVER"
            if int(score) > highscore:
                highscore = int(score)
                save_highscore(highscore)
            return

    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)


def draw_menu():
    window.blit(backround_image, (0, 0))

    # Judul Game
    title_render = title_font.render("OCEAN TAP", True, "orange")
    window.blit(title_render, (GAME_WIDTH // 2 - title_render.get_width() // 2, 80))

    # Menggambar Opsi Menu
    for i, option in enumerate(menu_options):
        color = "yellow" if i == menu_index else "white"
        text = f"> {option} <" if i == menu_index else option
        option_render = text_font.render(text, True, color)
        window.blit(
            option_render,
            (GAME_WIDTH // 2 - option_render.get_width() // 2, 250 + i * 60),
        )

    hs_render = text_font.render(f"Highscore: {highscore}", True, "white")
    window.blit(hs_render, (GAME_WIDTH // 2 - hs_render.get_width() // 2, 160))


def draw_game():
    window.blit(backround_image, (0, 0))
    window.blit(kapal_selam.img, kapal_selam)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    text_str = str(int(score))
    text_render = title_font.render(text_str, True, "white")
    window.blit(text_render, (GAME_WIDTH // 2 - text_render.get_width() // 2, 20))


def draw_game_over():
    draw_game()

    go_render = game_over_font.render("GAME OVER", True, "red")

    score_render = game_over_text.render(f"Skor Akhir: {int(score)}", True, "white")
    hs_render = game_over_text.render(f"Highscore: {highscore}", True, "orange")
    restart_render = game_over_text.render("[SPACE] untuk Main Lagi", True, "yellow")
    menu_render = game_over_text.render("[M] ke Menu Utama", True, "white")

    window.blit(go_render, (GAME_WIDTH // 2 - go_render.get_width() // 2, 180))
    window.blit(score_render, (GAME_WIDTH // 2 - score_render.get_width() // 2, 240))
    window.blit(hs_render, (GAME_WIDTH // 2 - hs_render.get_width() // 2, 280))
    window.blit(
        restart_render, (GAME_WIDTH // 2 - restart_render.get_width() // 2, 360)
    )
    window.blit(menu_render, (GAME_WIDTH // 2 - menu_render.get_width() // 2, 410))


# Timer Custom Event untuk Pipa
Create_Pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(Create_Pipes_timer, 1500)

# Game Loop Utama
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Timer pipa hanya bekerja saat kondisi sedang bermain (PLAYING)
        if event.type == Create_Pipes_timer and game_state == "PLAYING":
            Create_Pipes()

        if event.type == pygame.KEYDOWN:
            if game_state == "MAIN_MENU":
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(menu_options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if menu_index == 0:  # Mulai
                        reset_game()
                        game_state = "PLAYING"
                    elif menu_index == 1:  # Keluar
                        pygame.quit()
                        exit()

            # LOGIK SAAT BERMAIN
            elif game_state == "PLAYING":
                if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                    velocity_y = -6
                    suara_lompat.play()

            # LOGIK GAME OVER
            elif game_state == "GAME_OVER":
                if event.key == pygame.K_SPACE:  # Opsi Restart Langsung
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_m:  # Opsi Kembali Ke Menu Utama
                    game_state = "MAIN_MENU"

    # RENDER & UPDATE BERDASARKAN STATUS
    if game_state == "MAIN_MENU":
        draw_menu()
    elif game_state == "PLAYING":
        move()
        draw_game()
    elif game_state == "GAME_OVER":
        draw_game_over()

    pygame.display.update()
    clock.tick(60)
