import pygame
class platformBox:
    def __init__(self, xCoordinate, yCoordinate, width, length,
                 horizontalMovement, verticalMovement, hLength, vLength, window):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.length = length
        self.width = width
        self.horizontalMovement = horizontalMovement
        self.verticalMovement = verticalMovement
        self.startingHCoordinate = xCoordinate
        self.endingHCoordinate = xCoordinate + hLength
        self.startingVCoordinate = yCoordinate + vLength
        self.endingVCoordinate = yCoordinate
        self.movingRight = True
        self.movingUp = True
        self.window = window

    # moves the platform horizontally
    def platformHorizontalMove(self):
        if self.xCoordinate >= self.endingHCoordinate:
            self.movingRight = False
        if self.xCoordinate <= self.startingHCoordinate:
            self.movingRight = True
        if self.movingRight:
            self.xCoordinate += self.horizontalMovement
        if not self.movingRight:
            self.xCoordinate -= self.horizontalMovement

    # moves the vertical platform horizontally
    def platformVerticalMove(self):
        if self.yCoordinate <= self.endingVCoordinate:
            self.movingUp = False
        if self.yCoordinate >= self.startingVCoordinate:
            self.movingUp = True
        if self.movingUp:
            self.yCoordinate -= self.verticalMovement
        if not self.movingUp:
            self.yCoordinate += self.verticalMovement

    # draws the platform
    def platformDraw(self):
        pygame.draw.rect(
            self.window, (99, 99, 99),
            pygame.Rect(self.xCoordinate, self.yCoordinate, self.width,
                        self.length))
