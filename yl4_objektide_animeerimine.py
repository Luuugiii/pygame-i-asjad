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

#game loop
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

            game_over_font = pygame.font.SysFont("Arial", 60, bold=True)
            small_font = pygame.font.SysFont("Arial", 30)

            restart = False

            while True:

                ekraan.fill((0, 0, 0))

                game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
                score_text = small_font.render("skoor: " + str(skoor), True, (255, 255, 255))
                restart_text = small_font.render("vajuta R restartimiseks", True, (255, 255, 255))
                exit_text = small_font.render("vajuta ESC valjumiseks", True, (255, 255, 255))

                ekraan.blit(game_over_text, (laius // 2 - game_over_text.get_width() // 2, 130))
                ekraan.blit(score_text, (laius // 2 - score_text.get_width() // 2, 220))
                ekraan.blit(restart_text, (laius // 2 - restart_text.get_width() // 2, 270))
                ekraan.blit(exit_text, (laius // 2 - exit_text.get_width() // 2, 320))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_r:
                            restart = True

                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

                if restart:
                    break

            punane_rect.center = (laius // 2, korgus - 50)

            sinised.clear()
            for i in range(3):
                x = random.randint(150, laius - 150)
                y = random.randint(-400, -50)
                sinised.append(
                    pygame.Rect(
                        x,
                        y,
                        sinine_auto.get_width(),
                        sinine_auto.get_height()
                    )
                )

            skoor = 0
            break

        ekraan.blit(sinine_auto, rect)

    #punane auto
    ekraan.blit(punane_auto, punane_rect)

    #scoreboard
    tekst = font.render("skoor: " + str(skoor), True, (255, 255, 255))
    ekraan.blit(tekst, (10, 10))

    pygame.display.flip()
    kell.tick(60)