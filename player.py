import pygame


class player(pygame.sprite.Sprite):
    def __init__(self, currentGameController, gameDisplay):
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
        self.currentGameController = currentGameController
        self.gameDisplay = gameDisplay

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
        self.pos.x -= self.currentGameController.currentLevelController.moveSpeed
        # Updating player visual position on-screen
        self.rect.topleft = [self.pos.x, self.pos.y]
        self.hitbox.topleft = [self.pos.x, self.pos.y]
        # Debug to show hitbox: pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)

    def checkDeath(self):
        if self.hitbox.topleft[0] < -8-self.hitbox.width or self.hitbox.topleft[1] > self.gameDisplay.get_width():
            self.currentGameController.endGame()
            # Put the player far off-screen
            self.pos.y = -1000

    def checkCollision(self):
        # Checks all 4 sides with three contact points using getClipLine to call the respective collidePlatform func
        for spriteGroup in self.currentGameController.currentLevelController.loadedPlats:
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
        self.pos.xy += self.vel.xy * self.currentGameController.dt

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