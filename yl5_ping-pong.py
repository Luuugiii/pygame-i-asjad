import pygame
import random

pygame.init()

# ekraani size
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("ping pong mikk-gregor")

# background
bgColor = (200, 230, 255)

# piltide laadimine
ballImage = pygame.image.load(r"X:\PyCharmMiscProject\yl5\ball.png")
padImage = pygame.image.load(r"X:\PyCharmMiscProject\yl5\Pad.png")

# suuruste muutmine
ballImage = pygame.transform.scale(ballImage, (20, 20))
padImage = pygame.transform.scale(padImage, (120, 20))

# palli settingud
ballX = random.randint(0, screenWidth - 20)
ballY = 0

# MUUDA PALLI KIIRUST SIIT
ballSpeed = 2

ballSpeedX = random.choice([-ballSpeed, ballSpeed])
ballSpeedY = ballSpeed

# aluse settingud
padX = screenWidth // 2 - 60
padY = int(screenHeight / 1.5)

#aluse kiirus
padSpeed = 5

#punktid
score = 0

# font
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(60)

    #mangu kinni panemine
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #pall liigub
    ballX += ballSpeedX
    ballY += ballSpeedY

    #seinte bounce
    if ballX <= 0 or ballX >= screenWidth - 20:
        ballSpeedX *= -1

    if ballY <= 0:
        ballSpeedY *= -1

    #kui pall valja lendab
    if ballY >= screenHeight - 20:
        score -= 1

        #palli spawn yleval randomly
        ballX = random.randint(0, screenWidth - 20)
        ballY = 0

        #sailitab sama kiirust
        ballSpeedY = ballSpeed
        ballSpeedX = random.choice([-ballSpeed, ballSpeed])

    #alus liigub
    padX += padSpeed

    #direction change
    if padX <= 0 or padX >= screenWidth - 120:
        padSpeed *= -1

    #kokkuporgete tuvastamine
    ballRect = pygame.Rect(ballX, ballY, 20, 20)
    padRect = pygame.Rect(padX, padY, 120, 20)

    if ballRect.colliderect(padRect) and ballSpeedY > 0:
        ballSpeedY *= -1
        score += 1

    #drawing
    screen.fill(bgColor)

    screen.blit(ballImage, (ballX, ballY))
    screen.blit(padImage, (padX, padY))

    #punktide score
    scoreText = font.render(f"punktid: {score}", True, (0, 0, 0))
    screen.blit(scoreText, (10, 10))

    pygame.display.update()

pygame.quit()