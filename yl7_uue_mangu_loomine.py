import pygame
import random
import math

pygame.init()

#ekraani size
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("circle game mikk-gregor")

clock = pygame.time.Clock()

#ringide list
rings = []

#algne raadius
BASE_RADIUS = 10

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #mouseclick
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # Loo uus ring
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            new_ring = {"x": x, "y": y, "r": BASE_RADIUS, "color": color}
            rings.append(new_ring)

            #max 10 ringi, kui seda yletada, ss kustutatakse
            if len(rings) > 10:
                rings.pop(0)

            #parast ringi kliki laheb ringid suuremaks
            for ring in rings:
                ring["r"] += 3

            #midagi, mis ise lisasin
            #Kui klikk on ekraani keskusele lahedal, ss kasvavad koik ringid veel
            #saad uue colori
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            dist_to_center = math.hypot(x - center_x, y - center_y)
            if dist_to_center < 40:
                for ring in rings:
                    ring["r"] += 5
                    ring["color"] = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )

    #drawing
    screen.fill((0, 0, 0))

    for ring in rings:
        pygame.draw.circle(
            screen,
            ring["color"],
            (ring["x"], ring["y"]),
            ring["r"],
            1  #ringig on 10 pikslit
        )

    pygame.display.flip()

pygame.quit()