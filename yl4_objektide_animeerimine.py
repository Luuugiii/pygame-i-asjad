import pygame
import random
import sys

pygame.init()

#ekraani settings
laius, korgus = 640, 480
ekraan = pygame.display.set_mode((laius, korgus))
pygame.display.set_caption("car game - mikk-gregor")

#pictures
taust = pygame.image.load("X:\PyCharmMiscProject\yl4/bg_rally.jpg").convert()
punane_auto = pygame.image.load("X:\PyCharmMiscProject\yl4/f1_red.png").convert_alpha()
sinine_auto = pygame.image.load("X:\PyCharmMiscProject\yl4/f1_blue.png").convert_alpha()

# Auto positsioonid
punane_rect = punane_auto.get_rect(center=(laius // 2, korgus - 50))

#sinised autod ja mitu tykki
sinised = []
for i in range(3):
    x = random.randint(150, laius - 150)
    y = random.randint(-400, -50)
    sinised.append(pygame.Rect(x, y, sinine_auto.get_width(), sinine_auto.get_height()))

kiirus = 5
skoor = 0
font = pygame.font.SysFont("Arial", 24)

kell = pygame.time.Clock()

#game tsykkel
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #background
    ekraan.blit(taust, (0, 0))

    #siniste autode liikumine ylevalt alla
    for rect in sinised:
        rect.y += kiirus
        if rect.y > korgus:
            rect.y = random.randint(-200, -100)
            rect.x = random.randint(150, laius - 150)
            skoor += 1

        ekraan.blit(sinine_auto, rect)

    #red auto (mis on staatiline)
    ekraan.blit(punane_auto, punane_rect)

    #scoreboard
    tekst = font.render("Skoor: " + str(skoor), True, (255, 255, 255))
    ekraan.blit(tekst, (10, 10))

    pygame.display.flip()
    kell.tick(60)
