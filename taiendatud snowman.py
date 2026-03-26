import pygame

pygame.init()

#kysib kasutajal tausta varvi ja kas lisada myts
myts = input("kas lumememmel on myts (jah/ei)? ")
taust = input("tausta varv (black/blue/white/lightblue)? ")

varvid = {
    "black": (0, 0, 0),
    "blue": (0, 100, 255),
    "white": (255, 255, 255),
    "lightblue": (173, 216, 230)
}

bg = varvid.get(taust, (173, 216, 230))

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("snowman - mikk-gregor rannel")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bg)

    #sun
    pygame.draw.circle(screen, (255, 255, 0), (350, 50), 30)
    for i in range(8):
        pygame.draw.line(screen, (255, 255, 0), (350, 50),
                         (350 + 50 * pygame.math.Vector2(1, 0).rotate(i * 45).x,
                          50 + 50 * pygame.math.Vector2(1, 0).rotate(i * 45).y), 2)

    #pilved (3tk)
    pygame.draw.circle(screen, (255, 255, 255), (80, 60), 20)
    pygame.draw.circle(screen, (255, 255, 255), (100, 60), 25)
    pygame.draw.circle(screen, (255, 255, 255), (120, 60), 20)

    pygame.draw.circle(screen, (255, 255, 255), (200, 80), 20)
    pygame.draw.circle(screen, (255, 255, 255), (220, 80), 25)
    pygame.draw.circle(screen, (255, 255, 255), (240, 80), 20)

    pygame.draw.circle(screen, (255, 255, 255), (300, 100), 20)
    pygame.draw.circle(screen, (255, 255, 255), (320, 100), 25)
    pygame.draw.circle(screen, (255, 255, 255), (340, 100), 20)

    #lumememm
    if bg == (255, 255, 255):
        pygame.draw.circle(screen, (255, 255, 255), (200, 300), 50)
        pygame.draw.circle(screen, (0, 0, 0), (200, 300), 50, 2)

        pygame.draw.circle(screen, (255, 255, 255), (200, 230), 40)
        pygame.draw.circle(screen, (0, 0, 0), (200, 230), 40, 2)

        pygame.draw.circle(screen, (255, 255, 255), (200, 170), 30)
        pygame.draw.circle(screen, (0, 0, 0), (200, 170), 30, 2)
    else:
        pygame.draw.circle(screen, (255, 255, 255), (200, 300), 50)
        pygame.draw.circle(screen, (255, 255, 255), (200, 230), 40)
        pygame.draw.circle(screen, (255, 255, 255), (200, 170), 30)

    #eyes
    pygame.draw.circle(screen, (0, 0, 0), (190, 160), 5)
    pygame.draw.circle(screen, (0, 0, 0), (210, 160), 5)

    #nose
    pygame.draw.polygon(screen, (255, 120, 0), [(200, 170), (195, 185), (205, 185)])

    #noobid (3tk)
    pygame.draw.circle(screen, (0, 0, 0), (200, 210), 5)
    pygame.draw.circle(screen, (0, 0, 0), (200, 240), 5)
    pygame.draw.circle(screen, (0, 0, 0), (200, 270), 5)

    #kaed
    pygame.draw.line(screen, (139, 69, 19), (160, 230), (120, 200), 3)
    pygame.draw.line(screen, (139, 69, 19), (240, 230), (280, 200), 3)

    #hari (paremas käes)
    pygame.draw.line(screen, (139, 69, 19), (280, 200), (310, 150), 4)
    pygame.draw.rect(screen, (200, 0, 0), (305, 140, 10, 20))

    #myts
    if myts == "jah":
        pygame.draw.rect(screen, (0, 0, 0), (170, 140, 60, 10))
        pygame.draw.rect(screen, (0, 0, 0), (180, 110, 40, 30))

    pygame.display.flip()

pygame.quit()