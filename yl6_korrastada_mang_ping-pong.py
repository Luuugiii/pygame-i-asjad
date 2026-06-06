import pygame
import random

pygame.init()

#background musicccc
pygame.mixer.music.load("music/airship.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

#ekraani size
screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("ping pong mikk-gregor")

#background
bgColor = (200, 230, 255)

#piltide uploadimine
ballImage = pygame.image.load(r"C:\Users\duden\Desktop\coding\pildid\ball.png")
padImage = pygame.image.load(r"C:\Users\duden\Desktop\coding\pildid\Pad.png")

#size muutmine
ballImage = pygame.transform.scale(ballImage, (20, 20))
padImage = pygame.transform.scale(padImage, (120, 20))

#palli settingud
ballX = random.randint(0, screenWidth - 20)
ballY = 0

#palli kiirus
ballSpeed = 5
ballSpeedX = random.choice([-ballSpeed, ballSpeed])
ballSpeedY = ballSpeed

#aluse settingud
padX = screenWidth // 2 - 60
padY = int(screenHeight / 1.5)

#aluse kiirus
padSpeed = 7

#score mangu alguses
score = 0

#font
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(60)

    #mangu kinni panemine
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #aluse liigutamine klaviatuuriga
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        padX -= padSpeed

    if keys[pygame.K_RIGHT]:
        padX += padSpeed

    #alus ei lahe mangust valja
    if padX < 0:
        padX = 0

    if padX > screenWidth - 120:
        padX = screenWidth - 120

    #pall liigub
    ballX += ballSpeedX
    ballY += ballSpeedY

    #seinte bounce
    if ballX <= 0 or ballX >= screenWidth - 20:
        ballSpeedX *= -1

    #ylemine sein
    if ballY <= 0:
        ballSpeedY *= -1

    #mang lopp kui pall puudutab alumist aart
    if ballY >= screenHeight - 20:
        gameOverText = font.render("GAME OVER", True, (255, 0, 0))
        screen.fill(bgColor)
        screen.blit(gameOverText, (220, 220))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    #kokkupuudete kontroll ja score
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