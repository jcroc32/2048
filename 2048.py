#!/usr/bin/python3
from __future__ import print_function
import sys
import os
import platform
import random
import copy
# import correct packages for python 2 or 3
if sys.version_info[0] < 3:
	import Tkinter as tkinter
	from pathlib2 import Path
else:
	import tkinter
	from pathlib import Path
root = tkinter.Tk()

###--game variables--###
global board
global score
global high_score
global use_old_game
dimension = 4
total_tiles = dimension*dimension
game_data_folder = '.2048gamedata/.'
Path(game_data_folder).mkdir(exist_ok=True)
if platform.system() == 'Windows':
	import subprocess
	subprocess.check_call(["attrib","+H",game_data_folder])
high_score_file = game_data_folder + str(dimension) + 'DHIGHSCORE.txt'
previous_game_file = game_data_folder + str(dimension) + 'DPREVIOUSGAME.txt'
previous_score_file = game_data_folder + str(dimension) + 'DPREVIOUSSCORE.txt'
colormap = {0:'#cdc1b4', 2:'#eee4da', 4:'#ede0c8', 8:'#f2b179', 16:'#f59563', 32:'#f67c5f',
			64:'#f6603c', 128:'#eed072', 256: '#edcc61', 512:'#ecc851', 1024:'#edc53f', 
			2048:'#edc22e', 4096:'#f925d2', 8192:'#ff2ab3', 16384:'#fb2ea4', 32768:'#fb3572'}
###------------------###

###--GUI variables--###
global retry_button_text
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width_tile = 130
height_tile = 130
height_scoreboard = 50
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
score_board = top.create_text((total_width - 200, height_scoreboard/2), text='', font='Times 12 italic bold')
hight_score_board = top.create_text((total_width - 75, height_scoreboard/2), text='',font='Times 12 italic bold')
game_over_box = top.create_text((75,25), text='', font='Times 16 italic bold', fill='red')
retry_button_window = top.create_window(175, 25)
retry_button_text = tkinter.StringVar()
top.pack()
###-----------------###

###--GUI actions--###
def save_game():
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
#
def on_closing():
	save_game()
	root.destroy()
#
root.protocol("WM_DELETE_WINDOW", on_closing)
#
def init_game():
	global board
	global score
	global retry_button_text
	global use_old_game
	if use_old_game:
		use_old_game = not check_if_game_over(board)
	if not use_old_game:
		board = total_tiles*[0]
		score = 0
		add_tile(board)
		add_tile(board)
	use_old_game = False
	top.itemconfig(hight_score_board, text='high score: '+str(high_score), fill='grey')
	retry_button_text.set('Start over')
	retry_button = tkinter.Button(top, textvariable=retry_button_text, command=init_game, bg='#c0c0c0')
	top.itemconfig(retry_button_window, window=retry_button)
	top.coords(retry_button_window,(50,25))
	top.itemconfig(game_over_box, text='')
	top.coords(game_over_box,(75,25))
	update_board(board, score)
#
def set_score(score):
	global high_score
	top.itemconfig(score_board, text='score: ' + str(score))
	if score > high_score:
		high_score = score
		top.itemconfig(hight_score_board, text='high score: '+str(high_score), fill='black')
#
def update_board(board, score):
	for i in range(total_tiles):
		tile = board[i]
		if tile > 32768:
			bg = '#3c3a32'
		else:
			bg = colormap[tile]
		if tile == 0:
			text = ''
		else:
			text = str(tile)
		top.itemconfig(tile_board[i], fill=bg)
		top.itemconfig(text_board[i], text=text)
	set_score(score)
#
def end_game():
	global score
	global high_score
	global retry_button_text
	retry_button_text.set('Try Again?')
	top.coords(retry_button_window,(200, 25))
	top.itemconfig(score_board, text='')
	top.itemconfig(hight_score_board, text='')
	top.itemconfig(game_over_box, text='GAME OVER')
	if score == high_score:
		top.itemconfig(game_over_box, text='NEW HIGHSCORE!')
		top.coords(game_over_box,(100,25))
		top.coords(retry_button_window,(250, 25))
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
def up(i):
	return lambda j: j*dimension + i
#
def left(i):
	return lambda j: i*dimension + j
#
def down(i):
	return lambda j: (dimension - j - 1)*dimension + i
#
def right(i):
	return lambda j: (i + 1)*dimension - j - 1
#
def collect_tiles(board, f):
	needs_update = False
	zeros = 0
	non_zero = 0
	for i in range(dimension):
		if board[f(i)] == 0:
			zeros+=1
		else:
			non_zero+=1
			if zeros > 0:
				board[f(i - zeros)] = board[f(i)]
				board[f(i)] = 0
				needs_update = True
	return non_zero, needs_update
#
def match_tiles(board, non_zero, f):
	needs_update = False
	move_score = 0
	i = 0
	pad = 0
	while i < non_zero-1:
		tile_value = board[f(i)]
		if tile_value == board[f(i+1)]:
			board[f(i-pad)] = tile_value*2
			pad+=1
			i+=1
			move_score+=tile_value*2
		else:
			board[f(i-pad)] = tile_value
		i+=1
	if i < non_zero:
		board[f(i-pad)] = board[f(i)]
	for i in range(non_zero-pad,non_zero):
		board[f(i)] = 0
	return move_score
#
def move(board, direction):
	needs_update = False
	move_score = 0
	for i in range(dimension):
		f = direction(i)
		non_zero, update = collect_tiles(board,f)
		move_score+=match_tiles(board,non_zero,f)
		needs_update = needs_update or update or move_score > 0
	return needs_update, move_score
#
def check_if_game_over(board):
	test_board = copy.deepcopy(board)
	for i in range(total_tiles):
		if test_board[i] == 0:
			return False
	for i in range(dimension):
		for j in range(dimension-1):
			if test_board[up(i)(j)] == test_board[up(i)(j+1)]:
				return False
			if test_board[left(i)(j)] == test_board[left(i)(j+1)]:
				return False
	return True
#
def move_direction(direction):
	global board
	global score
	needs_update, move_score = move(board, direction)
	if needs_update:
		score += move_score
		add_tile(board)
		update_board(board, score)
		if check_if_game_over(board):
			end_game()
#
def move_up(event):
	move_direction(up)
def move_left(event):
	move_direction(left)
def move_down(event):
	move_direction(down)
def move_right(event):
	move_direction(right)
###----------------###

###--Debugging actions--###
def print_board(board):
	for i in range(dimension):
		start = dimension*i
		end = start+dimension
		print(' '+(13*dimension-1)*'-')
		print('|'+dimension*(12*' '+'|'))
		print('|',end='')
		for j in board[start:end]:
			if j == 0:
				print('{0:8s}    |'.format(' '),end='')
			else:
				print('{0:9d}   |'.format(j),end='')
		print('\n|'+dimension*(12*' '+'|'))
	print(' '+(13*dimension-1)*'-')
###---------------------###

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

init_game()
top.mainloop()