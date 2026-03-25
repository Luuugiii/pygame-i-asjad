import pygame
pygame.init()

#varvide funktsioon
def color(nimi):
    nimi = nimi.lower()
    kaart = {
        "punane": (255, 0, 0),
        "kollane": (255, 255, 0),
        "roheline": (0, 255, 0),
        "sinine": (0, 0, 255),
        "valge": (255, 255, 255),
        "must": (0, 0, 0),
        "hall": (80, 80, 80)
    }
    return kaart.get(nimi, None)

#kasutaja sisend
width = int(input("sisesta akna laius (nt 300): "))
height = int(input("sisesta akna korgus (nt 300): "))
radius = int(input("sisesta ringi suurus (nt 25): "))

#tulede colors
first_light = color(input("1 tule varv: "))
second_light = color(input("2 tule varv: "))
third_light = color(input("3 tule varv: "))

#background
taust_input = input("tausta varv voi tyhi: ")
if taust_input.strip() == "":
    background = (0, 0, 0)
else:
    background = color(taust_input)
    if background is None:
        background = (0, 0, 0)

#window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("foor - sinu nimi")

grey = (80, 80, 80)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background)

    #foori korpus
    pygame.draw.rect(screen, grey, (width//2 - radius, 20, radius*2, radius*6))

    #tuled
    pygame.draw.circle(screen, first_light, (width//2, 20 + radius), radius)
    pygame.draw.circle(screen, second_light, (width//2, 20 + radius*3), radius)
    pygame.draw.circle(screen, third_light, (width//2, 20 + radius*5), radius)

    pygame.display.flip()

pygame.quit()