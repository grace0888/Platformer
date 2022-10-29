import pygame
import time

class characterBox:
    def __init__(self, image, speed, xCoordinate, yCoordinate, size, characterChosen, window, windowWidth, windowLength, platformList, activePowerUpList, powerUpList):
        self.image = image
        self.speed = speed
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.size = size
        self.Character = pygame.image.load(self.image)
        self.scaledCharacter = pygame.transform.scale(self.Character,
                                                      (self.size, self.size))
        self.originalX = xCoordinate
        self.originalY = yCoordinate
        self.rectangleList = []
        if characterChosen == "jenny":
            self.jennyRectangles()
        if characterChosen == "ella":
            self.ellaRectangles()
        # positive vertical speed means the character is going up
        self.verticalSpeed = 0
        self.limitSpeed = 10
        self.movingRight = False
        self.movingLeft = False
        self.lives = 3
        self.window = window
        self.windowWidth = windowWidth
        self.windowLength = windowLength
        self.platformList = platformList
        self.activePowerUpList = activePowerUpList
        self.powerUpList = powerUpList

    # goes up with the up button
    def characterUp(self):
        if self.yCoordinate > 0:
            self.verticalSpeed = self.limitSpeed
            # self.yCoordinate -= 10 * self.speed

    # goes to the right with the right button
    def characterRight(self):
        if self.xCoordinate < self.windowWidth - self.size:
            self.xCoordinate += self.speed
            self.movingRight = True

    # goes to the left with the left button
    def characterLeft(self):
        if self.xCoordinate > 0:
            self.xCoordinate -= self.speed
            self.movingLeft = True

    # goes down with the down button
    def characterDown(self):
        if self.yCoordinate < self.windowLength - self.size:
            self.yCoordinate += self.speed

    # draws the character
    def characterDraw(self):
        self.window.blit(self.scaledCharacter, (self.xCoordinate, self.yCoordinate))

    def singleCollisionDetection(self, rectangle, platform):
        xCoord = rectangle.real_xCoord(self.xCoordinate, self.size)
        yCoord = rectangle.real_yCoord(self.yCoordinate, self.size)
        width = rectangle.real_width(self.size)
        length = rectangle.real_length(self.size)
        if xCoord + width < platform.xCoordinate:
            return False

        if platform.xCoordinate + platform.width < xCoord:
            return False

        if yCoord + length < platform.yCoordinate:
            return False

        if platform.yCoordinate + platform.length < yCoord:
            return False

        else:
            return True

    # returns True if character is hitting one specific platform
    def collisionDetection(self, platform):
        for rectangle in self.rectangleList:
            if self.singleCollisionDetection(rectangle, platform):
                return True
        return False

    # uses collisionDetection function to check if the character is hitting any of the platforms in the list of platform
    # takes in the character and list of platforms
    # returns false if the character is colliding with any of the platforms
    # returns true if the character is colliding with at least one of the platforms
    # also returns which platform the character is standing on
    def collisionDetectionAll(self, listPlatform):
        for platform in listPlatform:
            if self.collisionDetection(platform):
                return True
        return False

    # if the character is inside a platform, the character will come out of the platform.
    def stationaryCollision(self, platform):
        colliding = False
        if self.collisionDetection(platform):
            colliding = True
        if self.movingLeft and colliding:
            self.xCoordinate += self.speed
        if self.movingRight and colliding:
            self.xCoordinate -= self.speed
        if self.verticalSpeed < 0 and colliding:
            self.yCoordinate += self.verticalSpeed
        if self.verticalSpeed > 0 and colliding:
            self.yCoordinate -= self.verticalSpeed
        if self.verticalSpeed == 0 and colliding:
            self.yCoordinate -= self.verticalSpeed

    # checks for all platforms in platformList
    def stationaryCollisionAll(self):
        for platform in self.platformList:
            self.stationaryCollision(platform)

    # character moves with platform if platform is going horizontal
    def horizontalPlatformMove(self, platform):
        if platform.movingRight:
            self.xCoordinate += platform.horizontalMovement
        if not platform.movingRight:
            self.xCoordinate -= platform.horizontalMovement

    # character moves with platform if platform is going vertical
    def verticalPlatformMove(self, platform):
        if platform.movingUp:
            self.yCoordinate -= platform.verticalMovement

    # sees if the previous gravity was high to check if the character was falling
    # sees if the platform is moving up
    # pushes the character back up
    def vertical_platform_collision(self, platform, gravity):
        if self.collisionDetection(platform):
            if gravity != 0:
                if platform.movingUp:
                    self.yCoordinate += gravity

    # calls different power ups depending on which power up type it sees
    def powerUpCollision(self):
        for powerUp in self.powerUpList:
            if self.collisionDetection(powerUp):
                powerUp.start = time.time()
                self.activePowerUpList.append(powerUp)
                if powerUp.type == "sizeUp":
                    powerUp.sizeUp()
                if powerUp.type == "sizeDown":
                    powerUp.sizeDown()
                if powerUp.type == "speedUp":
                    powerUp.speedUp()
                if powerUp.type == "speedDown":
                    powerUp.speedDown()
                if powerUp.type == "jump":
                    powerUp.jumpHigher()
                if powerUp.type == "heartAdd":
                    if self.lives == 5:
                        pass
                    else:
                        powerUp.moreHeart()
                if powerUp.type == "heartRemove":
                    if self.lives == 1:
                        pass
                    else:
                        powerUp.lessHeart()

                self.powerUpList.remove(powerUp)
    # appends the rectangles of jenny to the list of the character's rectangles (jenny is blond)

    def jennyRectangles(self):
        self.rectangleList.append(character_rectangles(1/6, 0, 2/3, 1/6))
        self.rectangleList.append(character_rectangles(0, 1/6, 1, 1/3))
        self.rectangleList.append(character_rectangles(1/6, 0.5, 2/3, .25))
        self.rectangleList.append(character_rectangles(3/8, .75, 1/4, .25))
        self.bottomRect = character_rectangles(3/8, .75, 1/4, .25)

    # appends the rectangles of ella to the list of the character's rectangles (ella has purple hair)
    def ellaRectangles(self):
        self.rectangleList.append(character_rectangles(0, 1/8, 1, 3/8))
        self.rectangleList.append(character_rectangles(1/8, 3/4, 3/4, 1/4))
        self.rectangleList.append(character_rectangles(1/4, 1/16, 1/2, 7/8))
        self.bottomRect = character_rectangles(1/8, 3/4, 3/4, 1/4)

class character_rectangles:
    def __init__(self, rectangleX, rectangleY, width, length):
        self.rectangleX = rectangleX
        self.rectangleY = rectangleY
        self.width = width
        self.length = length

    # top left coordinate
    def real_xCoord(self, charXCoord, charSize):
        return charXCoord + charSize * self.rectangleX

    def real_yCoord(self, charYCoord, charSize):
        return charYCoord + charSize * self.rectangleY

    def real_width(self, charSize):
        return charSize * self.width

    def real_length(self, charSize):
        return charSize * self.length