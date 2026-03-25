import pygame

pygame.init()

#kysib kasutajal tausta varvi ja kas lisada myts
myts = input("kas lumememmel on myts (jah/ei)? ")
taust = input("tausta varv (black/blue/white)? ")

varvid = {
    "black": (0, 0, 0),
    "blue": (0, 100, 255),
    "white": (255, 255, 255)
}

bg = varvid.get(taust, (0, 0, 0))

screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("snowman - mikk-gregor rannel")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bg)

    #kui taust on valge, lisa outline
    if bg == (255, 255, 255):
        pygame.draw.circle(screen, (255, 255, 255), (150, 220), 50)
        pygame.draw.circle(screen, (0, 0, 0), (150, 220), 50, 2)

        pygame.draw.circle(screen, (255, 255, 255), (150, 150), 40)
        pygame.draw.circle(screen, (0, 0, 0), (150, 150), 40, 2)

        pygame.draw.circle(screen, (255, 255, 255), (150, 90), 30)
        pygame.draw.circle(screen, (0, 0, 0), (150, 90), 30, 2)
    else:
        pygame.draw.circle(screen, (255, 255, 255), (150, 220), 50)
        pygame.draw.circle(screen, (255, 255, 255), (150, 150), 40)
        pygame.draw.circle(screen, (255, 255, 255), (150, 90), 30)

    #silmad
    pygame.draw.circle(screen, (0, 0, 0), (140, 80), 5)
    pygame.draw.circle(screen, (0, 0, 0), (160, 80), 5)

    #nina
    pygame.draw.polygon(screen, (255, 120, 0), [(150, 90), (145, 105), (155, 105)])

    #nupud
    pygame.draw.circle(screen, (0, 0, 0), (150, 140), 5)
    pygame.draw.circle(screen, (0, 0, 0), (150, 165), 5)

    #myts
    if myts == "jah":
        pygame.draw.rect(screen, (0, 0, 0), (120, 50, 60, 10))
        pygame.draw.rect(screen, (0, 0, 0), (130, 20, 40, 30))

    pygame.display.flip()

pygame.quit()