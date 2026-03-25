import pygame

pygame.init()

#window suurus
laius = 800
korgus = 600
ekraan = pygame.display.set_mode((laius, korgus))
pygame.display.set_caption("Liikuv ruut")

#varvid
valge = (255, 255, 255)
sinine = (0, 100, 255)

#ruudu algpositsion (keskel)
ruudu_suurus = 50
x = laius // 2 - ruudu_suurus // 2
y = korgus // 2 - ruudu_suurus // 2

#liikumise kiirus
kiirus = 5

#peatsykl
too_kaib = True
while too_kaib:
    for sundmus in pygame.event.get():
        if sundmus.type == pygame.QUIT:
            too_kaib = False

    #klahvide kontroll
    klahvid = pygame.key.get_pressed()

    if klahvid[pygame.K_LEFT]:
        x -= kiirus
    if klahvid[pygame.K_RIGHT]:
        x += kiirus
    if klahvid[pygame.K_UP]:
        y -= kiirus
    if klahvid[pygame.K_DOWN]:
        y += kiirus

    #piirid (ruut ei lahe ekraanist valja)
    if x < 0:
        x = 0
    if x > laius - ruudu_suurus:
        x = laius - ruudu_suurus
    if y < 0:
        y = 0
    if y > korgus - ruudu_suurus:
        y = korgus - ruudu_suurus

    #joonistamine
    ekraan.fill(valge)
    pygame.draw.rect(ekraan, sinine, (x, y, ruudu_suurus, ruudu_suurus))
    pygame.display.flip()

pygame.quit()
