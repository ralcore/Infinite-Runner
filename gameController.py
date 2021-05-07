import pygame
import pygame.freetype
import levelController
import player

class gameController:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.gameState = "title"
        self.currentPlayer = player.player(self, self.gameDisplay)
        self.currentLevelController = levelController.levelController(0, self, self.gameDisplay)
        self.clock = pygame.time.Clock()
        self.dt = 0
        # Setting up fonts
        self.freeTypeFontLarge = pygame.freetype.Font("Thirteen-Pixel-Fonts.ttf", 72)
        self.freeTypeFontSmall = pygame.freetype.Font("Anti.biz_DigitalDrip_TTF.ttf", 32)

    def startGame(self):
        self.gameState = "playing"
        self.currentPlayer = player.player(self, self.gameDisplay)
        self.currentLevelController = levelController.levelController(2, self, self.gameDisplay)

    def endGame(self):
        self.gameState = "dead"
        self.currentLevelController.endGame()

    def update(self):
        # 60fps lock
        self.dt = self.clock.tick(60)

        # If pressing escape, quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        # We always fill the screen black
        self.gameDisplay.fill((0, 0, 0))
        # Main state machine
        if self.gameState == "title":
            self.drawTitleUI()
            self.currentLevelController.update()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RETURN]:
                self.startGame()
        if self.gameState == "playing":
            self.drawPlayingUI()
            self.currentPlayer.update()
            self.currentLevelController.update()
            self.gameDisplay.blit(self.currentPlayer.surf, self.currentPlayer.rect)
        elif self.gameState == "dead":
            self.currentLevelController.update()
            self.drawDeadUI()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RETURN]:
                self.startGame()
        pygame.display.update()
        return True

    def drawPlayingUI(self):
        text_surface, rect = self.freeTypeFontLarge.render(str(self.currentLevelController.moveSpeed / 2) + "x", (40, 40, 40))
        self.gameDisplay.blit(text_surface, (20, 20))
        text_surface, rect = self.freeTypeFontSmall.render(str(self.currentLevelController.moveSpeed * 1000 + self.currentLevelController.frameCounter) + "pts", (40, 40, 40))
        self.gameDisplay.blit(text_surface, (630 - text_surface.get_width(), 10))

    def drawDeadUI(self):
        text_surface, rect = self.freeTypeFontLarge.render("whoops!", (140, 0, 50))
        self.gameDisplay.blit(text_surface, (320-text_surface.get_width()/2, 200-text_surface.get_height()/2))
        text_surface, rect = self.freeTypeFontSmall.render(("score: " + str(self.currentLevelController.frameCounter) + " - enter to reset"), (160, 50, 50))
        self.gameDisplay.blit(text_surface, (320-text_surface.get_width()/2, 260-text_surface.get_height()/2))

    def drawTitleUI(self):
        text_surface, rect = self.freeTypeFontLarge.render("schmoovin'", (140, 0, 0))
        self.gameDisplay.blit(text_surface, (320-text_surface.get_width()/2, 200-text_surface.get_height()/2))
        text_surface, rect = self.freeTypeFontSmall.render("press enter to start", (140, 0, 50))
        self.gameDisplay.blit(text_surface, (320-text_surface.get_width()/2, 280-text_surface.get_height()/2))