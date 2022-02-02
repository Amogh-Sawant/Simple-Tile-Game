from ast import arg
import pygame
import random
import argparse
from a import *

height = 600
width = 600
window = pygame.display.set_mode((width, height))
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pygame.display.set_caption("Tiles")
fps = 2
run = True
clock = pygame.time.Clock()
pygame.init()

numbers = [
            pygame.transform.scale(pygame.image.load("D:/Programs/imgs/one.png"), (50, 50)), 
            pygame.transform.scale(pygame.image.load("D:/Programs/imgs/two.png"), (50, 50)), 
            pygame.transform.scale(pygame.image.load("D:/Programs/imgs/three.png"), (50, 50)), 
            pygame.transform.scale(pygame.image.load("D:/Programs/imgs/four.png"), (50, 50)), 
            pygame.transform.scale(pygame.image.load("D:/Programs/imgs/five.png"), (50, 50)), 
            pygame.transform.scale(pygame.image.load("D:/Programs/imgs/six.png"), (50, 50)), 
            pygame.transform.scale(pygame.image.load("D:/Programs/imgs/seven.png"), (50, 50)), 
            pygame.transform.scale(pygame.image.load("D:/Programs/imgs/eight.png"), (50, 50))
        ]

class Tile:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.color = white
        self.img = numbers[n-1]

    def draw(self):
        pygame.draw.rect(window, self.color, [self.x, self.y, 200, 200])
        pygame.draw.line(window, black, (self.x, self.y), (self.x+200, self.y))
        pygame.draw.line(window, black, (self.x, self.y), (self.x, self.y+200))
        pygame.draw.line(window, black, (self.x, self.y+200), (self.x+200, self.y+200))
        pygame.draw.line(window, black, (self.x+200, self.y), (self.x+200, self.y+200))
        window.blit(self.img, (self.x, self.y))

    # def animateMove(self, direction):
    #     if direction == "up":
    #         self.snap_to_pos = self.y - 200
    #         while self.y >= self.y-200:
    #             self.y -= 20
    #             self.draw()
    #         self.y = self.snap_to_pos

    #     elif direction == "down":
    #         self.snap_to_pos = self.y + 200
    #         while self.y <= self.y+200:
    #             self.y += 20
    #             self.draw()
    #         self.y = self.snap_to_pos

    #     elif direction == "left":
    #         self.snap_to_pos = self.x - 200
    #         while self.x >= self.x-200:
    #             self.x -= 20
    #             self.draw()
    #         self.x = self.snap_to_pos

    #     elif direction == "right":
    #         self.snap_to_pos = self.x + 200
    #         while self.x <= self.x+200:
    #             self.x += 20
    #             self.draw()
    #         return self.snap_to_pos

    def isClicked(self, x, y):
        if self.x < x < self.x + 200 and self.y < y < self.y + 200:
            return True

        return False

    def moveToEmptyPos(self, occupiedPos, direction):

        if (self.x + 200, self.y) not in occupiedPos and (self.x + 200) <= 400 and direction=="right": # move right
            occupiedPos.remove((self.x, self.y))
            self.x = self.x + 200
            occupiedPos.append((self.x, self.y))
            return True

        elif (self.x - 200, self.y) not in occupiedPos and (self.x - 200) >= 0 and direction=="left": # move left
            occupiedPos.remove((self.x, self.y))
            self.x = self.x - 200
            occupiedPos.append((self.x, self.y))
            return True

        elif (self.x, self.y + 200) not in occupiedPos and (self.y + 200) <= 400 and direction=="down": # move down
            occupiedPos.remove((self.x, self.y))
            self.y = self.y + 200
            occupiedPos.append((self.x, self.y))
            return True

        elif (self.x, self.y - 200) not in occupiedPos and (self.y - 200) >= 0 and direction=="up": # move up
            occupiedPos.remove((self.x, self.y))
            self.y = self.y - 200
            occupiedPos.append((self.x, self.y))
            return True
        
        return False

#--------- Declaring all the variables ---------#
tiles = []
occupied = []
movedirection = ["up", "down", "right", "left"]
x, y = 0, 0
d = 0
given_order = [8, 4, 3, 2, 1, 7, 6, 5, 0]
parser = argparse.ArgumentParser()
parser.add_argument("--startrow",help='Enter the numbers in sequence for starting arangement starting from row 1 to row 3 space separated (put 0 for blank area).',type=int, nargs=9, metavar=('row1col1', 'row1col2', 'row1col3','row2col1','row2col2','row2col3','row3col1','row3col2','row3col3'), required=True)
parser.add_argument("--goalrow",help='Enter the numbers in sequence for goal arangement starting from row 1 to row 3 space sepearted (put 0 for blank area).',type=int, nargs=9, metavar=('row1col1','row1col2','row1col3','row2col1','row2col2','row2col3','row3col1','row3col2','row3col3'), required=True)
args = parser.parse_args()
valid_pattern = [1,2,3,4,5,6,7,8,0]

#----- Assert if Input is correct -----#

assert set(valid_pattern)==set(args.startrow)
assert set(valid_pattern)==set(args.goalrow)
given_order = args.startrow

#----- Reformat Input -----#
print(args.startrow)
startloc = [args.startrow[0:3],args.startrow[3:6],args.startrow[6:]]
goalloc = [args.goalrow[0:3],args.goalrow[3:6],args.goalrow[6:]]

#----- Initalize start and end node -----#

start = Node(startloc,0)
goal = Node(goalloc,0,'goal')

#----- Initilaize Game -----#

game = Game(start, goal)
sol = game.solve() #Solve Game

#-------- Get the order of start state and make Tile Objects with corresponding number --------#

for num in given_order:
    if num != 0:
        tiles.append(Tile(x, y, num))
        occupied.append((x, y))
    x += 200
    if x == 600:
        y += 200
        x = 0

#---------- Game Loop ----------# 

while run:
    window.fill(black)
    for tile in tiles:
        tile.draw()
    if d != len(sol):
        direction = sol[d]
        d += 1
    for tile in tiles:
        if tile.moveToEmptyPos(occupied, direction): break
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            run = False
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()

# python tiles_with_a.py --startrow 0 1 2 3 4 5 6 7 8 --goalrow 1 2 3 4 5 6 7 8 0