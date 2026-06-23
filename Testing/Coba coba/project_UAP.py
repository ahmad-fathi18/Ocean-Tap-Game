import pygame
import sys
import random
from termcolor import cprint


# ==========================================
# 6. FILE HANDLING (Membaca High Score)
# ==========================================
def baca_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # Jika file belum ada, set jadi 0


def simpan_high_score(skor):
    with open("highscore.txt", "w") as file:
        file.write(str(skor))
    # 7. TERMCOLOR (Cprint untuk log sistem)
    cprint("[SYSTEM] High Score baru berhasil disimpan!", "blue", attrs=["bold"])


# Inisialisasi Pygame
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird Pemula")

# ==========================================
# 6. DICTIONARY (Data Pemain)
# ==========================================
player_data = {"nama": "Ahmad", "score": 0, "high_score": baca_high_score()}

# Warna (RGB)
WARNA_LANGIT = (113, 197, 207)
WARNA_TIANG = (115, 191, 46)
WARNA_BURUNG = (247, 212, 33)
WARNA_AWAN = (255, 255, 255)

# Game Variables
gravitasi = 0.25
kecepatan_burung = 0
posisi_burung = pygame.Rect(100, 300, 30, 30)
game_aktif = True

# ==========================================
# 3. LIST / ARRAY 1D (Menampung Tiang)
# ==========================================
# Tiang disimpan sebagai kumpulan pygame.Rect
tiang_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # Spawn tiang setiap 1.2 detik
kecepatan_tiang = 3

# ==========================================
# 4. ARRAY 2 DIMENSI (Grid Dekorasi Awan di Langit)
# ==========================================
# 0 = Langit Kosong, 1 = Ada Awan
peta_langit = [[0, 1, 0, 0, 1], [1, 0, 0, 1, 0], [0, 0, 0, 0, 0]]
UKURAN_GRID = 80

# ==========================================
# 7. ANIMATION VARIABLES
# ==========================================
ukuran_burung_tinggi = 30
animasi_counter = 0


# ==========================================
# 5. FUNCTIONS (Fungsi-Fungsi Game)
# ==========================================
def buat_tiang():
    posisi_tiang_random = random.randint(200, 400)
    tiang_bawah = pygame.Rect(SCREEN_WIDTH, posisi_tiang_random, 60, 500)
    tiang_atas = pygame.Rect(
        SCREEN_WIDTH, posisi_tiang_random - 650, 60, 500
    )  # Jarak celah = 150
    return tiang_bawah, tiang_atas


def gerakkan_tiang(daftar_tiang):
    # 2. PERULANGAN (Mengupdate semua tiang di dalam list)
    for tiang in daftar_tiang:
        tiang.centerx -= kecepatan_tiang
    # Hapus tiang yang sudah keluar layar agar memori hemat
    return [tiang for tiang in daftar_tiang if tiang.right > 0]


def gambar_tiang(daftar_tiang):
    for tiang in daftar_tiang:
        pygame.draw.rect(screen, WARNA_TIANG, tiang)


def cek_tabrakan(daftar_tiang):
    for tiang in daftar_tiang:
        # 1. PENGKONDISIAN (Cek nabrak tiang)
        if posisi_burung.colliderect(tiang):
            cprint("[GAME OVER] Burung menabrak tiang!", "red")
            return False

    # 1. PENGKONDISIAN (Cek nabrak batas layar atas / bawah)
    if posisi_burung.top <= 0 or posisi_burung.bottom >= SCREEN_HEIGHT:
        cprint("[GAME OVER] Burung jatuh atau keluar batas!", "red")
        return False

    return True


def gambar_dekorasi_2d():
    # 2. PERULANGAN BERSARANG untuk membaca Array 2D
    for baris_idx, baris in enumerate(peta_langit):
        for kolom_idx, nilai in enumerate(baris):
            if nilai == 1:
                # Menggambar kotak awan sederhana berdasarkan posisi index array 2D
                pygame.draw.circle(
                    screen, WARNA_AWAN, (kolom_idx * 100 + 40, baris_idx * 70 + 40), 25
                )


def tampilkan_skor():
    font = pygame.font.SysFont("Arial", 24)
    skor_text = font.render(f"Skor: {player_data['score']}", True, (255, 255, 255))
    high_text = font.render(
        f"High Score: {player_data['high_score']}", True, (255, 255, 255)
    )
    screen.blit(skor_text, (10, 10))
    screen.blit(high_text, (10, 40))


# ==========================================
# 2. PERULANGAN UTAMA (Game Loop)
# ==========================================
while True:
    # Cek Event / Input User
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_aktif:
                kecepatan_burung = 0
                kecepatan_burung -= 6  # Burung melompat ke atas

            if event.key == pygame.K_SPACE and not game_aktif:
                # Reset Game jika sudah Game Over
                game_aktif = True
                tiang_list.clear()
                posisi_burung.center = (100, 300)
                kecepatan_burung = 0
                player_data["score"] = 0
                cprint("[GAME] Memulai kembali permainan...", "yellow")

        if event.type == SPAWNPIPE and game_aktif:
            # 3. ARRAY/LIST (Menambahkan tiang baru hasil dari function)
            tiang_bawah, tiang_atas = buat_tiang()
            tiang_list.append(tiang_bawah)
            tiang_list.append(tiang_atas)

    # Menggambar Background Langit
    screen.fill(WARNA_LANGIT)

    # 4. Memanggil Array 2D untuk dekorasi awan
    gambar_dekorasi_2d()

    if game_aktif:
        # Pergerakan Burung (Fisika Gravitasi)
        kecepatan_burung += gravitasi
        posisi_burung.centery += kecepatan_burung

        # 7. ANIMATION (Mengecilkan/membesarkan tinggi burung sedikit demi sedikit seperti mengepak)
        animasi_counter += 1
        if animasi_counter % 10 == 0:
            if ukuran_burung_tinggi == 30:
                ukuran_burung_tinggi = 20  # Sayap menekuk (terlihat tipis)
            else:
                ukuran_burung_tinggi = 30  # Sayap mengembang

        # Gambar Burung dengan ukuran tinggi dinamis hasil animasi
        kotak_animasi_burung = pygame.Rect(
            posisi_burung.x, posisi_burung.y, 30, ukuran_burung_tinggi
        )
        pygame.draw.ellipse(screen, WARNA_BURUNG, kotak_animasi_burung)

        # Pergerakan & Penggambaran Tiang
        tiang_list = gerakkan_tiang(tiang_list)
        gambar_tiang(tiang_list)

        # Cek Tabrakan
        game_aktif = cek_tabrakan(tiang_list)

        # Menghitung Skor (Setiap ada tiang yang melewati koordinat burung x=100)
        for tiang in tiang_list:
            if tiang.centerx == 100:
                player_data["score"] += (
                    0.5  # Karena 1 pasang ada 2 tiang (atas & bawah), 0.5 + 0.5 = 1
                )
                if player_data["score"].is_integer():
                    # 7. TERMCOLOR (Cprint warna hijau saat dapat skor)
                    cprint(
                        f"[SCORE] +1! Skor Sekarang: {int(player_data['score'])}",
                        "green",
                    )

    else:
        # 1. PENGKONDISIAN & 6. FILE HANDLING (Jika Game Over, cek High Score)
        if player_data["score"] > player_data["high_score"]:
            player_data["high_score"] = int(player_data["score"])
            simpan_high_score(player_data["high_score"])

        # Tampilan Game Over di Layar Terminal / Screen
        font_over = pygame.font.SysFont("Arial", 30)
        text_over = font_over.render("GAME OVER - Tekan Space", True, (255, 0, 0))
        screen.blit(text_over, (50, 250))

    # Tampilkan Skor di Layar GUI
    tampilkan_skor()

    # Update Layar dan Mengatur FPS ke 60
    pygame.display.update()
    clock.tick(60)
