import pygame
import random
import sys
import math

pygame.init()

# =========================
# INSTÄLLNINGAR
# =========================
WIDTH = 1280
HEIGHT = 720
FPS = 60
WORLD_WIDTH = 3200
WORLD_HEIGHT = 2200

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Häxbrygden")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

# =========================
# FÄRGER
# =========================
GRASS = (70, 140, 70)
HEATH = (140, 120, 70)
MOUNTAIN = (120, 120, 120)
DARK_FOREST = (20, 80, 20)
WATER = (40, 120, 255)
BROWN = (120, 70, 30)
LIGHT_BROWN = (170, 120, 70)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
BLUE = (50, 120, 255)
PURPLE = (160, 70, 200)
YELLOW = (255, 220, 0)
GRAY = (180, 180, 180)
GREEN = (50, 200, 70)

# =========================
# SPELARE
# =========================
player = pygame.Rect(200, 1700, 40, 50)
player_speed = 5
player_health = 100

# =========================
# OMRÅDEN
# =========================
farm = pygame.Rect(100, 1600, 250, 250)
forest = pygame.Rect(1700, 500, 900, 1000)
mountains = pygame.Rect(2500, 100, 600, 700)
heath = pygame.Rect(800, 1200, 700, 500)

river = pygame.Rect(1200, 0, 180, 1700)
lake = pygame.Rect(900, 1600, 700, 500)
bridge = pygame.Rect(1200, 900, 180, 140)

witch_house = pygame.Rect(2100, 700, 150, 150)

child = pygame.Rect(180, 1680, 35, 35)
witch = pygame.Rect(2140, 740, 40, 40)

# =========================
# ÖRTER
# =========================
herbs = []

while len(herbs) < 5:
    herb = pygame.Rect(
        random.randint(900, 2500),
        random.randint(300, 1800),
        20,
        20
    )
    if not herb.colliderect(river) and not herb.colliderect(lake):
        herbs.append(herb)

collected_herbs = 0
required_herbs = 5

# =========================
# FIENDER
# =========================
enemies = []

for i in range(10):
    enemy = {
        "rect": pygame.Rect(
            random.randint(1700, 2600),
            random.randint(400, 1400),
            40,
            40
        ),
        "dir_x": random.choice([-2, 2]),
        "dir_y": random.choice([-2, 2])
    }
    enemies.append(enemy)

# =========================
# SPELSTATUS
# =========================
has_medicine = False
won = False
lost = False
message = "Ditt barn är svårt sjukt..."
time_left = 4500

camera_x = 0
camera_y = 0
animation_timer = 0

# =========================
# TEXT
# =========================
def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# =========================
# HUVUDLOOP
# =========================
while True:

    dt = clock.tick(FPS)
    animation_timer += 0.08

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not won and not lost:

        keys = pygame.key.get_pressed()

        old_x = player.x
        old_y = player.y

        moving = False

        if keys[pygame.K_LEFT]:
            player.x -= player_speed
            moving = True

        if keys[pygame.K_RIGHT]:
            player.x += player_speed
            moving = True

        if keys[pygame.K_UP]:
            player.y -= player_speed
            moving = True

        if keys[pygame.K_DOWN]:
            player.y += player_speed
            moving = True

        # Begränsa världen
        player.x = max(0, min(WORLD_WIDTH - player.width, player.x))
        player.y = max(0, min(WORLD_HEIGHT - player.height, player.y))

        # Flod och sjö
        if (player.colliderect(river) or player.colliderect(lake)) and not player.colliderect(bridge):
            player.x = old_x
            player.y = old_y

        # Fiender
        for enemy in enemies:

            rect = enemy["rect"]

            rect.x += enemy["dir_x"]
            rect.y += enemy["dir_y"]

            if rect.left < forest.left or rect.right > forest.right:
                enemy["dir_x"] *= -1

            if rect.top < forest.top or rect.bottom > forest.bottom:
                enemy["dir_y"] *= -1

            if player.colliderect(rect):
                player_health -= 1
                message = "Rövare attackerar dig!"

        # Samla örter
        for herb in herbs[:]:
            if player.colliderect(herb):
                herbs.remove(herb)
                collected_herbs += 1
                message = f"Du hittade örter ({collected_herbs}/{required_herbs})"

        # Häxan
        if player.colliderect(witch):

            if collected_herbs < required_herbs:
                message = "Häxan: 'Samla fler örter åt mig!'"

            elif not has_medicine:
                has_medicine = True
                message = "Häxan brygger medicinen åt dig!"

        # Vinst
        if has_medicine and player.colliderect(child):
            won = True
            message = "Ditt barn överlevde!"

        # Förlust
        if player_health <= 0:
            lost = True
            message = "Du dog på resan."

        time_left -= 1

        if time_left <= 0:
            lost = True
            message = "Du hann inte tillbaka innan barnet dog."

    # =========================
    # KAMERA
    # =========================
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

    camera_x = max(0, min(WORLD_WIDTH - WIDTH, camera_x))
    camera_y = max(0, min(WORLD_HEIGHT - HEIGHT, camera_y))

    # =========================
    # BAKGRUND
    # =========================
    screen.fill(GRASS)

    # Hedar
    pygame.draw.rect(screen, HEATH,
                     (heath.x - camera_x,
                      heath.y - camera_y,
                      heath.width,
                      heath.height))

    # Berg
    pygame.draw.rect(screen, MOUNTAIN,
                     (mountains.x - camera_x,
                      mountains.y - camera_y,
                      mountains.width,
                      mountains.height))

    # Skog
    pygame.draw.rect(screen, DARK_FOREST,
                     (forest.x - camera_x,
                      forest.y - camera_y,
                      forest.width,
                      forest.height))

    # Sjö
    pygame.draw.ellipse(screen, WATER,
                        (lake.x - camera_x,
                         lake.y - camera_y,
                         lake.width,
                         lake.height))

    # Flod
    wave = math.sin(animation_timer) * 5

    pygame.draw.rect(screen,
                     (40, 120 + int(wave), 255),
                     (river.x - camera_x,
                      river.y - camera_y,
                      river.width,
                      river.height))

    # Bro
    pygame.draw.rect(screen, LIGHT_BROWN,
                     (bridge.x - camera_x,
                      bridge.y - camera_y,
                      bridge.width,
                      bridge.height))

    # Gård
    pygame.draw.rect(screen, BROWN,
                     (farm.x - camera_x,
                      farm.y - camera_y,
                      farm.width,
                      farm.height))

    # Häxans stuga
    pygame.draw.rect(screen, GRAY,
                     (witch_house.x - camera_x,
                      witch_house.y - camera_y,
                      witch_house.width,
                      witch_house.height))

    # Barn
    if not won:
        pygame.draw.circle(screen, RED,
                           (child.x - camera_x + 15,
                            child.y - camera_y + 15), 15)

    # Häxa
    pygame.draw.circle(screen, PURPLE,
                       (witch.x - camera_x + 20,
                        witch.y - camera_y + 20), 20)

    # Örter
    for herb in herbs:
        pygame.draw.circle(screen, GREEN,
                           (herb.x - camera_x + 10,
                            herb.y - camera_y + 10), 10)

    # Fiender
    for enemy in enemies:
        rect = enemy["rect"]

        pygame.draw.rect(screen, BLACK,
                         (rect.x - camera_x,
                          rect.y - camera_y,
                          rect.width,
                          rect.height))

    # Spelare
    bounce = math.sin(animation_timer * 10) * 3 if moving else 0

    pygame.draw.rect(screen, BLUE,
                     (player.x - camera_x,
                      player.y - camera_y + bounce,
                      player.width,
                      player.height))

    # =========================
    # UI
    # =========================
    pygame.draw.rect(screen, BLACK, (10, 10, 340, 180))

    draw_text(f"Liv: {player_health}", 20, 20)
    draw_text(f"Tid kvar: {time_left}", 20, 55)
    draw_text(f"Örter: {collected_herbs}/{required_herbs}", 20, 90)

    if has_medicine:
        draw_text("Medicin: JA", 20, 125, YELLOW)
    else:
        draw_text("Medicin: NEJ", 20, 125)

    draw_text(message, 20, 160)

    # Slutskärm
    if won:
        draw_text("DU RÄDDADE DITT BARN!", WIDTH // 2 - 220, HEIGHT // 2, YELLOW)

    if lost:
        draw_text("GAME OVER", WIDTH // 2 - 120, HEIGHT // 2, RED)

    pygame.display.flip()
