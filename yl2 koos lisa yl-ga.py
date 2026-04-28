import pygame
import sys
import math

pygame.init()

#ekraani setting
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Ülesanne 2")

#pildid and skaleerimine
def lae_pilt(fail, suurus):
    pilt = pygame.image.load(fail)
    return pygame.transform.smoothscale(pilt, suurus)

bg = lae_pilt("bg_shop.jpg", (640, 480))#background
seller = lae_pilt("seller.png", (260, 310))#shopkeeper
chat = lae_pilt("chat.png", (252, 200))#chatbubble

#teksti seadistus
font = pygame.font.SysFont("times_new_roman", 28)
text = font.render("tere, olen mikk-gregor", True, (255, 255, 255))

#2.1
logo = lae_pilt("VIKK100.png", (280, 70))#logo
mook = lae_pilt("mook.png", (120, 160))#sword
tort = lae_pilt("cake.png", (120, 120))#cake

#kaare text
font3 = pygame.font.SysFont("times_new_roman", 22, bold=True)
tekst_kaar = "0502 KIVELUT"

#kaare seadistus
center_x, center_y = 240, 10
radius = 100
algus_nurk = 0.1

#mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #background
    screen.blit(bg, (0, 0))

    #shopkeeper
    screen.blit(seller, (105, 155))

    #chatbubble
    screen.blit(chat, (250, 65))

    #tekst chatbubblei sisse
    screen.blit(text, (280, 145))

    #logo
    screen.blit(logo, (25, 10))

    #kaare text joonistamine
    for i, tahl in enumerate(tekst_kaar):
        nurk = algus_nurk + i * 0.13
        x = center_x + radius * math.cos(nurk)
        y = center_y + radius * math.sin(nurk)

        tahl_surf = font3.render(tahl, True, (0, 150, 200))
        tahl_surf = pygame.transform.rotate(tahl_surf, -math.degrees(nurk) + 90)

        rect = tahl_surf.get_rect(center=(x, y))
        screen.blit(tahl_surf, rect)

    #sword
    screen.blit(mook, (510, 140))

    #cake
    screen.blit(tort, (400, 200))

    pygame.display.flip()