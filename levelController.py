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