# Documentation used:
# https://coderslegacy.com/python/pygame-platformer-game-development/
# https://www.pygame.org/docs/ 

# SETUP
import pygame
pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('My Game...')

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([64, 64])
        self.image.fill([255, 255, 255])
        self.rect = self.image.get_rect(center = [100, 100])

gameRunning = True
currentPlayer = player()

sgPlayer = pygame.sprite.Group()
sgPlayer.add(currentPlayer)

while gameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameRunning = False

    gameDisplay.fill((0, 0, 0))

    for entity in sgPlayer:
        gameDisplay.blit(entity.image, entity.rect)

    pygame.display.update()

pygame.quit()
quit()