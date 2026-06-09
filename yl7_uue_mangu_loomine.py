import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("circle game mikk-gregor")

clock = pygame.time.Clock()

rings = []

spawn_radius = 10
MAX_RADIUS = 80

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

            rings.append({
                "x": x,
                "y": y,
                "r": spawn_radius,
                "color": color
            })

            #kasv + reset
            spawn_radius += 2

            if spawn_radius > MAX_RADIUS:
                spawn_radius = 10  # reset

            #max 10 ringi
            if len(rings) > 10:
                rings.pop(0)

            #center bonus
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            dist_to_center = math.hypot(x - center_x, y - center_y)

            if dist_to_center < 40:
                spawn_radius += 3

                if spawn_radius > MAX_RADIUS:
                    spawn_radius = 10  #reset ka siin

    #draw
    screen.fill((0, 0, 0))
ss
    for ring in rings:
        pygame.draw.circle(
            screen,
            ring["color"],
            (ring["x"], ring["y"]),
            ring["r"],
            1
        )

    pygame.display.flip()

pygame.quit()
