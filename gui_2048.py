import sys
import math
import random
import copy
# import correct package for python 2 or 3
if sys.version_info[0] < 3:
	import Tkinter as tkinter
else:
	import tkinter

###--game variables--###
global board
global score
global high_score
dimension = 4
total_tiles = dimension**2
file_name = '.HIGHSCORE.txt'
###------------------###

###--GUI variables--###
width_tile = 130
height_tile = 130
height_scoreboard = 50
width_scoreboard = 130
pad = 5
total_width = (width_tile + pad)*dimension + pad
total_height = (height_tile+pad)*dimension + pad + height_scoreboard
font_tile = 'Times 24 italic bold'
font_scoreboard = 'Times 12 italic bold'
root = tkinter.Tk()
top = tkinter.Canvas(root, width=total_width, height=total_height)
def tile_cords(index):
	x1 = pad + (width_tile + pad)*(index%dimension)
	y1 = height_scoreboard + pad + (height_tile + pad)*(index//dimension)
	x2 = (width_tile + pad)*(1 + index%dimension)
	y2 = height_scoreboard + (height_tile + pad)*(1 + index//dimension)
	return x1, y1, x2, y2
tile_board = [top.create_rectangle(tile_cords(i), fill='#cdcdcd') for i in range(total_tiles)]
text_board = [top.create_text((tile_cords(i)[0] + width_tile/2,tile_cords(i)[1] + height_tile/2), text = '') for i in range(total_tiles)]
top.pack()
###-----------------###

###--GUI actions--###
def make_gui_tile(width, height, bg, row, column, font, text):
	if bg == '':
		canvas = tkinter.Canvas(top, width=width, height=height)
	else:
		canvas = tkinter.Canvas(top, width=width, height=height, bg=bg)
	canvas.grid(row=row,column=column)
	canvas.create_text(width/2, height/2, font=font, text=text)

def set_score(score):
	global high_score
	width = width_scoreboard
	height = height_scoreboard
	bg = ''
	row = 0
	column = dimension-1
	font = font_scoreboard
	text = 'score: ' + str(score)
	make_gui_tile(width, height, bg, row, column, font, text)
	if score > high_score:
		high_score = score
	column = dimension
	text = 'high score: '+str(high_score)
	make_gui_tile(width, height, bg, row, column, font, text)

def init_gui_board():
	global board
	global score
	board = total_tiles*[0]
	score = 0
	add_tile(board)
	add_tile(board)
	update_gui_board(board, score)

def update_gui_board(board, score):
	width = width_tile
	height = height_tile
	font = font_tile
	for i in range(total_tiles):
		tile = board[i]
		if tile == 0:
			bg = '#cdcdcd'
		elif tile < 64:
			bg = '#'+'{0:#0{1}x}'.format(13487565 - 34*int(math.log(tile, 2)), 8)[2:]
		elif tile < 4096:
			bg = '#'+'{0:#0{1}x}'.format(13487395 - 34*int(math.log(tile, 2)-5)*256, 8)[2:]
		else:
			bg = '#'+'{0:#0{1}x}'.format(13435171 - 34*int(math.log(tile, 2)-11)*65536, 8)[2:]
		if tile == 0:
			text = ''
		else:
			text = str(tile)
		top.itemconfig(tile_board[i], fill=bg)
		top.itemconfig(text_board[i], text=text)
	# set_score(score)

def end_gui_game():
	global score
	global high_score
	width = width_tile
	height = height_scoreboard
	bg = ''
	text = 'GAME OVER'
	font = 'Times 16 italic bold'
	row = 0
	column = 1
	make_gui_tile(width, height, bg, row, column, font, text)
	canvas = tkinter.Canvas(top, width=width, height=height_scoreboard)
	canvas.grid(row=0, column=2)
	retry_button = tkinter.Button(canvas, text='Try Again?', command=init_gui_board, bg='#c0c0c0')
	retry_button_window = canvas.create_window(65, 25, window=retry_button)
	top.pack()
	if score == high_score:
		file = open(file_name, 'w')
		file.write(str(high_score))
		file.close()
###---------------###

###--Game actions--###	
def add_tile(board):
	free_tiles = [i for i in range(total_tiles) if board[i] == 0]
	position = random.choice(free_tiles)
	p = random.random()
	tile = 2 if p < .9 else 4
	board[position] = tile

def move(step,factor,board):
	move_score = 0
	needs_update = False
	for i in (range(dimension)[::step])[:-1]:
		start = factor*i
		end = int(start+dimension**2/factor)
		for j in range(start,end,int(dimension/factor)):
			next_index = j + step*factor
			if board[j] == 0:
				board[j] = board[next_index]
				board[next_index] = 0
				if board[j] != 0:
					needs_update = True
			elif board[j] == board[next_index]:
				board[j] *= 2
				board[next_index] = 0
				needs_update = True
				move_score += board[j]
	return needs_update, move_score

def check_if_game_over(board):
	test_board = copy.deepcopy(board)
	move_possible = (move(1, 1, test_board)[0] or move(1, dimension, test_board)[0] 
				or move(-1, dimension, test_board)[0] or move(-1, 1, test_board)[0])
	if move_possible:
		pass
	else:
		end_gui_game()

def move_direction(step, factor):
	global board
	global score
	needs_update, move_score = move(step, factor, board)
	if needs_update:
		score += move_score
		add_tile(board)
		update_gui_board(board, score)
		check_if_game_over(board)

def move_up(event):
	step = 1
	factor = dimension
	move_direction(step, factor)
def move_left(event):
	step = 1
	factor = 1
	move_direction(step, factor)
def move_down(event):
	step = -1
	factor = dimension
	move_direction(step, factor)
def move_right(event):
	step = -1
	factor = 1
	move_direction(step, factor)
###----------------###

# load high score from txt file
try:
	file = open(file_name, 'r')
	high_score = file.read()
	high_score = int(high_score)
	file.close()
except Exception as e:
	file = open(file_name, 'w')
	high_score = 0
	file.close()

root.title('2048')
root.minsize(total_width, total_height)
root.maxsize(total_width, total_height)
root.bind('<Up>', move_up)
root.bind('<Down>', move_down)
root.bind('<Left>', move_left)
root.bind('<Right>', move_right)

init_gui_board()
top.mainloop()