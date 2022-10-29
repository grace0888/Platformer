import pygame

class power_ups:
    def __init__(self, type, xCoordinate, yCoordinate, mainCharacter, window):
        self.type = type
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.image = "power up 1.png"
        self.power_up = pygame.image.load(self.image)
        self.width = 50
        self.length = 50
        self.scaledPowerUp = pygame.transform.scale(self.power_up, (self.width, self.length))
        self.start = 0
        self.mainCharacter = mainCharacter
        self.window = window

    def undo_speed(self):
        self.mainCharacter.speed = 5

    def speedUp(self):
        self.mainCharacter.speed = 10

    def speedDown(self):
        self.mainCharacter.speed = 3

    def undo_jump(self):
        self.mainCharacter.limitSpeed = 10

    def jumpHigher(self):
        self.mainCharacter.limitSpeed = 20

    def undo_size(self):
        self.mainCharacter.size = 100
        self.mainCharacter.scaledCharacter = pygame.transform.scale(self.mainCharacter.Character,
                                                               (self.mainCharacter.size, self.mainCharacter.size))
        self.mainCharacter.limitSpeed = 10

    def sizeUp(self):
        self.mainCharacter.size = 150
        self.mainCharacter.scaledCharacter = pygame.transform.scale(self.mainCharacter.Character, (self.mainCharacter.size, self.mainCharacter.size))
        self.mainCharacter.yCoordinate -= 50

    def sizeDown(self):
        self.mainCharacter.size = 50
        self.mainCharacter.scaledCharacter = pygame.transform.scale(self.mainCharacter.Character, (self.mainCharacter.size, self.mainCharacter.size))
        self.mainCharacter.limitSpeed = 13

    def moreHeart(self):
        self.mainCharacter.lives += 1

    def lessHeart(self):
        self.mainCharacter.lives -= 1

    def draw(self):
        self.window.blit(self.scaledPowerUp, (self.xCoordinate, self.yCoordinate))