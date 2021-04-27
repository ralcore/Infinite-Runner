# Documentation used:
# https://coderslegacy.com/python/pygame-platformer-game-development/
# https://www.pygame.org/docs/
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
# https://www.1001fonts.com/thirteen-pixel-fonts-font.html
# https://www.1001fonts.com/digitaldrip-font.html

# SETUP 
import pygame
import pygame.freetype
from random import *
pygame.init()
gameDisplay = pygame.display.set_mode((640, 480))
pygame.display.set_caption('My Game...')
# Setting up fonts
freeTypeFontLarge = pygame.freetype.Font("Thirteen-Pixel-Fonts.ttf", 72)
freeTypeFontSmall = pygame.freetype.Font("Anti.biz_DigitalDrip_TTF.ttf", 32)

class platform(pygame.sprite.Sprite):
    def __init__(self, height, width, x1, y1):
        super().__init__()
        self.surf = pygame.Surface([width, height])
        # Texturing platform's surface
        self.texture()
        # Each X positional value gets an offset of 640 added automatically, so that they spawn off-screen by default.
        self.rect = self.surf.get_rect()
        self.rect.topleft = [x1 + 640, y1]
        self.hitbox = self.surf.get_rect()
        self.hitbox.topleft = [x1 + 640, y1]

    def texture(self):
        # This function directly draws to the surface to create a pixel-like texture,
        # without the need to store .pngs.
        # These graphics are produced dynamically using pg's PixelArray functions
        # I wouldn't have to do this if pygame had native 9-patch support, but here we are LOL
        self.surf.fill([0, 0, 0])
        pxArray = pygame.PixelArray(self.surf)
        WHITE_END = 4
        LG_END = 8
        DG_END = 12
        # Left side
        pxArray[:WHITE_END] = (255, 255, 255)
        pxArray[WHITE_END:LG_END] = (160, 160, 160)
        pxArray[LG_END:DG_END] = (80, 80, 80)
        # Right side
        pxArray[-DG_END:-LG_END] = (80, 80, 80)
        pxArray[-LG_END:-WHITE_END] = (160, 160, 160)
        pxArray[-WHITE_END:] = (255, 255, 255)
        # Top side
        pxArray[:, :WHITE_END] = (255, 255, 255)
        pxArray[4:-4, WHITE_END:LG_END] = (160, 160, 160)
        pxArray[8:-8, LG_END:DG_END] = (80, 80, 80)
        # Bottom side
        pxArray[8:-8, -DG_END:-LG_END] = (80, 80, 80)
        pxArray[4:-4, -LG_END:-WHITE_END] = (160, 160, 160)
        pxArray[:, -WHITE_END:] = (255, 255, 255)
        pxArray.close()

    def update(self):
        # Debug to show hitbox: pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)
        self.rect.topleft = [self.rect.topleft[0] - currentGameController.currentLevelController.moveSpeed, self.rect.topleft[1]]
        self.hitbox.topleft = [self.hitbox.topleft[0] - currentGameController.currentLevelController.moveSpeed, self.hitbox.topleft[1]]


class checkpoint(platform):
    def __init__(self, height, width, x1, y1):
        super().__init__(height, width, x1, y1)
        self.completed = False

    def update(self):
        if self.rect.topleft[0] + self.rect.width < 640 and not self.completed:
            currentGameController.currentLevelController.levelComplete()
            self.completed = True
        super().update()


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2()
        self.oldpos = pygame.Vector2()
        self.vel = pygame.Vector2()
        self.pos.xy = 100, 100
        self.oldpos.xy = self.pos.xy
        self.vel.xy = 0, 0

        self.surf = pygame.Surface([64, 64])
        self.texture()
        self.surf.fill([255, 255, 255])
        self.rect = self.surf.get_rect()
        self.hitbox = self.surf.get_rect()

        self.grounded = "airborne"

    def texture(self):
        # Very similar to the platform's texture function, but now with eyes
        self.surf.fill([0, 0, 0])
        pxArray = pygame.PixelArray(self.surf)
        WHITE_END = 4
        LG_END = 8
        DG_END = 12
        # Left side
        pxArray[:WHITE_END] = (255, 255, 255)
        pxArray[WHITE_END:LG_END] = (160, 160, 160)
        pxArray[LG_END:DG_END] = (80, 80, 80)
        # Right side
        pxArray[-DG_END:-LG_END] = (80, 80, 80)
        pxArray[-LG_END:-WHITE_END] = (160, 160, 160)
        pxArray[-WHITE_END:] = (255, 255, 255)
        # Top side
        pxArray[:, :WHITE_END] = (255, 255, 255)
        pxArray[4:-4, WHITE_END:LG_END] = (160, 160, 160)
        pxArray[8:-8, LG_END:DG_END] = (80, 80, 80)
        # Bottom side
        pxArray[8:-8, -DG_END:-LG_END] = (80, 80, 80)
        pxArray[4:-4, -LG_END:-WHITE_END] = (160, 160, 160)
        pxArray[:, -WHITE_END:] = (255, 255, 255)
        # Setting eye "direction"
        eyepos = pygame.Vector2()
        eyepos.xy = (pxArray.shape[0]/2, pxArray.shape[1]/2)
        if self.vel.x < 0:
            eyepos.x -= 16
        else:
            eyepos.x += 16
        # Then, setting how high up/down the player is looking
        eyepos.y += self.vel.y * 20
        # Drawing left eye
        pxArray[int(eyepos.x-16):int(eyepos.x-8), int(eyepos.y-4):int(eyepos.y+4)] = (255, 255, 255)
        # Drawing right eye
        pxArray[int(eyepos.x+8):int(eyepos.x+16), int(eyepos.y-4):int(eyepos.y+4)] = (255, 255, 255)

    def update(self):
        self.updateMovement()
        self.checkCollision()
        self.checkDeath()
        self.texture()
        # Scrolling effect
        self.pos.x -= currentGameController.currentLevelController.moveSpeed
        # Updating player visual position on-screen
        self.rect.topleft = [self.pos.x, self.pos.y]
        self.hitbox.topleft = [self.pos.x, self.pos.y]
        # Debug to show hitbox: pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)

    def checkDeath(self):
        if self.hitbox.topleft[0] < -8-self.hitbox.width or self.hitbox.topleft[1] > gameDisplay.get_width():
            currentGameController.endGame()
            # Put the player far off-screen
            self.pos.y = -1000

    def checkCollision(self):
        # Checks all 4 sides with three contact points using getClipLine to call the respective collidePlatform func
        for spriteGroup in currentGameController.currentLevelController.loadedPlats:
            for platform in spriteGroup:
                # Checking for a top collision using three points of potential contact:
                if self.getClipLine("up", 0, 1, platform) or self.getClipLine("up", 0.5, 1, platform) or self.getClipLine("up", 1, 1, platform):
                    self.collidePlatformTop(platform)
                # Left of platform collision, same deal:
                elif self.getClipLine("left", 1, 0, platform) or self.getClipLine("left", 1, 0.5, platform) or self.getClipLine("left", 1, 1, platform):
                    self.collidePlatformLeft(platform)
                # Right of platform:
                elif self.getClipLine("right", 0, 0, platform) or self.getClipLine("right", 0, 0.5, platform) or self.getClipLine("right", 0, 1, platform):
                    self.collidePlatformRight(platform)
                # And finally, the bottom:
                elif self.getClipLine("down", 0, 0, platform) or self.getClipLine("down", 0.5, 0, platform) or self.getClipLine("down", 1, 0, platform):
                    self.collidePlatformBottom(platform)

    def getClipLine(self, checkedSide, xOffset, yOffset, platform):
        # This function uses a clipped line and predicted position to check whether the player will intercept a platform
        # checkedSide specifies whether we're checking a vertical collision or a horizontal one
        # In effect, whether to consider the resultant X or Y value of the line and which side of the plat to check
        # xOffset and yOffset are multiples of the player height and width
        # For example, to check from the middle of the player's width, xOffset should be 0.5
        clippedLine = platform.hitbox.clipline(self.oldpos.x + self.hitbox.width * xOffset,
                                               self.oldpos.y + self.hitbox.height * yOffset,
                                               self.pos.x + self.hitbox.width * xOffset,
                                               self.pos.y + self.hitbox.height * yOffset)
        if clippedLine:
            # Debug code to show clipped line: pygame.draw.line(gameDisplay, 'blue', clippedLine[0], clippedLine[1], 4)
            # Checking if the trimmed line starts on the relevant edge
            # If it does, then the player will pass through the platform on the next frame,
            # so we need to proc a collision
            # Hitboxes are inclusive on one side and exclusive on the other, so we need to -1 on right and bottom
            if checkedSide == "up":
                return True if clippedLine[0][1] == platform.hitbox.top else False
            if checkedSide == "down":
                return True if clippedLine[0][1] == platform.hitbox.bottom - 1 else False
            if checkedSide == "left":
                return True if clippedLine[0][0] == platform.hitbox.left else False
            if checkedSide == "right":
                return True if clippedLine[0][0] == platform.hitbox.right - 1 else False
        else:
            # No collision, guaranteed a false call
            return False

    def updateMovement(self):
        # Adding left/right momentum
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.vel.x -= 0.015
        if pressed_keys[pygame.K_RIGHT]:
            self.vel.x += 0.015
        # If not moving, decelerate the player
        if not (pressed_keys[pygame.K_LEFT] ^ pressed_keys[pygame.K_RIGHT]):
            self.vel.x = self.vel.x/1.075
        # Jumping
        if pressed_keys[pygame.K_UP]:
            if self.grounded == "grounded":
                self.vel.y = -0.9
            elif self.grounded == "leftwall":
                self.vel.y = -0.7
                self.vel.x = -0.4
            elif self.grounded == "rightwall":
                self.vel.y = -0.7
                self.vel.x = 0.4
            self.grounded = "airborne"
        # Applying gravity + terminal velocity
        self.vel.y += 0.03
        self.vel.y = self.vel.y/1.01
        # Saving the old position to memory, and finally applying our velocity changes
        self.oldpos.xy = self.pos.xy
        self.pos.xy += self.vel.xy * currentGameController.dt

    def collidePlatformTop(self, platform):
        self.grounded = "grounded"
        if self.vel.y > 0:
            self.vel.y = 0
        if self.pos.y > platform.hitbox.top - self.hitbox.height:
            self.pos.y = platform.hitbox.top - self.hitbox.height

    def collidePlatformLeft(self, platform):
        self.grounded = "leftwall"
        if self.vel.x > 0:
            self.vel.x = 0
        if self.pos.x > platform.hitbox.left - self.hitbox.width:
            self.pos.x = platform.hitbox.left - self.hitbox.width

    def collidePlatformRight(self, platform):
        self.grounded = "rightwall"
        if self.vel.x < 0:
            self.vel.x = 0
        if self.pos.x < platform.hitbox.right:
            self.pos.x = platform.hitbox.right

    def collidePlatformBottom(self, platform):
        if self.vel.y < 0:
            self.vel.y = 0
        if self.pos.y < platform.hitbox.bottom:
            self.pos.y = platform.hitbox.bottom


class levelController:
    def __init__(self, moveSpeed):
        self.loadedPlats = []
        self.addLevel(0)
        self.moveSpeed = moveSpeed
        self.frameCounter = 0

    def endGame(self):
        # Setting framecounter to total frames lived, undoing resets
        self.frameCounter += self.moveSpeed * 1000
        self.moveSpeed = 0

    def addLevel(self, level):
        self.loadedPlats.append(pygame.sprite.Group())
        if level == 0:
            # Since platforms load off-screen (640px right) by default, the tutorial area uses negative X values
            # to offset it back on-screen when loaded at the start of the game.
            # This solution isn't very expandable, but since it's a single edge case for a level that never gets
            # loaded randomly, I'm allowing it.
            # Floor with some boxes to jump
            self.loadedPlats[-1].add(checkpoint(500, 1850, -690, 400))
            self.loadedPlats[-1].add(platform(100, 50, 0, 100))
            self.loadedPlats[-1].add(platform(100, 10, 20, 0))
            self.loadedPlats[-1].add(platform(200, 200, 200, 200))
            # Walljump section
            self.loadedPlats[-1].add(platform(350, 200, 500, -50))
            self.loadedPlats[-1].add(platform(300, 200, 800, 100))
        elif level == 1:
            # Triple plats
            self.loadedPlats[-1].add(platform(50, 200, 0, 400))
            self.loadedPlats[-1].add(platform(50, 200, 400, 300))
            self.loadedPlats[-1].add(checkpoint(50, 200, 800, 400))
        elif level == 2:
            # Forced drop-walljump to walljump to forced drop-walljump
            self.loadedPlats[-1].add(platform(200, 100, 0, 400))
            self.loadedPlats[-1].add(platform(350, 50, 225, -50))
            self.loadedPlats[-1].add(platform(200, 100, 400, 400))
            self.loadedPlats[-1].add(platform(290, 50, 625, 180))
            self.loadedPlats[-1].add(platform(200, 100, 800, 400))
            self.loadedPlats[-1].add(platform(350, 50, 1025, -50))
            self.loadedPlats[-1].add(checkpoint(200, 100, 1200, 400))
        elif level == 3:
            # Walljump up and down a bit
            self.loadedPlats[-1].add(platform(200, 200, 0, 400))
            self.loadedPlats[-1].add(platform(500, 100, 100, -200))
            self.loadedPlats[-1].add(platform(350, 100, 300, 150))
            self.loadedPlats[-1].add(platform(250, 100, 300, -200))
            self.loadedPlats[-1].add(platform(500, 100, 500, -200))
            self.loadedPlats[-1].add(checkpoint(200, 200, 500, 400))
        elif level == 4:
            # Forced walljump storage
            # Staircase
            self.loadedPlats[-1].add(platform(300, 200, 0, 400))
            self.loadedPlats[-1].add(platform(400, 100, 200, 300))
            self.loadedPlats[-1].add(platform(200, 100, 300, 200))
            # Overhang
            self.loadedPlats[-1].add(platform(50, 50, 400, 200))
            self.loadedPlats[-1].add(platform(25, 25, 400, 250))
            # Big wall + final floor
            self.loadedPlats[-1].add(platform(300, 100, 900, -50))
            self.loadedPlats[-1].add(checkpoint(100, 300, 900, 400))
        # elif level == 5:
        #     # Forced walljump cannon - guaranteed the worst level LOL - commented out for your sanity
        #     # Starting plat
        #     self.loadedPlats[-1].add(platform(300, 400, 0, 400))
        #     # Walljump cannon block
        #     self.loadedPlats[-1].add(platform(65, 50, 350, 335))
        #     # Left platform to walljump off of (for turning around after initial WJ)
        #     self.loadedPlats[-1].add(platform(110, 50, 150, -50))
        #     # Blind jumps, because I'm committed to this being a run killer at this point
        #     self.loadedPlats[-1].add(platform(40, 40, 450, 40))
        #     self.loadedPlats[-1].add(platform(40, 40, 600, 40))
        #     self.loadedPlats[-1].add(platform(40, 40, 750, 40))
        #     self.loadedPlats[-1].add(platform(40, 40, 900, 80))
        #     self.loadedPlats[-1].add(platform(40, 40, 1200, 160))
        #     self.loadedPlats[-1].add(platform(40, 40, 1600, 200))
        #     self.loadedPlats[-1].add(checkpoint(40, 40, 2100, 240))

    def removeOldLevel(self):
        if len(self.loadedPlats) >= 4:
            self.loadedPlats.pop(0)

    def update(self):
        if currentGameController.gameState == "playing":
            self.frameCounter += 1
            if self.frameCounter > 1000:
                self.moveSpeed += 1
                self.frameCounter = 0
        for spriteGroup in self.loadedPlats:
            for platform in spriteGroup:
                gameDisplay.blit(platform.surf, platform.rect)
                platform.update()

    def levelComplete(self):
        self.addLevel(randint(1, 4))
        self.removeOldLevel()


class gameController:
    def __init__(self):
        self.gameState = "title"
        self.currentPlayer = player()
        self.currentLevelController = levelController(0)
        self.clock = pygame.time.Clock()
        self.dt = 0

    def startGame(self):
        self.gameState = "playing"
        self.currentPlayer = player()
        self.currentLevelController = levelController(2)

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
        gameDisplay.fill((0, 0, 0))
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
            gameDisplay.blit(self.currentPlayer.surf, self.currentPlayer.rect)
        elif self.gameState == "dead":
            self.currentLevelController.update()
            self.drawDeadUI()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RETURN]:
                self.startGame()
        pygame.display.update()
        return True

    def drawPlayingUI(self):
        text_surface, rect = freeTypeFontLarge.render(str(currentGameController.currentLevelController.moveSpeed / 2) + "x", (40, 40, 40))
        gameDisplay.blit(text_surface, (20, 20))
        text_surface, rect = freeTypeFontSmall.render(str(currentGameController.currentLevelController.moveSpeed * 1000 + currentGameController.currentLevelController.frameCounter) + "pts", (40, 40, 40))
        gameDisplay.blit(text_surface, (630 - text_surface.get_width(), 10))

    def drawDeadUI(self):
        text_surface, rect = freeTypeFontLarge.render("whoops!", (140, 0, 50))
        gameDisplay.blit(text_surface, (320-text_surface.get_width()/2, 200-text_surface.get_height()/2))
        text_surface, rect = freeTypeFontSmall.render(("score: " + str(currentGameController.currentLevelController.frameCounter) + " - enter to reset"), (160, 50, 50))
        gameDisplay.blit(text_surface, (320-text_surface.get_width()/2, 260-text_surface.get_height()/2))

    def drawTitleUI(self):
        text_surface, rect = freeTypeFontLarge.render("schmoovin'", (140, 0, 0))
        gameDisplay.blit(text_surface, (320-text_surface.get_width()/2, 200-text_surface.get_height()/2))
        text_surface, rect = freeTypeFontSmall.render("press enter to start", (140, 0, 50))
        gameDisplay.blit(text_surface, (320-text_surface.get_width()/2, 280-text_surface.get_height()/2))


currentGameController = gameController()
gameRunning = True

while gameRunning:
    gameRunning = currentGameController.update()
    # If pressing escape, quit game

pygame.quit()
quit()