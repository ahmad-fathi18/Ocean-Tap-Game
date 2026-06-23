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

# ============ KONFIGURASI FONT BARU ============
# Judul utama tetap bergaya besar (bisa pakai Arial Black / Impact agar gagah)
title_font = pygame.font.SysFont("Impact", 45)

# Opsi Menu & Highscore menggunakan font yang modern, tebal, dan sangat rapi
text_font = pygame.font.SysFont("Arial", 24, bold=True)

# Nama Kreator & Teks Game Over menggunakan font modern yang halus tapi tegas
game_over_font = pygame.font.SysFont("Impact", 40)
game_over_text = pygame.font.SysFont("Arial", 18, bold=True)

# ============ STATE & VARIABEL GAME ============
game_state = "MAIN_MENU"

submarine = Submarine(sub_image)
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
score = 0

menu_options = ["Mulai", "Keluar"]
menu_index = 0

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

    if submarine.y > GAME_HEIGHT:
        game_state = "GAME_OVER"
        check_highscore()
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and submarine.x > pipe.x + pipe_width:
            score += 0.5
            pipe.passed = True

        if submarine.colliderect(pipe):
            game_state = "GAME_OVER"
            check_highscore()
            return

    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)


# ============ UI/UX HELPER FUNCTIONS ============
def draw_shadow_text(text, font, color, x, y, shadow_color=(20, 20, 20), offset=2):
    """Menggambar teks dengan bayangan hitam di belakangnya agar kontras di background apapun"""
    shadow = font.render(text, True, shadow_color)
    window.blit(shadow, (x + offset, y + offset))
    render = font.render(text, True, color)
    window.blit(render, (x, y))


def draw_panel(x, y, w, h, alpha=160):
    """Menggambar panel latar belakang transparan gelap dengan border biru laut estetis"""
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((12, 28, 42, alpha))  # Warna biru dongker transparan
    pygame.draw.rect(
        panel, (70, 160, 240, 200), panel.get_rect(), 2, border_radius=8
    )  # Border luar
    window.blit(panel, (x, y))


# ============ FUNGSI RENDER/DRAW ============
def draw_menu():
    window.blit(background_image, (0, 0))

    # ================= 1. JUDUL UTAMA =================
    title = "OCEAN TAP"
    tw = title_font.size(title)[0]
    draw_shadow_text(title, title_font, (255, 140, 0), GAME_WIDTH // 2 - tw // 2, 90)

    # ================= 2. HIGHSCORE =================
    hs_text = f"Highscore: {highscore}"
    hw = text_font.size(hs_text)[0]
    draw_shadow_text(
        hs_text, text_font, (255, 255, 255), GAME_WIDTH // 2 - hw // 2, 160
    )

    # ================= 3. TOMBOL NAVIGASI (MODERN & CENTER) =================
    for i, option in enumerate(menu_options):
        selected = i == menu_index
        text = option
        color = (255, 255, 0) if selected else (200, 230, 255)

        btn_w, btn_h = 160, 42
        bx = GAME_WIDTH // 2 - btn_w // 2
        by = 330 + i * 65  # Sedikit dinaikkan agar tidak terlalu mepet panel nama bawah

        if selected:
            draw_panel(bx, by, btn_w, btn_h, alpha=140)
        else:
            draw_panel(bx, by, btn_w, btn_h, alpha=40)

        ow = text_font.size(text)[0]
        oh = text_font.size(text)[1]
        text_x = GAME_WIDTH // 2 - ow // 2
        text_y = by + (btn_h // 2 - oh // 2)

        draw_shadow_text(text, text_font, color, text_x, text_y)

    # ================= 4. FOOTER: NAMA KREATOR (SOLUSI KONTRAS) =================
    # Kita buatkan panel transparan memanjang di bagian paling bawah layar
    # Ini berfungsi sebagai "tameng" agar gambar latar belakang melunak dan teks kontras
    panel_footer_w = GAME_WIDTH - 40
    panel_footer_h = 95
    pfx = 20
    pfy = 525
    draw_panel(
        pfx, pfy, panel_footer_w, panel_footer_h, alpha=150
    )  # Alpha 150 agar teks dijamin kontras

    # Teks "DEVELOPED BY"
    creator_title = "DEVELOPED BY:"
    ct_w = game_over_text.size(creator_title)[0]
    # Menggunakan warna kuning emas lembut agar kontras dan estetik di dalam panel
    draw_shadow_text(
        creator_title,
        game_over_text,
        (255, 215, 0),
        GAME_WIDTH // 2 - ct_w // 2,
        pfy + 10,
    )

    # Nama-nama Kreator
    names = ["Ahmad Fathi", "M. Al Rafi Dzaki Akbar"]
    for idx, name in enumerate(names):
        n_w = game_over_text.size(name)[0]
        # Warna teks putih bersih, dengan bayangan hitam pekat bawaan draw_shadow_text
        draw_shadow_text(
            name,
            game_over_text,
            (255, 255, 255),
            GAME_WIDTH // 2 - n_w // 2,
            pfy + 38 + idx * 24,
        )


def draw_game():
    window.blit(background_image, (0, 0))
    window.blit(submarine.img, submarine)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    # ================= IMPROVISASI HUD SKOR (ARCADE BADGE) =================
    # Membuat panel mini transparan di pojok kiri atas agar tidak tertabrak pipa
    score_panel_w = 95
    score_panel_h = 40
    spx = 15
    spy = 15
    draw_panel(spx, spy, score_panel_w, score_panel_h, alpha=130)

    # Menggabungkan teks ikon bintang emas dengan angka skor
    score_text = f"★ {int(score)}"

    # Hitung posisi teks agar pas berada di tengah-tengah panel mini
    tw = text_font.size(score_text)[0]
    th = text_font.size(score_text)[1]
    text_x = spx + (score_panel_w // 2 - tw // 2)
    text_y = spy + (score_panel_h // 2 - th // 2)

    # Gambar skor dengan warna kuning menyala dan bayangan tebal agar sangat jelas terlihat
    draw_shadow_text(score_text, text_font, (255, 215, 0), text_x, text_y)


# ============ TIMER PEMBUAT PIPA ============
create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500)

# ============ GAME LOOP UTAMA ============
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_pipes_timer and game_state == "PLAYING":
            create_pipes()

        if event.type == pygame.KEYDOWN:
            if game_state == "MAIN_MENU":
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(menu_options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if menu_index == 0:
                        reset_game()
                        game_state = "PLAYING"
                    elif menu_index == 1:
                        pygame.quit()
                        exit()

            elif game_state == "PLAYING":
                if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                    velocity_y = -6
                    jump_sound.play()

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_m:
                    game_state = "MAIN_MENU"

    if game_state == "MAIN_MENU":
        draw_menu()
    elif game_state == "PLAYING":
        move()
        draw_game()
    elif game_state == "GAME_OVER":
        draw_game_over()

    pygame.display.update()
    clock.tick(60)
