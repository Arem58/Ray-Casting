import pygame, sys

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.Display_w/2, self.game.Display_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)
    
    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()
    
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startX, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 55
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 80
        self.cursor_rect.midtop = (self.startX + self.offset, self.starty)
        self.background = pygame.image.load('background.jpg')


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_state()
            self.check_input()
            self.game.display.fill(pygame.Color("gray"))
            self.game.display.blit(self.background, (0, 0))
            self.game.draw_text('Chutillu y el pana miguel', 22, self.game.Display_w/2, self.game.Display_H/2 - 100)
            self.game.draw_text('Main Menu', 20, self.game.Display_w/2, self.game.Display_H/2 - 20)
            self.game.draw_text('Start Game', 20, self.startX, self.starty)
            self.game.draw_text('Credits', 20, self.optionsx, self.optionsy)
            self.game.draw_text('Quit', 20, self.creditsx, self.creditsy)
            if self.game.draw_button(150, self.creditsy + 50, 200, 40,'Start game'):
                self.game.curr_menu = self.game.options
                self.run_display = False
            if self.game.draw_button(150, self.creditsy + 100, 200, 40,'Quit'):
                pygame.quit()
                sys.exit()
            self.draw_cursor()
            self.blit_screen()
            #print(self.game.rCaster.map)
    
    def check_state(self):
        if self.state == 'Start':
            self.game.loadMap()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startX + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Quit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startX + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
        
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.options
            elif self.state == 'Options':
                self.game.curr_menu = self.game.credist
            elif self.state == 'Quit':
                pygame.quit()
                sys.exit()
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'map1'
        self.map1x, self.map1y = self.mid_w, self.mid_h + 20
        self.map2x, self.map2y = self.mid_w, self.mid_h + 50
        self.map3x, self.map3y = self.mid_w, self.mid_h + 80
        self.cursor_rect.midtop = (self.map1x + self.offset, self.map1y)
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_state()
            self.game.check_events()
            self.check_inputs()
            self.game.display.fill((0,0,0))
            self.game.draw_text('Maps', 20, self.game.Display_w/2, self.game.Display_H/2 - 20)
            self.game.draw_text('Ululu', 15, self.map1x, self.map1y)
            self.game.draw_text('El ayayay', 15, self.map2x, self.map2y)
            self.game.draw_text('La matraca', 15, self.map3x, self.map3y)
            self.draw_cursor()
            self.blit_screen()
        
    def check_state(self):
        if self.state == 'map1':
            self.game.rCaster.map = []
            self.game.map = '1'
            self.game.loadMap()
        elif self.state == 'map2':
            self.game.rCaster.map = []
            self.game.map = '2'
            self.game.loadMap()
        elif self.state == 'map3':
            self.game.rCaster.map = []
            self.game.map = '3'
            self.game.loadMap()
    
    def check_inputs(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == 'map1':
                self.cursor_rect.midtop = (self.map2x + self.offset, self.map2y)
                self.state = 'map2'
            elif self.state == 'map2':
                self.cursor_rect.midtop = (self.map3x + self.offset, self.map3y)
                self.state = 'map3'
            elif self.state == 'map3':
                self.cursor_rect.midtop = (self.map1x + self.offset, self.map1y)
                self.state = 'map1'
        elif self.game.UP_KEY:
            if self.state == 'map1':
                self.cursor_rect.midtop = (self.map3x + self.offset, self.map3y)
                self.state = 'map3'
            elif self.state == 'map3':
                self.cursor_rect.midtop = (self.map2x + self.offset, self.map2y)
                self.state = 'map2'
            elif self.state == 'map2':
                self.cursor_rect.midtop = (self.map1x + self.offset, self.map1y)
                self.state = 'map1'
        elif self.game.START_KEY:
            self.game.playing = True
            self.run_display = False

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True 
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.Display_w/2, self.game.Display_H/2 - 20)
            self.game.draw_text('Made by me', 15, self.game.Display_w/2, self.game.Display_H/2 + 10)
            self.blit_screen()