import pygame
import random

height = 600
width = 600
window = pygame.display.set_mode((width, height))
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pygame.display.set_caption("Tiles")
fps = 10
run = True
clock = pygame.time.Clock()
pygame.init()

numbers = [pygame.transform.scale(pygame.image.load("D:/Programs/imgs/one.png"), (50, 50)), 
pygame.transform.scale(pygame.image.load("D:/Programs/imgs/two.png"), (50, 50)), 
pygame.transform.scale(pygame.image.load("D:/Programs/imgs/three.png"), (50, 50)), 
pygame.transform.scale(pygame.image.load("D:/Programs/imgs/four.png"), (50, 50)), 
pygame.transform.scale(pygame.image.load("D:/Programs/imgs/five.png"), (50, 50)), 
pygame.transform.scale(pygame.image.load("D:/Programs/imgs/six.png"), (50, 50)), 
pygame.transform.scale(pygame.image.load("D:/Programs/imgs/seven.png"), (50, 50)), 
pygame.transform.scale(pygame.image.load("D:/Programs/imgs/eight.png"), (50, 50))]

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = white
        self.img = random.choice(numbers)
        numbers.pop(numbers.index(self.img))

    def draw(self):
        pygame.draw.rect(window, self.color, [self.x, self.y, 200, 200])
        pygame.draw.line(window, black, (self.x, self.y), (self.x+200, self.y))
        pygame.draw.line(window, black, (self.x, self.y), (self.x, self.y+200))
        pygame.draw.line(window, black, (self.x, self.y+200), (self.x+200, self.y+200))
        pygame.draw.line(window, black, (self.x+200, self.y), (self.x+200, self.y+200))
        window.blit(self.img, (self.x, self.y))

    def isClicked(self, x, y):
        if self.x < x < self.x + 200 and self.y < y < self.y + 200:
            return True

        return False

    def moveToEmptyPos(self, occupiedPos):

        if (self.x + 200, self.y) not in occupiedPos and (self.x + 200) <= 400: 
            occupiedPos.remove((self.x, self.y))
            self.x = self.x + 200
            occupiedPos.append((self.x, self.y))

        elif (self.x - 200, self.y) not in occupiedPos and (self.x - 200) >= 0: 
            occupiedPos.remove((self.x, self.y))
            self.x = self.x - 200
            occupiedPos.append((self.x, self.y))

        elif (self.x, self.y + 200) not in occupiedPos and (self.y + 200) <= 400: 
            occupiedPos.remove((self.x, self.y))
            self.y = self.y + 200
            occupiedPos.append((self.x, self.y))

        elif (self.x, self.y - 200) not in occupiedPos and (self.y - 200) >= 0: 
            occupiedPos.remove((self.x, self.y))
            self.y = self.y - 200
            occupiedPos.append((self.x, self.y))


tiles = []
occupied = []

for _ in range(8):
    while True:

        x = random.randrange(0, 600, 200)
        y = random.randrange(0, 600, 200)

        if (x, y) not in occupied:
            tiles.append(Tile(x, y))
            occupied.append((x, y))
            break

while run:
    window.fill(black)
    for tile in tiles:
        tile.draw()

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            posX, posY = pygame.mouse.get_pos()
            for tile in tiles:
                if tile.isClicked(posX, posY):
                    tile.moveToEmptyPos(occupied)
    
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()