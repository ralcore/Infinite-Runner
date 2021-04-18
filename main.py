# Documentation used:
# https://coderslegacy.com/python/pygame-platformer-game-development/
# https://www.pygame.org/docs/

# SETUP 
import pygame
pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('My Game...')

class platform(pygame.sprite.Sprite):
    def __init__(self, height, width, x1, y1, topStyle):
        super().__init__()
        self.surf = pygame.Surface([width, height])
        self.surf.fill('black')
        # Texturing platform's surface
        self.texture("top", topStyle)
        self.rect = self.surf.get_rect()
        self.rect.topleft = [x1, y1]
        self.hitbox = self.surf.get_rect()
        self.hitbox.topleft = [x1, y1]

    def texture(self, side, style):
        # This function takes two inputs which describe the style a given side of the platform should have.
        # "textured": a textured line, for use where we want the player to land
        # "filled": a full white line, used where the player can land, but probably shouldn't
        # "dotted": a dotted white/grey/black line, used to lead into pits and the sort
        # "blank": a blank line, only to ever be used out of bounds.
        # These graphics are produced dynamically using pg's PixelArray functions
        # I wouldn't have to do this if pygame had native 9-patch support, but here we are LOL
        self.surf.fill([255, 255, 255])
        pxArray = pygame.PixelArray(self.surf)
        if side == "top":
            if style == "textured":
                pxArray[0:8] = (255, 255, 255)
                pxArray[0:8, 24::32] = (0, 0, 0)
                pxArray[8:16, 24::32] = (255, 255, 255)
                pxArray[16:24, 16::32] = (255, 255, 255)
            if style == "filled":
                pxArray[0:8] = (255, 255, 255)
            if style == "dotted":
                pxArray[0:8] = (255, 255, 255)
                pxArray[0:8, 64:128:32] = (0, 0, 0)
                pxArray[0:8, 128::16] = (0, 0, 0)
            if style == "blank":
                pxArray[0:8] = (0, 0, 0)

    def update(self):
        print("hello")
        # pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface([64, 64])
        self.surf.fill([255, 255, 255])
        self.rect = self.surf.get_rect()
        self.hitbox = self.surf.get_rect()

        self.pos = pygame.Vector2()
        self.oldpos = pygame.Vector2()
        self.vel = pygame.Vector2()
        self.pos.xy = 100, 100
        self.oldpos.xy = self.pos.xy
        self.vel.xy = 0, 0

        self.grounded = "airborne"

    def update(self):
        self.updateMovement()
        self.checkCollision()
        # Updating player visual position on-screen
        self.rect.topleft = [self.pos.x, self.pos.y]
        self.hitbox.topleft = [self.pos.x, self.pos.y]
        pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)

    def checkCollision(self):
        # Checks all 4 sides with three contact points using getClipLine to call the respective collidePlatform func
        for platform in sgPlatforms:
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
            # Trimming to the relevant coordinate value
            pygame.draw.line(gameDisplay, 'blue', clippedLine[0], clippedLine[1], 4)
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
        self.pos.xy += self.vel.xy * dt

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

gameRunning = True
currentPlayer = player()
testingPlatform = platform(64, 256, 100, 300, "textured")
testingPlatform2 = platform(64, 256, 500, 400, "filled")
testingPlatform3 = platform(64, 256, 300, 100, "dotted")
testingPlatform4 = platform(256, 64, 700, 100, "empty")

sgPlatforms = pygame.sprite.Group()
sgPlatforms.add(testingPlatform)
sgPlatforms.add(testingPlatform2)
sgPlatforms.add(testingPlatform3)
sgPlatforms.add(testingPlatform4)

sgPlayer = pygame.sprite.Group()
sgPlayer.add(currentPlayer)

clock = pygame.time.Clock()
dt = 0

while gameRunning:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameRunning = False

    gameDisplay.fill((0, 0, 0))

    for entity in sgPlatforms:
        gameDisplay.blit(entity.surf, entity.rect)
        entity.update()
    for entity in sgPlayer:
        gameDisplay.blit(entity.surf, entity.rect)
        entity.update()

    pygame.display.update()

pygame.quit()
quit()