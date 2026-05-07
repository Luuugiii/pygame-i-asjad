import pygame
import random
import sys

pygame.init()

#ekraani settings
laius, korgus = 640, 480
ekraan = pygame.display.set_mode((laius, korgus))
pygame.display.set_caption("car game - mikk-gregor")

#pictures
taust = pygame.image.load("X:/PyCharmMiscProject/yl4/bg_rally.jpg").convert()
punane_auto = pygame.image.load("X:/PyCharmMiscProject/yl4/f1_red.png").convert_alpha()
sinine_auto = pygame.image.load("X:/PyCharmMiscProject/yl4/f1_blue.png").convert_alpha()

#punase auto positsioon
punane_rect = punane_auto.get_rect(center=(laius // 2, korgus - 50))

#sinised autod
sinised = []
for i in range(3):
    x = random.randint(150, laius - 150)
    y = random.randint(-400, -50)
    sinised.append(pygame.Rect(x, y,
                                sinine_auto.get_width(),
                                sinine_auto.get_height()))

kiirus = 5
auto_kiirus = 7
skoor = 0
font = pygame.font.SysFont("Arial", 24)

kell = pygame.time.Clock()

# ame loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #klahvide kontroll
    nupud = pygame.key.get_pressed()

    if nupud[pygame.K_LEFT]:
        punane_rect.x -= auto_kiirus

    if nupud[pygame.K_RIGHT]:
        punane_rect.x += auto_kiirus

    #et auto ei laheks screenist valja
    if punane_rect.left < 120:
        punane_rect.left = 120

    if punane_rect.right > laius - 120:
        punane_rect.right = laius - 120

    #background
    ekraan.blit(taust, (0, 0))

    #siniste autode liikumine
    for rect in sinised:
        rect.y += kiirus

        #kui auto jouab alla
        if rect.y > korgus:
            rect.y = random.randint(-200, -100)
            rect.x = random.randint(150, laius - 150)
            skoor += 1

        #crash
        if punane_rect.colliderect(rect):
            print("game over, man.. game over!")
            pygame.quit()
            sys.exit()

        ekraan.blit(sinine_auto, rect)

    #punane auto
    ekraan.blit(punane_auto, punane_rect)

    #scoreboard
    tekst = font.render("skoor: " + str(skoor), True, (255, 255, 255))
    ekraan.blit(tekst, (10, 10))

    pygame.display.flip()
    kell.tick(60)
