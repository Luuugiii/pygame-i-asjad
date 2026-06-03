import pygame
import random

pygame.init()

#ekraani size
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("ping pong mikk-gregor")

#background
bgColor = (200, 230, 255)

#piltide laadimine
ballImage = pygame.image.load(r"X:\PyCharmMiscProject\yl5\ball.png")
padImage = pygame.image.load(r"X:\PyCharmMiscProject\yl5\Pad.png")

#suuruste muutmine
ballImage = pygame.transform.scale(ballImage, (20, 20))
padImage = pygame.transform.scale(padImage, (120, 20))

#palli settingud
ballX = screenWidth // 2
ballY = screenHeight // 2

ballSpeedX = 4
ballSpeedY = 4

#aluse settingud
padX = screenWidth // 2 - 60
padY = int(screenHeight / 1.5)

padSpeed = 5

#punktid
score = 0

#font
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(60)

    #mangu closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #pall
    ballX += ballSpeedX
    ballY += ballSpeedY

    #seinte põrkamine
    if ballX <= 0 or ballX >= screenWidth - 20:
        ballSpeedX *= -1

    if ballY <= 0:
        ballSpeedY *= -1

    #alumine corner
    if ballY >= screenHeight - 20:
        score -= 1

        #palli taastamine keskele
        ballX = screenWidth // 2
        ballY = screenHeight // 2

        #random suund
        ballSpeedY = -4
        ballSpeedX = random.choice([-4, 4])

    #alus/pad
    padX += padSpeed

    #suuna vahetamine
    if padX <= 0 or padX >= screenWidth - 120:
        padSpeed *= -1

    #kokkuporge
    ballRect = pygame.Rect(ballX, ballY, 20, 20)
    padRect = pygame.Rect(padX, padY, 120, 20)

    if ballRect.colliderect(padRect) and ballSpeedY > 0:
        ballSpeedY *= -1
        score += 1

    #drawing
    screen.fill(bgColor)

    screen.blit(ballImage, (ballX, ballY))
    screen.blit(padImage, (padX, padY))

    #scoreboard
    scoreText = font.render(f"Punktid: {score}", True, (0, 0, 0))
    screen.blit(scoreText, (10, 10))

    pygame.display.update()

pygame.quit()