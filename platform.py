import pygame

class platform(pygame.sprite.Sprite):
    def __init__(self, height, width, x1, y1, currentGameController):
        super().__init__()
        self.surf = pygame.Surface([width, height])
        # Texturing platform's surface
        self.texture()
        # Each X positional value gets an offset of 640 added automatically, so that they spawn off-screen by default.
        self.rect = self.surf.get_rect()
        self.rect.topleft = [x1 + 640, y1]
        self.hitbox = self.surf.get_rect()
        self.hitbox.topleft = [x1 + 640, y1]
        self.currentGameController = currentGameController

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
        self.rect.topleft = [self.rect.topleft[0] - self.currentGameController.currentLevelController.moveSpeed, self.rect.topleft[1]]
        self.hitbox.topleft = [self.hitbox.topleft[0] - self.currentGameController.currentLevelController.moveSpeed, self.hitbox.topleft[1]]


class checkpoint(platform):
    def __init__(self, height, width, x1, y1, currentGameController):
        super().__init__(height, width, x1, y1, currentGameController)
        self.completed = False

    def update(self):
        if self.rect.topleft[0] + self.rect.width < 640 and not self.completed:
            self.currentGameController.currentLevelController.levelComplete()
            self.completed = True
        super().update()