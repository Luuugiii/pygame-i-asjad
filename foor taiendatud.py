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

    #post
    post_width = 10
    post_height = height // 3
    post_x = width//2 - post_width//2
    post_y = 20 + radius*6
    pygame.draw.rect(screen, grey, (post_x, post_y, post_width, post_height))

    #postialus
    base_top_y = post_y + post_height
    base_height = 60
    base_half_width = 40

    left_point = (width//2 - base_half_width, base_top_y + base_height)
    right_point = (width//2 + base_half_width, base_top_y + base_height)
    top_point = (width//2, base_top_y)

    #jaotab kolmeks triibuks (eesti lipp)
    for i, color_flag in enumerate([(0, 0, 255), (0, 0, 0), (255, 255, 255)]):
        y1 = base_top_y + i * (base_height // 3)
        y2 = base_top_y + (i + 1) * (base_height // 3)

        pygame.draw.polygon(screen, color_flag, [
            (width//2 - (base_half_width * (y1 - base_top_y) / base_height), y1),
            (width//2 + (base_half_width * (y1 - base_top_y) / base_height), y1),
            (width//2 + (base_half_width * (y2 - base_top_y) / base_height), y2),
            (width//2 - (base_half_width * (y2 - base_top_y) / base_height), y2),
        ])

    #corner
    pygame.draw.polygon(screen, grey, [top_point, left_point, right_point], 2)

    pygame.display.flip()

pygame.quit()