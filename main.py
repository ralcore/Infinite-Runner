# Documentation used:
# https://coderslegacy.com/python/pygame-platformer-game-development/
# https://www.pygame.org/docs/
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
# https://www.1001fonts.com/thirteen-pixel-fonts-font.html
# https://www.1001fonts.com/digitaldrip-font.html

# SETUP
import pygame
import gameController
pygame.init()
gameDisplay = pygame.display.set_mode((640, 480))
pygame.display.set_caption('My Game...')

currentGameController = gameController.gameController(gameDisplay)
gameRunning = True

while gameRunning:
    gameRunning = currentGameController.update()
    # If pressing escape, quit game

pygame.quit()
quit()
