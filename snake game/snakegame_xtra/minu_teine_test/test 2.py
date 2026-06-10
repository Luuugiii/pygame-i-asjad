import pygame, sys, time, random

difficulty = 25

frame_size_x = 720
frame_size_y = 480

pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

black = pygame.Color(0, 80, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

fps_controller = pygame.time.Clock()

snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

food_pos = [random.randrange(1, (frame_size_x // 10)) * 10,
            random.randrange(1, (frame_size_y // 10)) * 10]

food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0
high_score = 0
paused = False


def invert_surface(surface):
    w, h = surface.get_size()
    inverted = pygame.Surface((w, h)).convert()

    for x in range(w):
        for y in range(h):
            r, g, b, _ = surface.get_at((x, y))
            inverted.set_at((x, y), (255 - r, 255 - g, 255 - b))

    return inverted


def game_over():
    font = pygame.font.SysFont('times new roman', 70)
    surf = font.render('YOU DIED', True, red)

    rect = surf.get_rect(center=(frame_size_x / 2, frame_size_y / 3))

    game_window.fill(black)
    game_window.blit(surf, rect)

    show_score()

    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()


def show_score():
    font = pygame.font.SysFont('consolas', 20)
    surf = font.render(f"Score: {score}  High: {high_score}", True, white)
    game_window.blit(surf, (10, 10))


def pause_menu():
    snapshot = game_window.copy()
    inverted = invert_surface(snapshot)

    overlay = pygame.Surface((frame_size_x, frame_size_y))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))
    inverted.blit(overlay, (0, 0))

    game_window.blit(inverted, (0, 0))

    big = pygame.font.SysFont('times new roman', 60)
    small = pygame.font.SysFont('consolas', 22)

    title = big.render("PAUSED", True, white)
    game_window.blit(title, title.get_rect(center=(frame_size_x / 2, frame_size_y / 3)))

    s1 = small.render(f"Score: {score}", True, white)
    s2 = small.render(f"High Score: {high_score}", True, white)
    s3 = small.render("Press P to continue", True, white)

    game_window.blit(s1, s1.get_rect(center=(frame_size_x / 2, frame_size_y / 2)))
    game_window.blit(s2, s2.get_rect(center=(frame_size_x / 2, frame_size_y / 2 + 30)))
    game_window.blit(s3, s3.get_rect(center=(frame_size_x / 2, frame_size_y / 2 + 70)))

    pygame.display.update()


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                paused = not paused

            if not paused:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    if paused:
        pause_menu()
        continue

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))

    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        if score > high_score:
            high_score = score
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // 10)) * 10,
                    random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True

    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white,
                     pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    show_score()

    if snake_pos[0] < 0 or snake_pos[0] >= frame_size_x:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] >= frame_size_y:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    pygame.display.update()
    fps_controller.tick(difficulty)
