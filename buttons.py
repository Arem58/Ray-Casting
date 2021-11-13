import pygame
from pygame.locals import *

pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

font = pygame.font.SysFont('Constantia', 30)

bg = (200, 200, 200)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

clicked = False
counter = 0

class button():

    button_col = (25, 190, 255)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = (255, 255, 255)
    width = 180
    height = 40

    def __init__(self, x, y, text):
        self.x = x
        self.y = y 
        self.text = text

    def draw_button(self):
        global clicked
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #create pygame Rect ovject for the vutton
        button_rect = Rect(self.x, self.y, self.width, self.height)
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else: 
            pygame.draw.rect(screen, self.button_col, button_rect)
        #add shading to button
        pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
        #add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width/2) - int(text_len/2), self.y + 5))
        return action      

again = button(75, 200, 'Play Again?')
quit = button(325, 200, 'Quit?')
down = button(75, 350, 'Down')
up = button(325, 350, 'Up')


run = True
while run:

	screen.fill(bg)

	if again.draw_button():
		print('Again')
		counter = 0
	if quit.draw_button():
		print('Quit')
	if up.draw_button():
		print('Up')
		counter += 1
	if down.draw_button():
		print('Down')
		counter -= 1

	counter_img = font.render(str(counter), True, red)
	screen.blit(counter_img, (280, 450))


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False	


	pygame.display.update()


pygame.quit()