import pygame
import sys

pygame.init()

#ekraani setting
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("yl 2")
#pildid and skaleerimine
bg = pygame.image.load("bg_shop.jpg")
bg = pygame.transform.smoothscale(bg, (640, 480))#taust

seller = pygame.image.load("seller.png")
seller = pygame.transform.smoothscale(seller, (260, 310))#müüja

chat = pygame.image.load("chat.png")
chat = pygame.transform.smoothscale(chat, (252, 200))#jutumull

#teksti seadistamine
font = pygame.font.SysFont("arial", 28)
text = font.render("Tere, mina olen Mikk-Gregor", True, (255, 255, 255))

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

    #chat bubble
    screen.blit(chat, (250, 65))

    #tekst chat bubble sees
    screen.blit(text, (290, 145))

    pygame.display.flip()