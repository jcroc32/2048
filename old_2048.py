from __future__ import print_function
# figure out if using python 2 or 3
import sys
if sys.version_info[0] < 3:
  def input(s):
    return raw_input(s)
import random as rn
rn.seed(a=0)

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
def add_tile(board=board):
	free_tiles = [i for i in range(len(board)) if board[i] == 0]
	if (len(free_tiles)) == 0:
		end_game(board)
	position = rn.choice(free_tiles)
	p = rn.random()
	tile = 2 if p < .9 else 4
	board[position] = tile

def move_down(board=board,dimension=dimension):
	for i in range(1,dimension)[::-1]:
		start = dimension*i
		end = start+dimension
		for j in range(start,end):
			if board[j] == 0:
				board[j] = board[j-dimension]
				board[j-dimension] = 0
			elif board[j] == board[j-dimension]:
				board[j] *= 2
				board[j-dimension] = 0

def move_up(board=board,dimension=dimension):
	for i in range(dimension-1):
		start = dimension*i
		end = start+dimension
		for j in range(start,end):
			if board[j] == 0:
				board[j] = board[j+dimension]
				board[j+dimension] = 0
			elif board[j] == board[j+dimension]:
				board[j] *= 2
				board[j+dimension] = 0

def move_right(board=board,dimension=dimension):
	for i in range(1,dimension)[::-1]:
		start = i
		end = dimension**2
		for j in range(start,end,dimension):
			if board[j] == 0:
				board[j] = board[j-1]
				board[j-1] = 0
			elif board[j] == board[j-1]:
				board[j] *= 2
				board[j-1] = 0

def move_left(board=board,dimension=dimension):
	for i in range(dimension-1):
		start = i
		end = dimension**2
		for j in range(start,end,dimension):
			if board[j] == 0:
				board[j] = board[j+1]
				board[j+1] = 0
			elif board[j] == board[j+1]:
				board[j] *= 2
				board[j+1] = 0

def get_input(board=board):
	keyboard_input = input('')
	if keyboard_input == 'w':
		move_up()
	elif keyboard_input == 's':
		move_down()
	elif keyboard_input == 'd':
		move_right()
	elif keyboard_input == 'a':
		move_left()
	elif keyboard_input == 'quit':
		end_game()
	else:
		clear_screen()
		print_board()
		get_input()

def end_game(board=board,high_score=high_score,file_name=file_name):
	clear_screen()
	score = sum(board)
	if score < high_score:
		print('GAME OVER, GOOD TRY!')
	else:
		high_score = score
		print('NEW HIGHSCORE!')
		file = open(file_name,'w')
		file.write(str(high_score))
	print_board()
	quit()

def print_board(board=board,dimension=dimension,high_score=high_score):
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

# actual gameplay
add_tile()
add_tile()
while(True):
	clear_screen()
	print_board()
	get_input()
	add_tile()