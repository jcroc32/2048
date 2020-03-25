import sys
import math
import random
# figure out if using python 2 or 3
if sys.version_info[0] < 3:
	import Tkinter as tkinter
else:
	import tkinter

###--game variables--###
dimension = 4
total_tiles = dimension**2
board = total_tiles*[0]
file_name = '.HIGHSCORE.txt'
high_score = 0
###------------------###

###--GUI variables--###
width_tile = 130
height_tile = 130
height_scoreboard = 50
font_tile = 'Times 24 italic bold'
font_scoreboard = 'Times 12 italic bold'
fill = 'black'
root = tkinter.Tk()
top = tkinter.Canvas(root,width=535,height=585)
###-----------------###

###--GUI actions--###
def make_gui_tile(width,height,bg,row,column,fill,font,text):
	if bg == '':
		canvas = tkinter.Canvas(top,width=width,height=height)
	else:
		canvas = tkinter.Canvas(top,width=width,height=height,bg=bg)
	canvas.grid(row=row,column=column)
	canvas.create_text(width/2,height/2,fill=fill,font=font,text=text)

def set_score(score,high_score):
	# make score box
	width = width_tile
	height = height_scoreboard
	bg = ''
	row = 0
	column = dimension-1
	font = font_scoreboard
	text = 'score: '+str(score)
	make_gui_tile(width,height,bg,row,column,fill,font,text)
	# make highscore box
	if score > high_score:
		high_score = score
	column = dimension
	text = 'high score: '+str(high_score)
	make_gui_tile(width,height,bg,row,column,fill,font,text)

def init_gui_board():
	board = total_tiles*[0]
	add_tile()
	add_tile()
	# retry_button_canvas.pack_forget()
	width = width_tile
	height = height_scoreboard
	bg = ''
	row = 0
	font = font_scoreboard
	text = ''
	for column in [1,2]:
		make_gui_tile(width,height,bg,row,column,fill,font,text)
	# create all tiles
	height = height_tile
	bg = '#cdcdcd'
	text = ''
	font = font_tile
	for i in range(total_tiles):
		row = i//dimension+1
		column = i%dimension+1
		make_gui_tile(width,height,bg,row,column,fill,font,text)
	# make scoreboard
	set_score(0,high_score)
	top.pack()

def update_gui_board():
	width = width_tile
	height = height_tile
	font = font_tile
	for i in range(total_tiles):
		tile = board[i]
		if tile == 0:
			bg = '#cdcdcd'
		elif tile < 64:
			bg = '#'+'{0:#0{1}x}'.format(13487565 - 34*int(math.log(tile,2)),8)[2:]
		elif tile < 4096:
			bg = '#'+'{0:#0{1}x}'.format(13487395 - 34*int(math.log(tile,2)-5)*256,8)[2:]
		else:
			bg = '#'+'{0:#0{1}x}'.format(13435171 - 34*int(math.log(tile,2)-11)*65536,8)[2:]
		row = i//dimension+1
		column = i%dimension+1
		if tile == 0:
			text = ''
		else:
			text = str(tile)
		make_gui_tile(width,height,bg,row,column,fill,font,text)
	set_score(sum(board),high_score)
	top.pack()

def end_gui_game(init_gui_board):
	width = width_tile
	height = height_scoreboard
	bg = ''
	text = 'GAME OVER'
	font = 'Times 16 italic bold'
	fill = 'red'
	row = 0
	column = 1
	make_gui_tile(width,height,bg,row,column,fill,font,text)
	canvas = tkinter.Canvas(top,width=width,height=height_scoreboard)
	canvas.grid(row=0,column=2)
	retry_button = tkinter.Button(canvas,text='Try Again?',command=init_gui_board,bg='#c0c0c0')
	retry_button_window = canvas.create_window(65,25,window=retry_button)
	top.pack()
###---------------###

###--Game actions--###
def make_fake_board():
	fake_board = total_tiles*[0]
	for i in range(total_tiles):
		fake_board[i] = board[i]
	return fake_board

def move(step,factor,board=board):
	is_change = False
	for i in (range(dimension)[::step])[:-1]:
		start = factor*i
		end = int(start+dimension**2/factor)
		for j in range(start,end,int(dimension/factor)):
			next_index = j+step*factor
			if board[j] == 0:
				board[j] = board[next_index]
				board[next_index] = 0
				if board[j] != 0:
					is_change = True
			elif board[j] == board[next_index]:
				board[j] *= 2
				board[next_index] = 0
				is_change = True
	return is_change

def add_tile():
	free_tiles = [i for i in range(total_tiles) if board[i] == 0]
	position = random.choice(free_tiles)
	p = random.random()
	tile = 2 if p < .9 else 4
	board[position] = tile

def check_if_game_over():
	fake_board = make_fake_board()
	if (move(1,1,fake_board) or move(1,dimension,fake_board) 
	or move(-1,dimension,fake_board) or move(-1,1,fake_board)):
		pass
	else:
		end_gui_game(init_gui_board)
	
def get_action(event):
	keyboard_input = event.char
	if keyboard_input == 'w':   # up
		step = 1
		factor = dimension
	elif keyboard_input == 'a': # left
		step = 1
		factor = 1
	elif keyboard_input == 's': # down
		step = -1
		factor = dimension
	elif keyboard_input == 'd': # right
		step = -1
		factor = 1
	else:
		return
	is_change = move(step,factor)
	if is_change:
		add_tile()
	update_gui_board()
	check_if_game_over()
	
def run_game():
	init_gui_board()
	update_gui_board()
	top.mainloop()	
###----------------###

# load high score from txt file
try:
	file = open(file_name,'r')
	high_score = file.read()
except Exception as e:
	# create file if doesn't exist
	file = open(file_name,'w+')
	high_score = 0
try:
	# set highscore
	high_score = int(high_score)
except Exception as e:
	high_score = 0

root.title('2048')
root.minsize(535,585)
root.maxsize(535,585)
root.bind("<Key>", get_action)

run_game()