import pygame
from math import cos, sin, pi

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

RAY_AMOUNT = 20

wallcolors = {
    '1': RED, 
    '2': GREEN,
    '3': BLUE
}

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.blocksize = 50
        self.wallheight = 50

        self.stepsize = 5

        self.player = {
            'x': 100,
            'y': 100,
            'fov': 60
        }

    def load_map(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append(list(line))

    def drawBlock(self, x, y, id):
        self.screen.fill(wallcolors[id], (x, y, self.blocksize, self.blocksize))

    def drawPlayerIcon(self, color):
        rect = (self.player['x'] - 2, self.player['y'] - 2, 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, angle):
        rads = angle * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['x'] + dist * sin(rads))
        
            self.screen.set_at((x,y), WHITE)
            dist += 1

            if dist >= 100:
                return

    def render(self):
        for x in range(0, self.width, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if self.map[j][i] != ' ':
                    self.drawBlock(x, y, self.map[j][i])

        self.drawPlayerIcon(BLACK)
        
        for column in range(RAY_AMOUNT):
            angle = -(self.player['fov'] / 2) + (self.player['fov'] * column / RAY_AMOUNT)
            self.castRay(angle)
            


width = 500
height = 500

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)

rCaster = Raycaster(screen)
rCaster.load_map("map.txt")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

isRunning = True
while isRunning:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False
        elif ev.type == pygame.KEYDOWN:
            newX = rCaster.player['x']
            newY = rCaster.player['y']

            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            elif ev.key == pygame.K_w:
                newY -= rCaster.stepsize
            elif ev.key == pygame.K_s:
                newY += rCaster.stepsize
            elif ev.key == pygame.K_a:
                newX -= rCaster.stepsize
            elif ev.key == pygame.K_d:
                newX += rCaster.stepsize
            i = int(newX/rCaster.blocksize)
            j = int(newY/rCaster.blocksize)

            if rCaster.map[j][i] == ' ':
                rCaster.player['x'] = newX  
                rCaster.player['y'] = newY
    
    screen.fill(pygame.Color("gray"))
    rCaster.render()

    #FPS
    screen.fill(pygame.Color("black"), (0,0,30,30))
    screen.blit(updateFPS(), (0,0))
    clock.tick(60)

    pygame.display.update()



pygame.quit()