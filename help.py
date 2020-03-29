def left(i,j):
	return i*dimension + j

def right(i,j):
	return (i + 1)*dimension - j - 1

def up(i,j):
	return j*dimension + i

def down(i,j):
	return (dimension - j - 1)*dimension + i

def move(board,direction):
	for j in range(dimension):
		def f(x): return direction(j,x)
		non_zero = collect_tiles(board,f)
		match_tiles(board,non_zero,f)

def collect_tiles(board,f):
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
	return non_zero

def match_tiles(board,non_zero,f):
	i = 0
	pad = 0
	while i < non_zero-1:
		if board[f(i)] == board[f(i+1)]:
			board[f(i-pad)] = board[f(i)]*2
			pad+=1
			i+=1
		else:
			board[f(i-pad)] = board[f(i)]
		i+=1
	if i < non_zero:
		board[f(i-pad)] = board[f(i)]
	for i in range(non_zero-pad,non_zero):
		board[f(i)] = 0

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

dimension = 4
board = 16*[2]
move(board,down)
print_board(board)

