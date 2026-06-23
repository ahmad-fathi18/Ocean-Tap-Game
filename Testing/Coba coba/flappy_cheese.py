import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Layar
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Warna
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 215, 0)
GREEN = (34, 139, 34)

# Variabel Game
bird_x = 50
bird_y = 300
bird_radius = 15
gravity = 0.5
bird_movement = 0

pipe_width = 70
pipe_gap = 150
pipe_speed = 3
pipes = []


def create_pipe():
    random_pipe_y = random.randint(150, 450)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, random_pipe_y, pipe_width, SCREEN_HEIGHT)
    top_pipe = pygame.Rect(
        SCREEN_WIDTH, random_pipe_y - pipe_gap - 500, pipe_width, 500
    )
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > -50]


def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)


# Main Loop
running = True
game_active = True
score = 0
font = pygame.font.Font(None, 40)

# Event untuk membuat pipa baru
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes.clear()
                bird_y = 300
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE and game_active:
            pipes.extend(create_pipe())

    screen.fill(SKY_BLUE)

    if game_active:
        # Burung
        bird_movement += gravity
        bird_y += bird_movement
        bird_rect = pygame.draw.circle(
            screen, YELLOW, (bird_x, int(bird_y)), bird_radius
        )

        # Pipa
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Cek Tabrakan
        if bird_y <= 0 or bird_y >= SCREEN_HEIGHT:
            game_active = False
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                game_active = False

        # Skor
        score += 0.01  # Sederhana: skor bertambah berjalannya waktu
        score_surface = font.render(str(int(score)), True, WHITE)
        screen.blit(score_surface, (SCREEN_WIDTH // 2, 50))
    else:
        # Game Over
        text = font.render("NUB anjir", True, WHITE)
        screen.blit(text, (30, SCREEN_HEIGHT // 2))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
