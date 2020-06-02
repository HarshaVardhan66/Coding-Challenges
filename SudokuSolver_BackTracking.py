from tkinter import *
from copy import deepcopy

x = 400/9
y = 400/9

def nextEmpty(b):
	for i in range(9):
		if ' ' in b[i]:
			return (i, b[i].index(' '))
	return None


def isvalid(b, num, pos):
	if num in b[pos[0]]:
		return False
	if num in  [b[i][pos[1]] for i in range(9)]:
		return False

	x = pos[0] // 3
	y = pos[1] // 3

	for i in range(x*3, x*3+3):
		for j in range(y*3, y*3+3) :
			if num == b[i][j]:
				return False
	return True


def solve(b, b1):
	position = nextEmpty(b)
	if not position:
		draw_sudoku(b, b1, x, y)
		print('Solved')
		return True
	
	for i in range(1, 10):
		if isvalid(b, i, position):
			s = position[0]
			t = position[1]
			b[s][t] = i
			if solve(b, b1):
				return True
			b[s][t] = ' '
	return False


def draw_sudoku(b, b1, x, y):
	r1 = Tk()
	r1.resizable(False, False)
	c = Canvas(r1, height=400, width=400)
	c.pack()
	for i in range(9):
		for j in range(9):
			x1 = i*x+2
			y1 = j *y+2
			x2 = x1 + x
			y2 = y1 + y
			if b1[j][i]!= ' ':
				c.create_rectangle(x1, y1, x2, y2, fill='lightblue', width=2)
				c.create_text((x1+x2)/2, (y1+y2)/2, text=str(b[j][i]), font=("Helvetica", "18", "bold"))
			else :
				c.create_rectangle(x1, y1, x2, y2, width=2)
				c.create_text((x1+x2)/2, (y1+y2)/2, text=str(b[j][i]), font=("Helvetica", "18"))
	r1.mainloop()


def start(num):
	sudoku = [ ['']*9 for i in range(9) ]
	for i in range(9):
		for j in range(9):
		    s = num[i][j].get()
		    if s == "":
		        sudoku[i][j] = ' '
		    else:
		        sudoku[i][j] = int(s)
	default = deepcopy(sudoku)
	if solve(sudoku, default):
		print('Solved')
	else :
		print('Not Solvable')


def initiate():
	root = Tk()
	root.resizable(False, False)
	canvas = Canvas(root, width=400, height=450)
	canvas.pack()
	num = [['']*9 for i in range(9)]
	for i in range(9):
		for j in range(9):
			x1 = i * x+5
			y1 = j * y+5
			x2 = x1 + x
			y2 = y1 + y
			num[j][i] = StringVar()
			e = Entry (root, width=3, textvariable=num[j][i], bg='lightblue', justify="center", font=("Helvetica", "15", "bold"))
			e.place(x=x1, y=y1)

	submit = Button(canvas, text='Solve', command=lambda:start(num))
	submit.place(x = 180, y=410)

	root.mainloop()


initiate()
input()
 
