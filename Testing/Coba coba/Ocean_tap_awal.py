import pygame
import time
import os
import random
from sys import exit

# ============ KONFIGURASI DASAR ============
GAME_WIDTH = 360
GAME_HEIGHT = 640

# Ukuran & posisi default submarine
sub_x = GAME_WIDTH / 8
sub_y = GAME_HEIGHT / 2
sub_width = 54
sub_height = 44

# Ukuran & posisi default pipe
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512


# ============ CLASS ============
class Submarine(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, sub_x, sub_y, sub_width, sub_height)
        self.img = img


class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False


# ============ INISIALISASI PYGAME ============
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Ocean Tap")
clock = pygame.time.Clock()
pygame.mixer.init()

# Audio
pygame.mixer.music.load("asset/sekuora-funny-bgm-240795.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound("asset/bestuploadsever67aryan-jump-sound-531048.mp3")
jump_sound.set_volume(0.5)

# Gambar/asset
background_image = pygame.image.load("asset/background.png")
sub_original = pygame.image.load("asset/kapalselam.png")
sub_image = pygame.transform.scale(sub_original, (sub_width, sub_height))

top_pipe_image = pygame.image.load("asset/top.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bot_pipe_image = pygame.image.load("asset/bottom.png")
bot_pipe_image = pygame.transform.scale(bot_pipe_image, (pipe_width, pipe_height))

# Font
text_font = pygame.font.SysFont("m5x7", 25)
title_font = pygame.font.SysFont("m5x7", 45)
game_over_font = pygame.font.SysFont("m5x7", 35)
game_over_text = pygame.font.SysFont("m5x7", 16)


# ============ STATE & VARIABEL GAME ============
# game_state: "MAIN_MENU", "PLAYING", "GAME_OVER"
game_state = "MAIN_MENU"

submarine = Submarine(sub_image)
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
score = 0

menu_options = ["Mulai", "Keluar"]
menu_index = 0

# Highscore disimpan ke file biar tetap ada walau game ditutup
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


# ============ FUNGSI GAME LOGIC ============
def reset_game():
    global pipes, score, velocity_y, submarine
    submarine.y = sub_y
    velocity_y = 0
    pipes.clear()
    score = 0


def create_pipes():
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


def check_highscore():
    global highscore
    if int(score) > highscore:
        highscore = int(score)
        save_highscore(highscore)


def move():
    global velocity_y, score, game_state
    velocity_y += gravity
    submarine.y += velocity_y
    submarine.y = max(submarine.y, 0)

    # Submarine jatuh keluar layar -> game over
    if submarine.y > GAME_HEIGHT:
        game_state = "GAME_OVER"
        check_highscore()
        return

    for pipe in pipes:
        pipe.x += velocity_x

        # Tambah skor saat berhasil melewati pipa
        if not pipe.passed and submarine.x > pipe.x + pipe_width:
            score += 0.5
            pipe.passed = True

        # Tabrakan dengan pipa -> game over
        if submarine.colliderect(pipe):
            game_state = "GAME_OVER"
            check_highscore()
            return

    # Buang pipa yang sudah keluar dari layar
    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)


# ============ FUNGSI RENDER/DRAW ============
def draw_menu():
    window.blit(background_image, (0, 0))

    title_render = title_font.render("OCEAN TAP", True, "orange")
    window.blit(title_render, (GAME_WIDTH // 2 - title_render.get_width() // 2, 80))

    hs_render = text_font.render(f"Highscore: {highscore}", True, "white")
    window.blit(hs_render, (GAME_WIDTH // 2 - hs_render.get_width() // 2, 160))

    for i, option in enumerate(menu_options):
        color = "yellow" if i == menu_index else "white"
        text = f"> {option} <" if i == menu_index else option
        option_render = text_font.render(text, True, color)
        window.blit(
            option_render,
            (GAME_WIDTH // 2 - option_render.get_width() // 2, 250 + i * 60),
        )


def draw_game():
    window.blit(background_image, (0, 0))
    window.blit(submarine.img, submarine)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    score_render = title_font.render(str(int(score)), True, "white")
    window.blit(score_render, (GAME_WIDTH // 2 - score_render.get_width() // 2, 20))


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


# ============ TIMER PEMBUAT PIPA ============
create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500)

# ============ GAME LOOP UTAMA ============
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Pipa hanya dibuat saat sedang PLAYING
        if event.type == create_pipes_timer and game_state == "PLAYING":
            create_pipes()

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

            elif game_state == "PLAYING":
                if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                    velocity_y = -6
                    jump_sound.play()

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_SPACE:  # Restart langsung
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_m:  # Kembali ke menu utama
                    game_state = "MAIN_MENU"

    # Render berdasarkan state aktif
    if game_state == "MAIN_MENU":
        draw_menu()
    elif game_state == "PLAYING":
        move()
        draw_game()
    elif game_state == "GAME_OVER":
        draw_game_over()

    pygame.display.update()
    clock.tick(60)
