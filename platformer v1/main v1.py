import pygame
import time
import random

pygame.init()
pygame.display.set_caption("Platformer")
windowWidth = 600
windowLength = 600
window = pygame.display.set_mode([windowWidth, windowLength])
window.fill((228, 245, 239))
characterSize = 100
fps = 15
platformList = []
powerUpList = []
activePowerUpList = []
characterChosen = ""
imageName = ""
level = 0
lives = 3
teleport_coordx = 400
teleport_coordy = 330
mouse_position = (0,0)
mouseX = mouse_position[0]
mouseY = mouse_position[1]
powerUpType = ["sizeUp", "sizeDown", "speedUp", "speedDown", "jump", "heartAdd", "heartRemove"]

# middle of the top of the box is the coordinates
# Classes and functions
class platformBox:
    def __init__(self, xCoordinate, yCoordinate, width, length,
                 horizontalMovement, verticalMovement, hLength, vLength):
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
            window, (99, 99, 99),
            pygame.Rect(self.xCoordinate, self.yCoordinate, self.width,
                        self.length))

class characterBox:
    def __init__(self, image, speed, xCoordinate, yCoordinate, size):
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

    # goes up with the up button
    def characterUp(self):
        if self.yCoordinate > 0:
            self.verticalSpeed = self.limitSpeed
            # self.yCoordinate -= 10 * self.speed

    # goes to the right with the right button
    def characterRight(self):
        if self.xCoordinate < windowWidth - characterSize:
            self.xCoordinate += self.speed
            self.movingRight = True

    # goes to the left with the left button
    def characterLeft(self):
        if self.xCoordinate > 0:
            self.xCoordinate -= self.speed
            self.movingLeft = True

    # goes down with the down button
    def characterDown(self):
        if self.yCoordinate < windowLength - characterSize:
            self.yCoordinate += self.speed

    # draws the character
    def characterDraw(self):
        window.blit(self.scaledCharacter, (self.xCoordinate, self.yCoordinate))

    # if the character is inside a platform, the character will come out of the platform.
    def stationaryCollision(self, platform):
        colliding = False
        if collisionDetection(self, platform):
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
        for platform in platformList:
            self.stationaryCollision(platform)

    # if platform is colliding with character when it's horizontally moving, moves character same amount as platform
    def movingCollisionHorizontal(self, platform):
        colliding = False
        if collisionDetection(self, platform):
            colliding = True
        if platform.horizontalMovement != 0 and colliding:
            if platform.movingRight:
                self.xCoordinate += platform.horizontalMovement
            if not platform.movingRight:
                self.xCoordinate -= platform.horizontalMovement

    # if platform is colliding with character when it's horizontally moving, moves character same amount as platform
    def movingCollisionVertical(self, platform):
        colliding = False
        if collisionDetection(self, platform):
            colliding = True
        if platform.verticalMovement != 0 and colliding:
            if platform.movingUp:
                self.yCoordinate -= platform.verticalMovement
            if not platform.movingUp:
                self.yCoordinate += platform.verticalMovement
    # applies previous 2 functions for all platforms
    def movingCollisionAll(self):
        for platform in platformList:
            self.movingCollisionHorizontal(platform)
            self.movingCollisionVertical(platform)

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
        if not platform.movingUp:
            self.yCoordinate += platform.verticalMovement

    # calls different power ups depending on which power up type it sees
    def powerUpCollision(self):
        global powerUpList
        for powerUp in powerUpList:
            if collisionDetection(mainCharacter, powerUp):
                powerUp.start = time.time()
                activePowerUpList.append(powerUp)
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
                    if lives == 5:
                        pass
                    else:
                        powerUp.moreHeart()
                if powerUp.type == "heartRemove":
                    if lives == 1:
                        pass
                    else:
                        powerUp.lessHeart()

                powerUpList.remove(powerUp)
    # appends the rectangles of jenny to the list of the character's rectangles
    def jennyRectangles(self):
        self.rectangleList.append(character_rectangles(1/6, 0, 2/3, 1/6))
        self.rectangleList.append(character_rectangles(0, 1/6, 1, 1/3))
        self.rectangleList.append(character_rectangles(1/6, 0.5, 2/3, .25))
        self.rectangleList.append(character_rectangles(3/8, .75, 1/4, .25))

    # appends the rectangles of ella to the list of the character's rectangles
    def ellaRectangles(self):
        self.rectangleList.append(character_rectangles(0, 1/8, 1, 3/8))
        self.rectangleList.append(character_rectangles(1/8, 3/4, 3/4, 1/4))
        self.rectangleList.append(character_rectangles(1/4, 1/16, 1/2, 7/8))

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

class power_ups:
    def __init__(self, type, xCoordinate, yCoordinate):
        self.type = type
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.image = "power up 1.png"
        self.power_up = pygame.image.load(self.image)
        self.width = 50
        self.length = 50
        self.scaledPowerUp = pygame.transform.scale(self.power_up, (self.width, self.length))
        self.start = 0

    def undo_speed(self):
        global mainCharacter
        mainCharacter.speed = 5

    def speedUp(self):
        global mainCharacter
        mainCharacter.speed = 10

    def speedDown(self):
        global mainCharacter
        mainCharacter.speed = 3

    def undo_jump(self):
        global mainCharacter
        mainCharacter.limitSpeed = 10

    def jumpHigher(self):
        global mainCharacter
        mainCharacter.limitSpeed = 20

    def undo_size(self):
        global mainCharacter
        mainCharacter.size = 100
        mainCharacter.scaledCharacter = pygame.transform.scale(mainCharacter.Character,
                                                               (mainCharacter.size, mainCharacter.size))
        mainCharacter.limitSpeed = 10

    def sizeUp(self):
        global mainCharacter
        mainCharacter.size = 150
        mainCharacter.scaledCharacter = pygame.transform.scale(mainCharacter.Character, (mainCharacter.size, mainCharacter.size))

    def sizeDown(self):
        global mainCharacter
        mainCharacter.size = 50
        mainCharacter.scaledCharacter = pygame.transform.scale(mainCharacter.Character, (mainCharacter.size, mainCharacter.size))
        mainCharacter.limitSpeed = 13

    def moreHeart(self):
        global lives
        lives += 1

    def lessHeart(self):
        global lives
        lives -= 1

    def draw(self):
        window.blit(self.scaledPowerUp, (self.xCoordinate, self.yCoordinate))


# Checks if character and platform are colliding (takes in character and platform)
# returns True if the character and platform are colliding
# returns false if the character and platform are not colliding
def singleCollisionDetection(character, rectangle, platform):
    xCoord = rectangle.real_xCoord(character.xCoordinate, character.size)
    yCoord = rectangle.real_yCoord(character.yCoordinate, character.size)
    width = rectangle.real_width(character.size)
    length = rectangle.real_length(character.size)
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
def collisionDetection(character, platform):
    for rectangle in character.rectangleList:
        if singleCollisionDetection(character, rectangle, platform):
            return True
    return False

# uses collisionDetection function to check if the character is hitting any of the platforms in the list of platform
# takes in the character and list of platforms
# returns false if the character is colliding with any of the platforms
# returns true if the character is colliding with at least one of the platforms
# also returns which platform the character is standing on
def collisionDetectionAll(character, listPlatform):
    for platform in listPlatform:
        if collisionDetection(character, platform):
            return True
    return False

# Checks if one of the character's rectangles is on one specific platform
def onPlatform(character, rectangle, platform):
    xCoord = rectangle.real_xCoord(character.xCoordinate, character.size)
    yCoord = rectangle.real_yCoord(character.yCoordinate, character.size)
    width = rectangle.real_width(character.size)
    length = rectangle.real_length(character.size)
    onPlatform = False

    if platform.yCoordinate - 5 <= yCoord + length <= platform.yCoordinate + 5:
        if platform.xCoordinate <= xCoord <= platform.xCoordinate + platform.width and platform.xCoordinate <= xCoord + width <= platform.xCoordinate + platform.width:
            onPlatform = True

        if xCoord < platform.xCoordinate and platform.xCoordinate < xCoord + width < platform.xCoordinate + platform.width:
            onPlatform = True

        if platform.xCoordinate < xCoord < platform.xCoordinate + platform.width and platform.xCoordinate + platform.width < xCoord + width:
            onPlatform = True

        if xCoord <= platform.xCoordinate <= platform.xCoordinate + platform.width and xCoord <= platform.xCoordinate + platform.width <= xCoord + width:
            onPlatform = True

    return onPlatform

# checks if any of the rectangles are on the platform
# returns true if one of the rectangles is on the platform
def onPlatform1_5(character, platform):
    for rectangle in character.rectangleList:
        if onPlatform(character, rectangle, platform):
            return True
    return False

# Returns if the character is on any of the platforms.
# returns true if character is on a platform, returns false if it is not
def onPlatform2(character, listPlatform):
    for platform in listPlatform:
        checking = onPlatform1_5(character, platform)
        if checking:
            return True
    return False


# returns the platform that the character is on
def platformCharacterOn(character, listPlatform):
    onAnyPlatform = onPlatform2(character, platformList)
    if onAnyPlatform:
        for platform in listPlatform:
            checking = onPlatform1_5(character, platform)
            if checking:
                return platform
    else:
        return None

    return False


# makes the character move with a moving platform
def moveWithPlatform(character, platformList):
    platformOn = platformCharacterOn(character, platformList)
    if platformOn == None:
        return
    else:
        if platformOn.horizontalMovement == 0 and platformOn.verticalMovement == 0:
            return
        if platformOn.horizontalMovement != 0:
            character.horizontalPlatformMove(platformOn)
        if platformOn.verticalMovement != 0:
            character.verticalPlatformMove(platformOn)

def level_one():
    global level
    level = 1
    global lives
    lives = 3
    platformList.clear()
    platformBox1 = platformBox(5, 500, 125, 20, 0, 0, 0, 0)
    platformList.append(platformBox1)
    platformBox2 = platformBox(200, 450, 125, 20, 0, 5, 0, 100)
    platformList.append(platformBox2)
    platformBox3 = platformBox(350, 400, 125, 20, 5, 0, 100, 0)
    platformList.append(platformBox3)
    powerUp1 = power_ups(random.choice(powerUpType), 110, 450)
    powerUpList.append(powerUp1)
    global mainCharacter
    mainCharacter.xCoordinate = 5
    mainCharacter.yCoordinate = 300
    mainCharacter.originalX = 5
    mainCharacter.originalY = 300

def level_two():
    platformList.clear()
    platform_L2_1 = platformBox(350, 300, 100, 20, 5, 0, 100, 0)
    platformList.append(platform_L2_1)
    platform_L2_2 = platformBox(300, 250, 20, 100, 0, 0, 0, 0)
    platformList.append(platform_L2_2)
    platform_L2_3 = platformBox(250, 200, 20, 100, 0, 0, 0, 0)
    platformList.append(platform_L2_3)
    platform_L2_4 = platformBox(200, 100, 20, 100, 0, 5, 0, 50)
    platformList.append(platform_L2_4)
    global mainCharacter
    mainCharacter.xCoordinate = 350
    mainCharacter.yCoordinate = 200
    mainCharacter.originalX = 350
    mainCharacter.originalY = 200

    global teleport_coordx
    teleport_coordx = 160
    global teleport_coordy
    teleport_coordy = 35

def level_three():
    platformList.clear()
    platform_L3_1 = platformBox(10, 125, 100, 20, 3, 0, 30, 0)
    platformList.append(platform_L3_1)
    platform_L3_2 = platformBox(250, 0, 30, 300, 0, 0, 0, 0)
    platformList.append(platform_L3_2)
    platform_L3_3 = platformBox(175, 500, 100, 20, 5, 0, 100, 0)
    platformList.append(platform_L3_3)
    platform_L3_4 = platformBox(425, 450, 20, 100, 0, 0, 0, 0)
    platformList.append(platform_L3_4)

    global mainCharacter
    mainCharacter.xCoordinate = 10
    mainCharacter.yCoordinate = 25
    mainCharacter.originalX = 10
    mainCharacter.originalY = 25

    global teleport_coordx
    teleport_coordx = 380
    global teleport_coordy
    teleport_coordy = 400

def leveling_up():
    global level
    if level == 1:
        if mainCharacter.xCoordinate >= 400 and mainCharacter.xCoordinate <= 500:
            if mainCharacter.yCoordinate >= 200 and mainCharacter.yCoordinate <= 350:
                level = 2
                level_two()
    if level == 2:
        if mainCharacter.xCoordinate <= 300 and mainCharacter.xCoordinate >= 200:
            if mainCharacter.yCoordinate <= 50 and mainCharacter.yCoordinate >= 0:
                level = 3
                level_three()

def undo_power_ups():
    for powerUp in activePowerUpList:
        if time.time() - powerUp.start >= 60:
            if powerUp.type == "sizeUp" or powerUp.type == "sizeDown":
                powerUp.undo_size()
            if powerUp.type == "speedUp" or powerUp.type == "speedDown":
                powerUp.undo_speed()
            if powerUp.type == "jump":
                powerUp.undo_jump()

def gravity(character, listPlatform):
    checking = onPlatform2(character, listPlatform)
    if checking:
        character.verticalSpeed = 0
    elif not checking:
        character.verticalSpeed -= 1
        if character.verticalSpeed <= character.limitSpeed * -1:
            character.verticalSpeed = -1 * character.limitSpeed

# checks if the character is on / off the screen
# returns true if character is dead, returns false if character is alive
def dead(character):
    if character.yCoordinate > windowLength:
        global lives
        lives -= 1
        return True
    else:
        return False

def respawn(character):
    if dead(character):
        if lives != 0:
            character.xCoordinate = character.originalX
            character.yCoordinate = character.originalY

        if lives == 0:
            global teleport_coordx
            teleport_coordx = 400
            global teleport_coordy
            teleport_coordy = 330

# draws the heart
def creating_heart(xCoord, yCoord):
    window.blit(heart_transformed, (xCoord, yCoord))

def hearts():
    global lives
    if lives == 5:
        creating_heart(10, 10)
        creating_heart(60, 10)
        creating_heart(110, 10)
        creating_heart(160, 10)
        creating_heart(210, 10)
    if lives == 4:
        creating_heart(10, 10)
        creating_heart(60, 10)
        creating_heart(110, 10)
        creating_heart(160, 10)
    if lives == 3:
        creating_heart(10, 10)
        creating_heart(60, 10)
        creating_heart(110, 10)
    if lives == 2:
        creating_heart(10, 10)
        creating_heart(60, 10)
    if lives == 1:
        creating_heart(10, 10)

def teleport_creation(xCoord, yCoord):
    window.blit(teleport_transformed, (xCoord, yCoord))

def image_creation():
    global heart_transformed
    heart_image = pygame.image.load("heart.png")
    heart_transformed = pygame.transform.scale(heart_image, (50, 50))

    global teleport_transformed
    teleport_image = pygame.image.load("teleport thing.png")
    teleport_transformed = pygame.transform.scale(teleport_image, (100, 100))

    global death_transformed
    death_image = pygame.image.load("death screen.png")
    death_transformed = pygame.transform.scale(death_image, (windowWidth, windowLength))

    global start_transformed
    start_image = pygame.image.load("start screen.png")
    start_transformed = pygame.transform.scale(start_image, (windowWidth, windowLength))

# choosing character and stuff
def preDraw():
    global characterChosen
    global imageName
    window.fill((255, 173, 222))
    window.blit(start_transformed, (0, 0))
    pygame.display.flip()
    # jenny
    if mouseX >= 20 and mouseX <= 250 and mouseY >= 20 and mouseY <= 270:
        characterChosen = "jenny"
        imageName = "game character fixed.png"
    # ella
    if mouseX >= 300 and mouseX <= 570 and mouseY >= 20 and mouseY <= 270:
        characterChosen = "ella"
        imageName = "game character 2.png"
def draw():
    if lives <= 0:
        window.fill((255, 173, 222))
        window.blit(death_transformed, (0, 0))
        pygame.display.flip()
        if mouseX >= 75 and mouseX <= 225 and mouseY >= 200 and mouseY <= 275:
            pygame.quit()
        if mouseX >= 375 and mouseX <= 525 and mouseY >= 200 and mouseY <= 275:
            level_one()
    else:
        window.fill((228, 245, 239))
        teleport_creation(teleport_coordx, teleport_coordy)
        hearts()
        mainCharacter.characterDraw()
        for platform in platformList:
            platform.platformDraw()
        for powerUp in powerUpList:
            powerUp.draw()
        pygame.display.flip()


# Calling functions
# platformBox(xCoordinate, yCoordinate, width, length,
# horizontalMovement, verticalMovement, hLength, vLength
image_creation()
while characterChosen == "":
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            gameStart = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            mouseX = mouse_position[0]
            mouseY = mouse_position[1]
    preDraw()
mainCharacter = characterBox(imageName, 5, 5, 300, characterSize, characterChosen)
level_one()
pygame.display.flip()
gameStart = True

clock = pygame.time.Clock()

# Game while loop
while gameStart:
    clock.tick(fps)
    # draw everything here!
    draw()
    # this checks if we level up
    leveling_up()
    # this checks if we should respawn and then respawns if we do
    respawn(mainCharacter)

    mainCharacter.movingRight = False
    mainCharacter.movingLeft = False
    events = pygame.event.get()

    mainCharacter.yCoordinate -= mainCharacter.verticalSpeed
    gravity(mainCharacter, platformList)

    # keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if onPlatform2(mainCharacter, platformList):
            mainCharacter.characterUp()
    if keys[pygame.K_RIGHT]:
        mainCharacter.characterRight()
    if keys[pygame.K_LEFT]:
        mainCharacter.characterLeft()

    # mouse clicks
    for event in events:
        if event.type == pygame.QUIT:
            gameStart = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            mouseX = mouse_position[0]
            mouseY = mouse_position[1]

    # updating our platforms/characters
    for platform in platformList:
        platform.platformHorizontalMove()
        platform.platformVerticalMove()
    moveWithPlatform(mainCharacter, platformList)
    mainCharacter.stationaryCollisionAll()
    mainCharacter.movingCollisionAll()
    mainCharacter.powerUpCollision()
    # undoing power up
    undo_power_ups()
pygame.quit()