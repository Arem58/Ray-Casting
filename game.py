import pygame
from pygame.locals import *
from menu import *
from math import cos, sin, pi, atan2
from pygame import mixer

RAY_AMOUNT = 100
SPRITE_BACKGROUND = (152, 0, 136, 255)
black = (0, 0, 0)
white = (255, 255, 255)

map1 = "map.txt"
map2 = "map2.txt"
map3 = "map3.txt"

mapLevel = {
    '1': map1, 
    '2': map2,
    '3': map3,
}

wallcolors = {
    '1': pygame.Color('red'), 
    '2': pygame.Color('green'),
    '3': pygame.Color('blue'),
    '4': pygame.Color('yellow'),
    '5': pygame.Color('purple')
}

wallTextures = {
    '1': pygame.image.load('wall1.png'), 
    '2': pygame.image.load('wall2.png'),
    '3': pygame.image.load('wall3.png'),
    '4': pygame.image.load('wall4.png'),
    '5': pygame.image.load('wall5.png'),
    '6': pygame.image.load('textures/BRNBIGC.png')
}

enemies = [
     {"x": 100,
      "y": 200,
      "sprite": pygame.image.load('sprite1.png')},
     {"x": 350,
      "y": 160,
      "sprite": pygame.image.load('cthulhu.png')},
     {"x": 300,
      "y": 330,
      "sprite": pygame.image.load('hitler.png')}
]

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.halfHeight = int(self.height/2)
        self.zbuffer = [float('inf') for z in range(self.width)]
        self.blocksize = 50
        self.wallheight = 50

        self.maxdistance = 300

        self.stepsize = 5
        self.turnSize = 5

        self.victoria = False

        self.player = {
            'x': 100,
            'y': 95,
            'fov': 20,
            'angle': 0,
            'height': 0,
        }

        self.hitEnemy = False

    def load_map(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append(list(line.rstrip()))
        return self.map

    def drawMinimap(self):
        minimapWidth = 100
        minimapHeight = 100


        minimapSurface = pygame.Surface( (500, 500 ) )
        minimapSurface.fill(pygame.Color("gray"))

        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):

                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if j < len(self.map):
                    if i < len(self.map[j]):
                        if self.map[j][i] != ' ':
                            tex = wallTextures[self.map[j][i]]
                            tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize) )
                            rect = tex.get_rect()
                            rect = rect.move((x,y))
                            minimapSurface.blit(tex, rect)

        rect = (int(self.player['x'] - 4), int(self.player['y']) - 4, 10,10)
        minimapSurface.fill(pygame.Color('black'), rect )

        for enemy in enemies:
            rect = (enemy['x'] - 4, enemy['y'] - 4, 10,10)
            minimapSurface.fill(pygame.Color('red'), rect )

        minimapSurface = pygame.transform.scale(minimapSurface, (minimapWidth,minimapHeight) )
        self.screen.blit(minimapSurface, (self.width - minimapWidth,self.height - minimapHeight))

    def drawSprite(self, obj, size):
        # Pitagoras
        spriteDist = ((self.player['x'] - obj['x']) ** 2 + (self.player['y'] - obj['y']) ** 2) ** 0.5

        # Angulo
        spriteAngle = atan2(obj['y'] - self.player['y'], obj['x'] - self.player['x']) * 180 / pi

        #Tamaño del sprite
        aspectRatio = obj['sprite'].get_width() / obj['sprite'].get_height()
        spriteHeight = (self.height / spriteDist) * size
        spriteWidth = spriteHeight * aspectRatio

        # Buscar el punto inicial para dibujar el sprite
        angleDif = (spriteAngle - self.player['angle']) % 360
        angleDif = (angleDif - 360) if angleDif > 180 else angleDif
        startX = angleDif * self.width / self.player['fov'] 
        startX += (self.width /  2) - (spriteWidth  / 2)
        startY = (self.height /  2) - (spriteHeight / 2)
        startX = int(startX)
        startY = int(startY) + self.player['height']

        for x in range(startX, startX + int(spriteWidth)):
            if (0 < x < self.width) and self.zbuffer[x] >= spriteDist:
                for y in range(startY, startY + int(spriteHeight)):
                    tx = int((x - startX) * obj['sprite'].get_width() / spriteWidth )
                    ty = int((y - startY) * obj['sprite'].get_height() / spriteHeight )
                    texColor = obj['sprite'].get_at((tx, ty))
                    if texColor != SPRITE_BACKGROUND and texColor[3] > 128:
                        self.screen.set_at((x,y), texColor)

                        if y == self.height / 2:
                            self.zbuffer[x] = spriteDist
                            if x == self.width / 2:
                                self.hitEnemy = True

    def castRay(self, angle):
        rads = angle * pi / 180
        dist = 0
        stepSize = 1
        stepX = stepSize * cos(rads)
        stepY = stepSize * sin(rads)

        playerPos = (self.player['x'], self.player['y'])

        x = playerPos[0]
        y = playerPos[1]

        while True:
            dist += stepSize

            x += stepX
            y += stepY

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if j < len(self.map):
                if i < len(self.map[j]):
                    if self.map[j][i] != ' ':
                        
                        hitX = x - i * self.blocksize
                        hitY = y - j * self.blocksize

                        hit = 0

                        if 1 < hitX < self.blocksize-1:
                            if hitY < 1:
                                hit = self.blocksize - hitX
                            elif hitY >= self.blocksize-1:
                                hit = hitX
                        elif 1 < hitY < self.blocksize-1:
                            if hitX < 1:
                                hit = hitY
                            elif hitX >= self.blocksize-1:
                                hit = self.blocksize - hitY

                        tx = hit / self.blocksize

                        return dist, self.map[j][i], tx
            
    def render(self):        
        for column in range(RAY_AMOUNT):
            angle = self.player['angle'] - (self.player['fov'] / 2) + (self.player['fov'] * column / RAY_AMOUNT)
            dist, id, tx = self.castRay(angle)
            rayWidth = int((1 / RAY_AMOUNT) * self.width)
            #print(dist, id)
            for i in range(rayWidth):
                self.zbuffer[column * rayWidth + i] = dist

            startx = int((column / RAY_AMOUNT) * self.width)
            
            #perceivedHeight = screenHeight / (distance * cos(rayAngle - viexAngle)) * wallHeight
            h = self.height / (dist * cos((angle - self.player['angle']) * pi / 180)) * self.wallheight
            startY = int(self.halfHeight - h/2) + self.player['height']
            endY = int(self.halfHeight + h/2)

            color_k = (1-min(1, dist/self.maxdistance)) * 255

            #rect = (x, y, rayWidth, h)
            #color_k = 1 - min(1, dist / self.maxdistance)
            #wallColor = (wallcolors[id][0] * color_k, 
            #             wallcolors[id][1] * color_k,
            #             wallcolors[id][2] * color_k)
            #self.screen.fill(wallColor, rect)
            if dist <= 45 and id == "6":
                self.victoria = True

            tex = wallTextures[id]
            tex = pygame.transform.scale(tex, (tex.get_width() * rayWidth, int(h)))
            #tex.fill((color_k, color_k, color_k), special_flags=pygame.BLEND_MULT)
            tx = int(tx * tex.get_width())
            #print( self.player['heightWall'])
            self.screen.blit(tex, (startx, startY), (tx, 0, rayWidth,tex.get_height()))

        
        self.hitEnemy = False
        for enemy in enemies:
            self.drawSprite(enemy, 50)

        sightRect = (int(self.width / 2 - 2), int(self.height / 2 - 2), 5,5 )
        self.screen.fill(pygame.Color('red') if self.hitEnemy else pygame.Color('white'), sightRect)

        self.drawMinimap()

class Game():
    def __init__(self):
        pygame.init()
        self.map = '1'
        self.runnig, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.Display_w, self.Display_H = 500, 500
        self.display = pygame.Surface((self.Display_w, self.Display_H))
        #self.window = pygame.display.set_mode(((self.Display_w, self.Display_H)))
        self.screen = pygame.display.set_mode((self.Display_w, self.Display_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE )
        self.screen.set_alpha(None)
        self.rCaster = Raycaster(self.screen)
        self.font_name = '8-BIT WONDER.TTF'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 25)
        self.font2 = pygame.font.SysFont('Constantia', 30)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credist = CreditsMenu(self)
        self.pause = PauseMenu(self)
        self.victoria = Victoria(self)
        self.curr_menu = self.main_menu
        self.clicked = False
        self.button_col = (25, 190, 255)
        self.hover_col = (75, 225, 255)
        self.click_col = (50, 150, 255)
        self.text_col = (255, 255, 255)
        self.confirmador = None
        self.name_map = None
        self.heart = pygame.image.load('life.png')
        self.bullet = pygame.image.load('bullet.png')
        self.isPause = False
    
    def loadMap(self):
        self.confirmador = self.rCaster.load_map(mapLevel[self.map])

    def updateFPS(self):
        fps = str(int(self.clock.get_fps()))
        fps = self.font.render(fps, 1, pygame.Color("white"))
        return fps

    def music(sefl):
        mixer.music.load('y2mate.com - Epic Dark Choral Music CTHULHU AWAKENS by Apollon de Moura_64kbps.mp3.mp3')
        mixer.music.play()

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            if self.rCaster.victoria:
                self.curr_menu = self.victoria
                self.playing = False
            halfHeight = int(self.rCaster.height/2) + self.rCaster.player['height']
            # Techo
            self.screen.fill(pygame.Color("saddlebrown"), (0, 0,  self.Display_w, halfHeight))

            # Piso
            self.screen.fill(pygame.Color("dimgray"), (0, halfHeight,  self.Display_w, int(self.Display_H / 2)))
            self.rCaster.render()

            #FPS
            self.screen.fill(pygame.Color("black"), (0,0,30,30))
            self.screen.blit(self.updateFPS(), (0,0))
            self.clock.tick(70)

            self.draw_text2(self.name_map, 20, self.Display_w / 2, 15)
            self.screen.blit(pygame.transform.scale(self.heart, (50, 50)), (5, self.Display_H - 50))
            self.screen.blit(pygame.transform.scale(self.heart, (50, 50)), (40, self.Display_H - 50))
            self.screen.blit(pygame.transform.scale(self.heart, (50, 50)), (75, self.Display_H - 50))
            self.screen.blit(pygame.transform.scale(self.bullet, (50, 50)), (150, self.Display_H - 50))
            self.draw_text2("30/ 30", 30, 275, self.Display_H - 25)
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.runnig, self.playing = False, False
                self.curr_menu.run_display = False
            elif ev.type == pygame.KEYDOWN and self.isPause == False:
                newX = self.rCaster.player['x']
                newY = self.rCaster.player['y']
                forward = self.rCaster.player['angle'] * pi / 180
                rigth = (self.rCaster.player['angle'] + 90) * pi / 180
                if ev.key == pygame.K_RETURN:
                    self.START_KEY = True
                elif ev.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif ev.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif ev.key == pygame.K_UP:
                    self.UP_KEY = True
                elif ev.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.curr_menu = self.pause
                    self.isPause = True
                    mixer.music.pause()
                elif ev.key == pygame.K_w:
                    newX += cos(forward) * self.rCaster.stepsize
                    newY += sin(forward) * self.rCaster.stepsize
                elif ev.key == pygame.K_s:
                    newX -= cos(forward) * self.rCaster.stepsize
                    newY -= sin(forward) * self.rCaster.stepsize
                elif ev.key == pygame.K_a:
                    newX -= cos(rigth) * self.rCaster.stepsize
                    newY -= sin(rigth) * self.rCaster.stepsize
                elif ev.key == pygame.K_d:
                    newX += cos(rigth) * self.rCaster.stepsize
                    newY += sin(rigth) * self.rCaster.stepsize
                elif ev.key == pygame.K_q:
                    self.rCaster.player['angle'] -= self.rCaster.turnSize
                elif ev.key == pygame.K_e:
                    self.rCaster.player['angle'] += self.rCaster.turnSize
                elif ev.key == pygame.K_r:
                    self.rCaster.player['height'] += 100
                elif ev.key == pygame.K_f:
                    self.rCaster.player['height'] -= 100
                elif ev.key == pygame.K_g:
                    self.music()
                elif ev.key == pygame.K_h:
                    mixer.music.pause()
                i = int(newX/self.rCaster.blocksize)
                j = int(newY/self.rCaster.blocksize)

                if self.rCaster.map[j][i] == ' ':
                    self.rCaster.player['x'] = newX  
                    self.rCaster.player['y'] = newY
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
    
    def draw_text2(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)
    
    def draw_button(self, x, y, width, height, text):
        global clicked
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #create pygame Rect ovject for the vutton
        button_rect = Rect(x, y, width, height)
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pygame.draw.rect(self.display, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            else:
                pygame.draw.rect(self.display, self.hover_col, button_rect)
        else: 
            pygame.draw.rect(self.display, self.button_col, button_rect)
        #add shading to button
        pygame.draw.line(self.display, white, (x, y), (x + width, y), 2)
        pygame.draw.line(self.display, white, (x, y), (x, y + height), 2)
        pygame.draw.line(self.display, black, (x, y + height), (x + width, y + height), 2)
        pygame.draw.line(self.display, black, (x + width, y), (x + width, y + height), 2)
        #add text to button
        text_img = self.font2.render(text, True, self.text_col)
        text_len = text_img.get_width()
        self.display.blit(text_img, (x + int(width/2) - int(text_len/2), y + 5))
        return action        
    
    