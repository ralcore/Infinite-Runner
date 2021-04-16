# Documentation used:
# https://coderslegacy.com/python/pygame-platformer-game-development/
# https://www.pygame.org/docs/

# SETUP 
import pygame
pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('My Game...')

class platform(pygame.sprite.Sprite):
    def __init__(self, height, width, x1, y1):
        super().__init__()
        self.surf = pygame.Surface([width, height])
        self.surf.fill([255, 255, 255])
        self.rect = self.surf.get_rect()
        self.rect.topleft = [x1, y1]
        self.hitbox = self.surf.get_rect()
        self.hitbox.topleft = [x1, y1]

    def update(self):
        pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)

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

        self.grounded = False

    def update(self):
        self.vel.y += 0.03
        self.vel.y = self.vel.y/1.01
        self.oldpos.xy = self.pos.xy
        self.pos.xy += self.vel.xy * dt
        self.checkCollision()
        self.rect.topleft = [self.pos.x, self.pos.y]
        self.hitbox.topleft = [self.pos.x, self.pos.y]
        pygame.draw.rect(gameDisplay, (255, 0, 0), self.hitbox, 2)

    def checkCollision(self):
        # This function takes the new and old positions of the player,
        # checking whether they have collided with a platform, and if they have,
        # checks what side they collided with, calling the corresponding function.

        # Using clipline to clip the line between new and old pos into each rectangle
        # See this documentation for more info: https://www.pygame.org/docs/ref/rect.html#pygame.Rect.clipline
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
            elif self.getClipLine("down", 0, 0, platform) or self.getClipLine("down", 0, 0.5, platform) or self.getClipLine("down", 0, 1, platform):
                self.collidePlatformBottom(platform)

    def getClipLine(self, checkedSide, xOffset, yOffset, platform):
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
            if checkedSide == "up":
                return True if clippedLine[0][1] == platform.hitbox.top else False
            if checkedSide == "down":
                return True if clippedLine[0][1] == platform.hitbox.bottom else False
            if checkedSide == "left":
                return True if clippedLine[0][0] == platform.hitbox.left else False
            if checkedSide == "right":
                return True if clippedLine[0][0] == platform.hitbox.right - 1 else False
        else:
            # No collision, guaranteed a false call
            return False

    def move(self, direction):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.vel.x -= 0.015
        if pressed_keys[pygame.K_RIGHT]:
            self.vel.x += 0.015
        if not (pressed_keys[pygame.K_LEFT] ^ pressed_keys[pygame.K_RIGHT]):
            self.vel.x = self.vel.x/1.075
        if pressed_keys[pygame.K_UP] & self.grounded == True:
            self.vel.y -= 1
            self.grounded = False

    def collidePlatformTop(self, platform):
        self.vel.y = 0
        self.pos.y = platform.hitbox.top - self.hitbox.height
        self.grounded = True

    def collidePlatformLeft(self, platform):
        self.vel.x = 0
        self.pos.x = platform.hitbox.left - self.hitbox.width
        self.grounded = True

    def collidePlatformRight(self, platform):
        self.vel.x = 0
        self.pos.x = platform.hitbox.right
        self.grounded = True

    def collidePlatformBottom(self, platform):
        self.vel.y = 0
        self.pos.y = platform.hitbox.bottom

gameRunning = True
currentPlayer = player()
testingPlatform = platform(64, 256, 100, 300)
testingPlatform2 = platform(64, 256, 500, 400)

sgPlatforms = pygame.sprite.Group()
sgPlatforms.add(testingPlatform)
sgPlatforms.add(testingPlatform2)

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

    currentPlayer.move("right")

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