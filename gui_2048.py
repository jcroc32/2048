import sys
import math
import random
import copy
# import correct package for python 2 or 3
if sys.version_info[0] < 3:
	import Tkinter as tkinter
else:
	import tkinter
root = tkinter.Tk()

###--game variables--###
global board
global score
global high_score
global use_old_game
dimension = 3
total_tiles = dimension**2
game_data_folder = '.2048gamedata/'
high_score_file = game_data_folder + '.HIGHSCOREFOR'+str(dimension)+'DBOARD.txt'
previous_game_file = game_data_folder + '.PREVIOUSGAMEFOR'+str(dimension)+'DBOARD.txt'
previous_score_file = game_data_folder + '.PREVIOUSSCOREFOR'+str(dimension)+'DBOARD.txt'
###------------------###
'''
def set_dim(dim):
    dimension = dim
scale = tkinter.Scale(orient='horizontal', from_=2, to=10, command=set_dim)
scale.pack()
scale.mainloop()
'''
###--GUI variables--###
global retry_button_text
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width_tile = 130
height_tile = 130
height_scoreboard = 50
width_scoreboard = 130
pad = 5
total_width = (width_tile + pad)*dimension + pad
total_height = (height_tile + pad)*dimension + pad + height_scoreboard
top = tkinter.Canvas(root, width=total_width, height=total_height)
tile_cords = total_tiles*[0]
for i in range(total_tiles):
	x1 = pad + (width_tile + pad)*(i%dimension)
	y1 = height_scoreboard + pad + (height_tile + pad)*(i//dimension)
	x2 = (width_tile + pad)*(1 + i%dimension)
	y2 = height_scoreboard + (height_tile + pad)*(1 + i//dimension)
	tile_cords[i] = (x1,y1,x2,y2)
text_cords = total_tiles*[0]
for i in range(total_tiles):
	x = pad + width_tile/2 + (width_tile + pad)*(i%dimension)
	y = height_scoreboard + pad + height_tile/2 + (height_tile + pad)*(i//dimension)
	text_cords[i] = (x,y)
tile_board = [top.create_rectangle(tile_cords[i], fill='#cdcdcd') for i in range(total_tiles)]
text_board = [top.create_text(text_cords[i], text='', font='Times 24 italic bold') for i in range(total_tiles)]
score_board = top.create_text((total_width - 150, height_scoreboard/2), text='', font='Times 12 italic bold')
hight_score_board = top.create_text((total_width - 50, height_scoreboard/2), text='',font='Times 12 italic bold')
game_over_box = top.create_text((75,25), text='', font='Times 16 italic bold', fill='red')
retry_button_window = top.create_window(175, 25)
retry_button_text = tkinter.StringVar()
top.pack()
###-----------------###

###--GUI actions--###
def on_closing():
	file = open(previous_game_file, 'w')
	file.write(str(board))
	file.close()
	file = open(previous_score_file, 'w')
	file.write(str(score))
	file.close()
	if score == high_score:
		file = open(high_score_file, 'w')
		file.write(str(high_score))
		file.close()
	root.destroy()
#
root.protocol("WM_DELETE_WINDOW", on_closing)
#
def init_gui_board():
	global board
	global score
	global retry_button_text
	global use_old_game
	if use_old_game:
		use_old_game = check_if_moves_possible(board)
	if not use_old_game:
		board = total_tiles*[0]
		score = 0
		add_tile(board)
		add_tile(board)
	use_old_game = False
	retry_button_text.set('Start over')
	retry_button = tkinter.Button(top, textvariable=retry_button_text, command=init_gui_board, bg='#c0c0c0')
	top.itemconfig(retry_button_window, window=retry_button)
	top.coords(retry_button_window,(50,25))
	top.itemconfig(game_over_box, text='')
	top.coords(game_over_box,(75,25))
	update_gui_board(board, score)
#
def set_score(score):
	global high_score
	top.itemconfig(score_board, text='score: ' + str(score))
	if score > high_score:
		high_score = score
	top.itemconfig(hight_score_board, text='high score: '+str(high_score))
#
def update_gui_board(board, score):
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
	set_score(score)
#
def end_gui_game():
	global score
	global high_score
	global retry_button_text
	retry_button_text.set('Try Again?')
	top.coords(retry_button_window,(180, 25))
	top.itemconfig(score_board, text='')
	top.itemconfig(hight_score_board, text='')
	top.itemconfig(game_over_box, text='GAME OVER')
	if score == high_score:
		top.itemconfig(game_over_box, text='NEW HIGHSCORE!')
		top.coords(game_over_box,(100,25))
		top.coords(retry_button_window,(240, 25))
		file = open(high_score_file, 'w')
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
#
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
#
def check_if_moves_possible(board):
	test_board = copy.deepcopy(board)
	move_possible = (move(1, 1, test_board)[0] or move(1, dimension, test_board)[0] 
				or move(-1, dimension, test_board)[0] or move(-1, 1, test_board)[0])
	return move_possible
#
def move_direction(step, factor):
	global board
	global score
	needs_update, move_score = move(step, factor, board)
	if needs_update:
		score += move_score
		add_tile(board)
		update_gui_board(board, score)
		move_possible = check_if_moves_possible(board)
		if not move_possible:
			end_gui_game()
#
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

# load previuos game, score, and high score from txt file
use_old_game = True
try:
	file = open(previous_game_file,'r')
	board = file.read()
	file.close()
	board = list(map(int, board[1:-1].split(',')))
	file = open(previous_score_file,'r')
	score = int(file.read())
	file.close()
	file = open(high_score_file, 'r')
	high_score = int(file.read())
	file.close()
	if len(board) != total_tiles:
		use_old_game = False
except Exception as e:
	use_old_game = False
	high_score = 0

root.title('2048')
root.minsize(total_width, total_height)
root.maxsize(screen_width, screen_height)
root.bind('<Up>', move_up)
root.bind('<Down>', move_down)
root.bind('<Left>', move_left)
root.bind('<Right>', move_right)

init_gui_board()
top.mainloop()