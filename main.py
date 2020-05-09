import pygame
import os
from PIL import ImageGrab
#from PIL import Image
#import pyscreenshot as ImageGrab
import datetime
import os
import cv2
import numpy as np
import tensorflow

pygame.init()


x = 100
y = 100
SCREENWIDTH = 300
SCREENHEIGHT = 300

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
#capture_window = (x+5,y+25,x+SCREENWIDTH+5,y+SCREENHEIGHT+25)
capture_window = (x,y,x+SCREENWIDTH,y+SCREENHEIGHT)

BLACK = (0,0,0)
WHITE = (255,255,255)
LIME = (0,255,0)
BLUE = (0,0,255)

CATEGORIES = ["0","1","2","3","4","5","6","7","8","9"," "]

model = tensorflow.keras.models.load_model("brain")

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


screen = pygame.display.set_mode((SCREENWIDTH+150,SCREENHEIGHT+35))
screen.fill(BLACK)
pygame.display.set_caption("Hand Written Digit Recognition")
pygame.draw.rect(screen,(WHITE),(0,0,300,300))
predicted_font = pygame.font.Font('freesansbold.ttf', 20)
prediction_font = pygame.font.Font('freesansbold.ttf', 100)
instruction_font = pygame.font.Font('freesansbold.ttf', 15)


brush_group = pygame.sprite.Group()

brush = Brush()

brush_group.add(brush)

running = True

predicted = "0"
prediction = 10

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
                screen.fill(BLACK)
                pygame.draw.rect(screen,(WHITE),(0,0,300,300))
            if event.key == pygame.K_p:
                image = ImageGrab.grab(capture_window)
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                image = image/255.0
                image = cv2.resize(image,(50,50))
                image = np.reshape(image,(1,50,50,1))
                predicted = model.predict(image)
                prediction=np.argmax(predicted)
                print(CATEGORIES[prediction])
                brush.rect.x,brush.rect.y = -50,0
                screen.fill(BLACK)
                pygame.draw.rect(screen,(WHITE),(0,0,300,300))
    brush_group.draw(screen)
    brush_group.update()
    predicted_value = predicted_font.render("PREDICTION", True, (0,200,0), (0,0,0))
    prediction_made = prediction_font.render(CATEGORIES[prediction], True, (0,200,0), (0,0,0))
    instruction = instruction_font.render("Press [P] to predict and [R] to refresh", True, (0,255,0), (0,0,0))
    screen.blit(predicted_value,(315,10))
    screen.blit(prediction_made,(345,40))
    screen.blit(instruction,(20,SCREENHEIGHT+10))
    pygame.display.flip()
quit()

