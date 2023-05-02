# importing the required libraries
import pygame as pg
import sys
import time
import datetime
from pygame.locals import *
import random

def message(data):

	message = data

	# setting a font object
	font1 = pg.font.Font(None, 30)

	# setting the font properties like
	# color and width of the text
	text = font1.render(message, 1, (255, 255, 255))

	# copy the rendered message onto the board
	# creating a small block at the bottom of the main display
	#text_rect = text.get_rect(center=(width / 2, 500-50))
	screen.fill((0, 0, 0), (0, 430, 500, 50))
	screen.blit(text, (140, 440))


class Semaforo():
	def __init__(self) -> None:
		self.n = 1
		self.fila = []
	
def wait(semaforo):
	if( semaforo.n == 0):
		return False
	semaforo.n = semaforo.n - 1
	return True

def signal(semaforo):
	semaforo.n += 1
	if semaforo.fila:
		semaforo.n -= 1
		return semaforo.fila.pop()
	else:
		return False


# for storing the 'x' or 'o'
# value as character
players = ['x','o']
XO = random.choice(players)

s00 = Semaforo()
s01 = Semaforo()
s02 = Semaforo()
s10 = Semaforo()
s11 = Semaforo()
s12 = Semaforo()
s20 = Semaforo()
s21 = Semaforo()
s22 = Semaforo()

winner = None
draw = None
width = 400
height = 400
white = (255, 255, 255)
line_color = (0, 0, 0)
board = [[None]*3, [None]*3, [None]*3]
semaforos = { 
'00': s00, 
'01': s01,
'02': s02, 
'10': s10,
'11': s11,
'12': s12, 
'20': s20, 
'21': s21, 
'22': s22
}

total_seconds = 5

pg.init()

fps = 30
CLOCK = pg.time.Clock()

screen = pg.display.set_mode((width, height + 100), 0, 32)

pg.display.set_caption("Jogo da Velha com Semáforos")

# loading the images as python object
initiating_window = pg.image.load("modified_cover.png")
x_img = pg.image.load("X_modified.png")
y_img = pg.image.load("o_modified.png")

# resizing images
initiating_window = pg.transform.scale(
	initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))


def game_initiating_window():

	# displaying over the screen
	screen.blit(initiating_window, (0, 0))
	
	# updating the display
	pg.display.update()
	time.sleep(3)

	screen.fill(white)
	screen.fill((0, 0, 0), (0, 400, 500, 100))
	
	pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
	pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)

	pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
	pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)

	draw_status()


def draw_timer(total_seconds):
	timer = datetime.timedelta(seconds = total_seconds)
	font = pg.font.Font(None, 20)
	message_timer = f'Tempo restante {timer.seconds}'
	text_timer = font.render(message_timer, 2, (255, 255, 255))
	screen.fill((0, 0, 0), (0, 400, 500, 30))
	#timer_rect = text_timer.get_rect(center=(60, 420)) 
	screen.blit(text_timer, (10, 415))
	pg.display.update()

def draw_status():

	# getting the global variable draw
	# into action
	global draw

	if winner is None:
		data = "Turno do " + XO.upper()
	else:
		data = winner.upper() + " ganhou!"
	if draw:
		data = "Empate!"

	message(data)
	pg.display.update()


def check_win():
	global board, winner, draw

	# checking for winning rows
	for row in range(0, 3):
		if((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None)):
			winner = board[row][0]
			pg.draw.line(screen, (250, 0, 0),
						(0, (row + 1)*height / 3 - height / 6),
						(width, (row + 1)*height / 3 - height / 6),
						4)
			break

	# checking for winning columns
	for col in range(0, 3):
		if((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):
			winner = board[0][col]
			pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
						((col + 1) * width / 3 - width / 6, height), 4)
			break

	# check for diagonal winners
	if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):

		# game won diagonally left to right
		winner = board[0][0]
		pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

	if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):

		# game won diagonally right to left
		winner = board[0][2]
		pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

	if(all([all(row) for row in board]) and winner is None):
		draw = True
	draw_status()


def drawXO(row, col):
	global board, XO, total_seconds


	if row == 1:
		posx = 30

	if row == 2:
		posx = width / 3 + 30

	if row == 3:
		posx = width / 3 * 2 + 30

	if col == 1:
		posy = 30

	if col == 2:
		posy = height / 3 + 30

	if col == 3:
		posy = height / 3 * 2 + 30

	board[row-1][col-1] = XO

	if(XO == 'x'):
		total_seconds = 5
		screen.blit(x_img, (posy, posx))
		XO = 'o'

	else:
		total_seconds = 5
		screen.blit(o_img, (posy, posx))
		XO = 'x'

	pg.display.update()


def user_click():
	x, y = pg.mouse.get_pos()
	if(x < width / 3):
		col = 1

	elif (x < width / 3 * 2):
		col = 2

	elif(x < width):
		col = 3

	else:
		col = None

	if(y < height / 3):
		row = 1

	elif (y < height / 3 * 2):
		row = 2

	elif(y < height):
		row = 3

	else:
		row = None


	if( row and col):
		id = str(row-1) + str(col-1)
		if( wait(semaforos[id])):
			global XO
			drawXO(row, col)
			check_win()

def draw_game_over_screen():
	screen.fill((0, 0, 0))
	font = pg.font.SysFont('arial', 40)
	title = font.render('Game Over', True, (255, 255, 255))
	restart_button = font.render('R - Restart', True, (255, 255, 255))
	quit_button = font.render('Q - Quit', True, (255, 255, 255))
	screen.blit(title, (width/2 - title.get_width()/2, height/2 - title.get_height()/3))
	screen.blit(restart_button, (width/2 - restart_button.get_width()/2, width/1.9 + restart_button.get_height()))
	screen.blit(quit_button, (width/2 - quit_button.get_width()/2, width/2 + quit_button.get_height()/2))
	pg.display.update()

def reset_game():
	global board, winner, XO, draw, total_seconds
	time.sleep(2)
	total_seconds = 5
	XO = random.choice(players)
	draw = False
	winner = None
	game_initiating_window()
	board = [[None]*3, [None]*3, [None]*3]
	for semaforo in semaforos:
		signal(semaforos[semaforo])

game_initiating_window()
game_state = "game"
while(True):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
		elif event.type == 1025:
			if game_state == "game":
				user_click()
			if(winner or draw):
				time.sleep(2)
				draw_game_over_screen()
				game_state = 'game_over'	
	if game_state == "game_over":
		keys = pg.key.get_pressed()
		if keys[pg.K_r]:
			game_state = "game"
			reset_game()
		if keys[pg.K_q]:
			pg.quit()
			quit()
	if game_state == "game":
		pg.display.update() 
		total_seconds -= 1/30
		if  total_seconds < 0:
			total_seconds = 0
			if XO == 'x':
				XO = 'o'
				winner = 'o'
				draw_status()
				game_state = "game_over"
				time.sleep(1)
				draw_game_over_screen()
			else:
				XO = 'x'
				winner = 'x'
				draw_status()
				game_state = "game_over"
				time.sleep(1)
				draw_game_over_screen()
		draw_timer(total_seconds)
	CLOCK.tick(fps)
