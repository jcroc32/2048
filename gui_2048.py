from __future__ import print_function
import platform
import sys
# figure out if Windows or Linux machine
if platform.system() == 'Windows':
	from msvcrt import getch
else:
	import termios, tty
	def getch():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)			
		finally:
			termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
		return ch
# figure out if using python 2 or 3
if sys.version_info[0] < 3:
	from Tkinter import *
else:
	from tkinter import *
import random as rn

rn.seed(a=0) # for debugging

# game variables
dimension = 4
board = dimension**2*[0]

file_name = '.HIGHSCORE.txt'
# load high score from txt file
try:
  file = open(file_name,'r')
  high_score = file.read()
except Exception as e:
  file = open(file_name,'w+')
  high_score = 0
try:
  high_score = int(high_score)
except Exception as e:
  high_score = 0

# game actions
def make_fake_board():
	fake_board = len(board)*[0]
	for i in range(len(board)):
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
	free_tiles = [i for i in range(len(board)) if board[i] == 0]
	position = rn.choice(free_tiles)
	p = rn.random()
	tile = 2 if p < .9 else 4
	board[position] = tile
	
def get_action():
	keyboard_input = getch()
	if keyboard_input == b'w' or keyboard_input == b'H' or keyboard_input == b'A':   # up
		step = 1
		factor = dimension
	elif keyboard_input == b'a' or keyboard_input == b'K' or keyboard_input == b'D': # left
		step = 1
		factor = 1
	elif keyboard_input == b's' or keyboard_input == b'P' or keyboard_input == b'B': # down
		step = -1
		factor = dimension
	elif keyboard_input == b'd' or keyboard_input == b'M' or keyboard_input == b'C': # right
		step = -1
		factor = 1
	elif keyboard_input == b'q' or keyboard_input == b'\x03':
		end_game()
	else:
		return
	is_change = move(step,factor)
	if is_change:
		add_tile()
		
def check_if_game_over():
	fake_board = make_fake_board()
	if (move(1,1,fake_board) or move(1,dimension,fake_board) 
	or move(-1,dimension,fake_board) or move(-1,1,fake_board)):
		pass
	else:
		end_game()
	
	
def end_game():
	clear_screen()
	score = sum(board)
	if score < high_score:
		print('GAME OVER, GOOD TRY!')
	else:
		print('NEW HIGHSCORE!')
		file = open(file_name,'w')
		file.write(str(score))
	print_board()
	quit()

def print_board():
	score = sum(board)
	if score < high_score:
		print('SCORE:',score,'HIGHSCORE:',high_score)
	else: 
		print('SCORE:',score,'HIGHSCORE:',score)
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
	
def clear_screen():
	print(48*'\n')
	
def run_game():
	add_tile()
	add_tile()
	while(True):
		clear_screen()
		print_board()
		get_action()
		check_if_game_over()

# start tkinter app
top = Tk()
top.title = '2048'
# make app size 600 by 250
top.geometry('660x660')
# create canvas we can put our buttons and output text on
#  "{0:#0{1}x}".format(2048111,8)[2:]

canvas = Canvas(top, width=160,height=160, bd=1,bg='#cdc1b3')
canvas.grid(row=0, column=0)

canvas = Canvas(top, width=160,height=160, bd=0,bg='#f0e6d6')
canvas.grid(row=0, column=1)
canvas.create_text(80,80,fill='black',font='Times 32 italic bold', text='2')

canvas = Canvas(top, width=160,height=160, bd=0,bg='#ffffa0')
canvas.grid(row=0, column=2)
canvas.create_text(80,80,fill='black',font='Times 32 italic bold', text='4')

canvas = Canvas(top, width=160,height=160, bd=0,bg='#ffe0b5')
canvas.grid(row=0, column=3)
canvas.create_text(80,80,fill='white',font='Times 32 italic bold', text='8')

canvas = Canvas(top, width=160,height=160, bd=0,bg='#ffff30')
canvas.grid(row=1, column=0)
canvas.create_text(80,80,fill='white',font='Times 32 italic bold', text='16')

canvas = Canvas(top, width=160,height=160, bd=0,bg='#ffc5c5')
canvas.grid(row=1, column=1)
canvas.create_text(80,80,fill='white',font='Times 32 italic bold', text='32')

canvas = Canvas(top, width=160,height=160, bd=0,bg='#ffff50')
canvas.grid(row=1, column=2)
canvas.create_text(80,80,fill='white',font='Times 32 italic bold', text='64')

canvas = Canvas(top, width=160,height=160, bd=0,bg='#ffff60')
canvas.grid(row=1, column=3)
canvas.create_text(80,80,fill='white',font='Times 32 italic bold', text='128')

canvas = Canvas(top, width=160,height=160, bd=0,bg='#ffff70')
canvas.grid(row=2, column=0)
canvas.create_text(80,80,fill='white',font='Times 32 italic bold', text='256')


top.mainloop()