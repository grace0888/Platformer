import pygame

# right and up are boolean for which way triangle is pointing
# xcoord and ycoord are for coordinates of pointiest point
class spikes:
    def __init__(self, orientation, height, width, xcoord, ycoord, window, connectedPlatform):
        self.orientation = orientation
        self.height = height
        self.width = width
        self.xcoord = xcoord
        self.ycoord = ycoord # top point??
        self.coord_list = []
        self.window = window
        self.triangle_lines = [] # is a list of points on a triangle's line
        self.connectedPlatform = connectedPlatform

    def platformConnect(self):
        # moving horizontally
        if self.connectedPlatform.horizontalMovement != 0:
            if self.connectedPlatform.movingRight:
                self.xcoord += self.connectedPlatform.horizontalMovement
            elif not self.connectedPlatform.movingRight:
                self.xcoord -= self.connectedPlatform.horizontalMovement
        # moving vertically
        if self.connectedPlatform.verticalMovement != 0:
            if self.connectedPlatform.movingUp:
                self.ycoord -= self.connectedPlatform.verticalMovement
            elif not self.connectedPlatform.movingUp:
                self.ycoord += self.connectedPlatform.verticalMovement

    def spikeDraw(self):
        self.platformConnect()
        self.spikeMath()
        pygame.draw.polygon(
            self.window, (240, 53, 102), self.coord_list, 0)

    # gives us the coord_list
    def spikeMath(self):
        self.coord_list.clear()
        if self.orientation == "right":
            self.coord_list.append((self.xcoord, self.ycoord))
            self.coord_list.append((self.xcoord - self.height, self.ycoord + self.width // 2))
            self.coord_list.append((self.xcoord - self.height, self.ycoord - self.width // 2))
        elif self.orientation == "left":
            self.coord_list.append((self.xcoord, self.ycoord))
            self.coord_list.append((self.xcoord + self.height, self.ycoord + self.width // 2))
            self.coord_list.append((self.xcoord + self.height, self.ycoord - self.width // 2))
        elif self.orientation == "up":
            self.coord_list.append((self.xcoord, self.ycoord))
            self.coord_list.append((self.xcoord + self.width // 2, self.ycoord + self.height))
            self.coord_list.append((self.xcoord - self.width // 2, self.ycoord + self.height))
        elif self.orientation == "down":
            self.coord_list.append((self.xcoord, self.ycoord))
            self.coord_list.append((self.xcoord + self.width // 2, self.ycoord - self.height))
            self.coord_list.append((self.xcoord - self.width // 2, self.ycoord - self.height))

# finds slope of 2 points and finds all the points in between those two points
    def slope(self, x1coord, y1coord, x2coord, y2coord):
        if x1coord != x2coord:
            slope = (y2coord - y1coord) / (x2coord - x1coord)
        # start from coordinate on left, if coordinates are vertical, start with coordinate on top
        if x1coord > x2coord:
            temp = x1coord
            x1coord = x2coord
            x2coord = temp
            temp = y1coord
            y1coord = y2coord
            y2coord = temp
        elif x1coord == x2coord:
            if y1coord > y2coord:
                temp = y1coord
                y1coord = y2coord
                y2coord = temp

        if x1coord != x2coord:
            for i in range(x2coord - x1coord):
                self.triangle_lines.append((x1coord + i, y1coord + (i*slope)))

        elif x1coord == x2coord:
            for i in range(y2coord - y1coord):
                self.triangle_lines.append((x1coord, y1coord + i))

    # checks if one specific point is inside one specific rectangle
    # if it is, returns True, if it is not, returns False
    def single_point_collision_detection(self, xcoord, ycoord, character, rectangle):
        rectX = rectangle.real_xCoord(character.xCoordinate, character.size)
        rectY = rectangle.real_yCoord(character.yCoordinate, character.size)
        rectWidth = rectangle.real_width(character.size)
        rectLength = rectangle.real_length(character.size)
        if xcoord > rectX and xcoord < rectX + rectWidth:
            if ycoord > rectY and ycoord < rectY + rectLength:
                return True
            else:
                return False
        else:
            return False

    def point_list_collision_detection(self, rectangle, character):
        for point in self.triangle_lines:
            if self.single_point_collision_detection(point[0], point[1], character, rectangle):
                xCoordinate = rectangle.real_xCoord(character.xCoordinate, character.size)
                yCoordinate = rectangle.real_yCoord(character.yCoordinate, character.size)
                size = rectangle.real_length(character.size)
                return True
        return False

    def point_collision_detection_all(self, character, rectangle_list):
        for rectangle in rectangle_list:
            if self.point_list_collision_detection(rectangle, character):
                return True
        return False

    def slope_calling(self):
        self.spikeMath()
        self.triangle_lines.clear()
        for i in range(0, 2):
            self.slope(self.coord_list[i][0], self.coord_list[i][1], self.coord_list[(i+1)%3][0], self.coord_list[(i+1)%3][1])