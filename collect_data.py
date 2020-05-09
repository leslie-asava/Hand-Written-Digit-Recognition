import pygame
import os
from PIL import ImageGrab # Use for Windows
#import pyscreenshot as ImageGrab # Use for Linux
import datetime
import os

pygame.init()


x = 100
y = 100
SCREENWIDTH = 300
SCREENHEIGHT = 300

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#capture_window = (x+5,y+25,x+SCREENWIDTH+5,y+SCREENHEIGHT+25) Use for Linux
capture_window = (x,y,x+SCREENWIDTH,y+SCREENHEIGHT) # use for Windows

BLACK = (0,0,0)
WHITE = (255,255,255)
LIME = (0,255,0)
BLUE = (0,0,255)

def get_filename():
    now = str(datetime.datetime.now())
    now = now.replace(" ","")
    now = now.replace(":","")
    now = now.replace("-","")
    now = now.replace(".","")
    now+=".png"
    return now

get_filename()

class Brush(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface((30,30))
		self.image.fill(LIME)
		self.image.set_colorkey(LIME)
		self.rect = self.image.get_rect()
		self.can_draw = False
		self.x = 0
		self.y = 0
		self.color = BLACK

	def update(self):
		if not self.can_draw:
			pygame.mouse.set_visible(True)

		if (self.can_draw):
			pygame.mouse.set_visible(False)
			pygame.draw.circle(self.image,self.color,(self.rect.centerx,self.rect.centery),15)
			self.rect.x,self.rect.y = pygame.mouse.get_pos()


screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT+35))
screen.fill(WHITE)
instruction_font = pygame.font.Font('freesansbold.ttf', 15)

brush_group = pygame.sprite.Group()

brush = Brush()

brush_group.add(brush)

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			brush.can_draw = True
		if event.type == pygame.MOUSEBUTTONUP:
			brush.can_draw = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				brush.rect.x,brush.rect.y = -50,0
				screen.fill(WHITE)
			if event.key == pygame.K_s:
				image = ImageGrab.grab(capture_window)
				image.save(os.path.join("",get_filename()))
				brush.rect.x,brush.rect.y = -50,0
				screen.fill(WHITE)
	brush_group.draw(screen)
	brush_group.update()
	pygame.draw.rect(screen,(BLACK),(0,SCREENHEIGHT,300,35))
	instruction = instruction_font.render("Press [S] to save and [R] to refresh", True, (0,255,0), (0,0,0))
	screen.blit(instruction,(20,SCREENHEIGHT+10))
	pygame.display.flip()
quit()

