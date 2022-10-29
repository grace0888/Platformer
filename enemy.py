import pygame
import time

class enemy:
    def __init__(self, xCoordinate, yCoordinate, speed, size, connectedPlatform, window):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.speed = speed
        self.length = size
        self.width = size
        self.size = size
        self.connectedPlatform = connectedPlatform
        self.window = window
        self.movingRight = False
        self.attacking = False

    def enemyDraw(self):
        self.platformConnect()
        pygame.draw.rect(
            self.window, (97, 2, 30),
            pygame.Rect(self.xCoordinate, self.yCoordinate, self.size,
                        self.size))

        # call gravity in the main loop after doing all the functions and stuff
    def enemyMove(self):
        if self.xCoordinate <= self.connectedPlatform.xCoordinate:
            self.movingRight = True
        if self.xCoordinate + self.size > self.connectedPlatform.xCoordinate + self.connectedPlatform.width:
            self.movingRight = False
        if self.movingRight:
            self.xCoordinate += self.speed
        if not self.movingRight:
            self.xCoordinate -= self.speed

    def platformConnect(self):
        # moving vertically
        if self.connectedPlatform.verticalMovement != 0:
            if self.connectedPlatform.movingUp:
                self.yCoordinate -= self.connectedPlatform.verticalMovement
            elif not self.connectedPlatform.movingUp:
                self.yCoordinate += self.connectedPlatform.verticalMovement

    # changes picture when attacks to attack picture
    # next class: attack of the enemy as well as attack of the character
