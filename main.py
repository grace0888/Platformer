import pygame
import time
import random

# hello
from character_class import *
from platform_class import *
from power_up_class import *
from spikes import *
from enemy import *

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
spikeList = []
enemyList = []
characterChosen = ""
imageName = ""
level = 0
teleport_coordx = 400
teleport_coordy = 330
mouse_position = (0,0)
mouseX = mouse_position[0]
mouseY = mouse_position[1]
powerUpType = ["sizeUp", "sizeDown", "speedUp", "speedDown", "jump", "heartAdd", "heartRemove"]

# middle of the top of the box is the coordinates
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
        # all the character is on top of the platform
        if platform.xCoordinate <= xCoord <= platform.xCoordinate + platform.width and platform.xCoordinate <= xCoord + width <= platform.xCoordinate + platform.width:
            onPlatform = True

        # the right side of the character is on top of the platform
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
    global mainCharacter
    mainCharacter.lives = 3
    platformList.clear()
    spikeList.clear()
    powerUpList.clear()
    enemyList.clear()
    platformBox1 = platformBox(5, 500, 125, 20, 0, 0, 0, 0, window)
    platformList.append(platformBox1)
    platformBox2 = platformBox(200, 450, 125, 20, 0, 5, 0, 100, window)
    platformList.append(platformBox2)
    platformBox3 = platformBox(350, 400, 125, 20, 5, 0, 100, 0, window)
    platformList.append(platformBox3)
    powerUp1 = power_ups("sizeUp", 110, 450, mainCharacter, window) #random.choice(powerUpType)
    powerUpList.append(powerUp1)
    enemy1 = enemy(350, 350, 1.5, 50, platformBox3, window)
    enemyList.append(enemy1)
    enemy2 = enemy(200, 400, 1.5, 50, platformBox2, window)
    enemyList.append(enemy2)

    mainCharacter.xCoordinate = 5
    mainCharacter.yCoordinate = 250
    mainCharacter.originalX = 5
    mainCharacter.originalY = 250

def level_two():
    powerUpList.clear()
    spikeList.clear()
    platformList.clear()
    enemyList.clear()
    platform_L2_1 = platformBox(350, 300, 100, 20, 5, 0, 100, 0, window)
    platformList.append(platform_L2_1)
    platform_L2_2 = platformBox(300, 250, 20, 100, 0, 0, 0, 0, window)
    platformList.append(platform_L2_2)
    platform_L2_3 = platformBox(250, 200, 20, 100, 0, 0, 0, 0, window)
    platformList.append(platform_L2_3)
    platform_L2_4 = platformBox(200, 100, 20, 100, 0, 5, 0, 50, window)
    platformList.append(platform_L2_4)

    global mainCharacter
    mainCharacter.xCoordinate = 350
    mainCharacter.yCoordinate = 145
    mainCharacter.originalX = 350
    mainCharacter.originalY = 145

    global teleport_coordx
    teleport_coordx = 160
    global teleport_coordy
    teleport_coordy = 35

def level_three():
    platformList.clear()
    powerUpList.clear()
    spikeList.clear()
    enemyList.clear()
    platform_L3_1 = platformBox(10, 125, 100, 20, 3, 0, 30, 0, window)
    platformList.append(platform_L3_1)
    platform_L3_2 = platformBox(300, 0, 30, 300, 0, 0, 0, 0, window)
    platformList.append(platform_L3_2)
    platform_L3_3 = platformBox(175, 500, 100, 20, 5, 0, 100, 0, window)
    platformList.append(platform_L3_3)
    platform_L3_4 = platformBox(425, 450, 20, 100, 0, 0, 0, 0, window)
    platformList.append(platform_L3_4)

    spike1 = spikes("up", 25, 10, 180, 475, window, platform_L3_3)
    spikeList.append(spike1)

    global mainCharacter
    mainCharacter.xCoordinate = 10
    mainCharacter.yCoordinate = -30
    mainCharacter.originalX = 10
    mainCharacter.originalY = -30

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

def undo_power_up_not_time():
    for powerUp in activePowerUpList:
        if powerUp.type == "sizeUp" or powerUp.type == "sizeDown":
            powerUp.undo_size()
        if powerUp.type == "speedUp" or powerUp.type == "speedDown":
            powerUp.undo_speed()
        if powerUp.type == "jump":
            powerUp.undo_jump()

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

# like Mario where if the character steps on enemy's head, enemy is removed from enemyList
def enemyDeath(character):
    for enemyObject in enemyList:
        if onPlatform(character, character.bottomRect, enemyObject):
            enemyList.remove(enemyObject)

# checks if the character is on / off the screen
# returns true if character is dead, returns false if character is alive
def dead(character):
    if character.yCoordinate > windowLength:
        character.lives -= 1
        return True
    for spike in spikeList:
        spike.slope_calling()
        if spike.point_collision_detection_all(character, character.rectangleList):
            character.lives -= 1
            return True
    for enemyObject in enemyList:
        if collisionDetection(character, enemyObject):
            if enemyObject.attacking == False:
                enemyObject.start = time.time()
                enemyObject.attacking = True
            else:
                if time.time() - enemyObject.start >= 1.5:
                    character.lives -= 1
                    enemyObject.attacking = False
                    return True
        else:
            enemyObject.attacking = False
        # kills character if character touches enemy more than 3 seconds
    return False

def respawn(character):
    if dead(character):
        if mainCharacter.lives != 0:
            character.xCoordinate = character.originalX
            character.yCoordinate = character.originalY

        if mainCharacter.lives == 0:
            activePowerUpList.clear()
            undo_power_up_not_time()
            global teleport_coordx
            teleport_coordx = 400
            global teleport_coordy
            teleport_coordy = 330

# draws the heart
def creating_heart(xCoord, yCoord):
    window.blit(heart_transformed, (xCoord, yCoord))

def hearts():
    if mainCharacter.lives == 5:
        creating_heart(10, 10)
        creating_heart(60, 10)
        creating_heart(110, 10)
        creating_heart(160, 10)
        creating_heart(210, 10)
    if mainCharacter.lives == 4:
        creating_heart(10, 10)
        creating_heart(60, 10)
        creating_heart(110, 10)
        creating_heart(160, 10)
    if mainCharacter.lives == 3:
        creating_heart(10, 10)
        creating_heart(60, 10)
        creating_heart(110, 10)
    if mainCharacter.lives == 2:
        creating_heart(10, 10)
        creating_heart(60, 10)
    if mainCharacter.lives == 1:
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
    global mouseX
    global mouseY
    window.fill((255, 173, 222))
    window.blit(start_transformed, (0, 0))
    pygame.display.flip()
    # jenny
    if mouseX >= 20 and mouseX <= 250 and mouseY >= 20 and mouseY <= 270:
        characterChosen = "jenny"
        imageName = "game character fixed.png"
        mouseX = 0
        mouseY = 0
    # ella
    if mouseX >= 300 and mouseX <= 570 and mouseY >= 20 and mouseY <= 270:
        characterChosen = "ella"
        imageName = "game character 2.png"
        mouseX = 0
        mouseY = 0
def draw():
    global mouseX
    global mouseY
    global gameStart
    if mainCharacter.lives <= 0:
        window.fill((255, 173, 222))
        window.blit(death_transformed, (0, 0))
        pygame.display.flip()
        if mouseX >= 75 and mouseX <= 225 and mouseY >= 200 and mouseY <= 275:
            pygame.quit()
            gameStart = False
        if mouseX >= 375 and mouseX <= 525 and mouseY >= 200 and mouseY <= 275:
            level_one()
            mouseX = 0
            mouseY = 0
    else:
        window.fill((228, 245, 239))
        teleport_creation(teleport_coordx, teleport_coordy)
        hearts()
        mainCharacter.characterDraw()
        for platform in platformList:
            platform.platformDraw()
        for powerUp in powerUpList:
            powerUp.draw()
        for spike in spikeList:
            spike.spikeDraw()
        for enemyObject in enemyList:
            enemyObject.enemyDraw()
        pygame.display.flip()


# Calling functions
# platformBox(xCoordinate, yCoordinate, width, length,
# horizontalMovement, verticalMovement, hLength, vLength
gameStart = True
image_creation()
while characterChosen == "":
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            characterChosen = "ella"
            imageName = "game character 2.png"
            gameStart = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            mouseX = mouse_position[0]
            mouseY = mouse_position[1]
    preDraw()
mainCharacter = characterBox(imageName, 5, 5, 300, characterSize, characterChosen, window, windowWidth, windowLength, platformList, activePowerUpList, powerUpList)
level_one()
pygame.display.flip()

clock = pygame.time.Clock()

# Game while loop
while gameStart:
    clock.tick(fps)
    # draw everything here!
    draw()
    # this checks if we level up
    leveling_up()

    enemyDeath(mainCharacter)
    respawn(mainCharacter)

    mainCharacter.movingRight = False
    mainCharacter.movingLeft = False
    events = pygame.event.get()

    mainCharacter.yCoordinate -= mainCharacter.verticalSpeed
    # oldGravity is the gravity from the previous frame to see if the character was falling
    oldGravity = mainCharacter.verticalSpeed
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
    for enemyObject in enemyList:
        enemyObject.enemyMove()
    moveWithPlatform(mainCharacter, platformList)
    mainCharacter.stationaryCollisionAll()
    mainCharacter.powerUpCollision()
    for platform in platformList:
        mainCharacter.vertical_platform_collision(platform, oldGravity)
    # undoing power up
    undo_power_ups()
pygame.quit()