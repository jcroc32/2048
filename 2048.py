from __future__ import print_function
# figure out if Windows or Linux machine
import platform
if platform.system() == 'Windows':
	from msvcrt import getch
else:
	import sys, termios, tty
	def getch():
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)			
		finally:
			termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
		return ch
import random as rn
#rn.seed(a=0) # for debugging

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
	if keyboard_input == b'w':   # up
		step = 1
		factor = dimension
	elif keyboard_input == b'a': # right
		step = 1
		factor = 1
	elif keyboard_input == b's': # down
		step = -1
		factor = dimension
	elif keyboard_input == b'd': # left
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

run_game()