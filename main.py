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
        self.vel = pygame.Vector2()
        self.pos.xy = 100, 100
        self.vel.xy = 0, 0

        self.grounded = False

    def update(self):
        self.vel.y += 0.03
        self.vel.y = self.vel.y/1.01
        for platform in sgPlatforms:
            if self.checkCollision():
                self.collidePlatform(platform)
                print("hello")
        self.oldpos.xy = self.vel.xy
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
        for entity in sgPlatforms:
            self.clippedLine = entity.hitbox.clipline(self.oldpos, self.newpos)
            if self.clippedLine:
                self.start, self.end = self.clippedLine
                self.clx1, self.cly1 = self.start
                self.clx2, self.cly2 = self.end
                if self.cly1 == entity.hitbox.top:
                    # We know that the player has collided with the top of the rect, so we call that function:
                    self.collidePlatformTop(entity)



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
        if self.vel.y > 0 & platform.hitbox.top <= self.hitbox.bottom <= platform.hitbox.top + 30:
            self.vel.y = 0
            # TODO: Fix reverse coyote time on this, no idea why this doesn't align the box
            self.hitbox.bottom = platform.hitbox.top
            self.grounded = True

gameRunning = True
currentPlayer = player()
testingPlatform = platform(64, 256, 100, 300)
testingPlatform2 = platform(64, 256, 500, 400)

sgPlatforms = pygame.sprite.Group()
sgPlatforms.add(testingPlatform)

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