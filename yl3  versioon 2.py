import pygame
import sys

def run_grid(cell_size, rows, cols, line_color, speed):

    #window suurus
    WIDTH, HEIGHT = cols * cell_size, rows * cell_size
    BG_COLOR = (180, 255, 180)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    #algsuund right
    dx, dy = 1, 0

    #paneb gridi ekraanist välja vastavalt suunale
    def reset():
        return -dx * WIDTH, -dy * HEIGHT

    offset_x, offset_y = reset()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():

            #akna sulgemine ristist
            if event.type == pygame.QUIT:
                running = False

            #nooleklahvid lubavad liigutada direktsiooni
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = 1, 0
                elif event.key == pygame.K_UP:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, 1

                offset_x, offset_y = reset()

        #ruutude liigutamine
        if offset_x != 0:
            offset_x += dx * speed
            if abs(offset_x) < speed:
                offset_x = 0

        if offset_y != 0:
            offset_y += dy * speed
            if abs(offset_y) < speed:
                offset_y = 0

        #drawing
        screen.fill(BG_COLOR)

        for r in range(rows):
            for c in range(cols):
                rect = pygame.Rect(
                    c * cell_size + offset_x,
                    r * cell_size + offset_y,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(screen, line_color, rect, 1)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


#kasutaja input
cell_size = int(input("ruudu size: ") or 20)
rows = int(input("ridade arv: ") or 20)
cols = int(input("veergude arv: ") or 30)
speed = int(input("kiirus: ") or 10)

print("RGB värv (nt 255 0 0):")
try:
    line_color = tuple(map(int, input().split()))
except:
    line_color = (255, 0, 0)

#startup
run_grid(cell_size, rows, cols, line_color, speed)