import time
import sys
if sys.version_info[0] < 3:
	from Tkinter import *
else:
	from tkinter import *


# start tkinter app
top = Tk()
top.title('2048')
# make app size 
top.geometry('560x620')
top.minsize(570, 620)
top.maxsize(570, 620)

for i in range(16):
	j = i
	if j < 6:
		bcolor = '#'+'{0:#0{1}x}'.format(13487565 - 34*j,8)[2:]
	elif j < 12:
		bcolor = '#'+'{0:#0{1}x}'.format(13487395 - 34*(j-5)*256,8)[2:]
	else:
		bcolor = '#'+'{0:#0{1}x}'.format(13435171 - 34*(j-11)*65536,8)[2:]
	canvas = Canvas(top, width=130,height=130, bd=4,bg=bcolor)
	canvas.grid(row=i//4+1, column=i%4+1)
	canvas.create_text(65,65,fill='black',font='Times 24 italic bold', text=str(2**(i+2)))

canvas = Canvas(top, width=130,height=50)
canvas.grid(row=0, column=3)
canvas.create_text(65,25,fill='black',font='Times 12 italic bold', text='score: 4096')

canvas = Canvas(top, width=130,height=50)
canvas.grid(row=0, column=4)
canvas.create_text(65,25,fill='black',font='Times 12 italic bold', text='high score: 114096')

canvas = Canvas(top, width=130,height=50)
canvas.grid(row=0, column=1)
canvas.create_text(65,25,fill='red',font='Times 16 italic bold', text='GAME OVER')

for j in range(6):
	top.grid_rowconfigure(j, weight=1)
	top.grid_columnconfigure(j, weight=1)

arr = []
varr = 'a'
for k in range(1000):
	arr.append(k)
	exec(varr + ' = arr')
	varr = varr+'a'



dim = 100
iterations = 100
for j in range(6):
	tot_tiles = dim**2
	f = dim**2*[1]

	start = time.time()
	for i in range(iterations):
		b = len(f)
		a = 1
		aa = 25
		aaaaaaaaaa = 24
	stop = time.time() - start
	print(stop)

	start = time.time()
	for i in range(iterations):
		b = dim**2
		a = 1
		aa = 25
		aaaaaaaaaa = 24
	stop = time.time() - start
	print(stop)


	start = time.time()
	for i in range(iterations):
		b = tot_tiles
		a = 1
		aa = 25
		aaaaaaaaaa = 24
	stop = time.time() - start
	print(stop)

	start = time.time()
	for i in range(iterations):
		b = dim*dim
		a = 1
		aa = 25
		aaaaaaaaaa = 24
	stop = time.time() - start
	print(stop)
	
	print('\n\n')
	iterations = iterations*10



top.mainloop()
