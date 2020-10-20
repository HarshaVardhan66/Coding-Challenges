from tkinter import *
from time import sleep
from copy import deepcopy

x = 400/9
y = 400/9
time = 0.2
colors = [['0']*3+['1']*3+['0']*3]*3+[['1']*3+['0']*3+['1']*3]*3+[['0']*3+['1']*3+['0']*3]*3
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
		return True
	
	for i in range(1, 10):
		if isvalid(b, i, position):
			s = position[0]
			t = position[1]
			b[s][t] = i
			x1 = t*x+2
			y1 = s*y+2
			x2 = x1 + x
			y2 = y1 + y
			sleep(time)
			rect1 = c.create_rectangle(x1, y1, x2, y2, width=4, outline='green2')
			d = c.create_text((x1+x2)/2, (y1+y2)/2, text=str(b[s][t]), font=("Helvetica", "18"))
			
			c.update()
			c.delete(rect1)
			if solve(b, b1):
				return True
			b[s][t] = ' '
			
			rect2 = c.create_rectangle(x1+x, y1, x2+x, y2, width=4, outline='red')
			if i < 9:
				r = c.create_text((x1+x2+x+x)/2, (y1+y2)/2, text=str(i+1), font=("Helvetica", "18"))
			else :
				r = c.create_text((x1+x2+x+x)/2, (y1+y2)/2, text=str(1), font=("Helvetica", "18"))
			sleep(time)
			c.update()
			c.delete(rect2)
			c.delete(d)
			c.delete(r)
	return False





def prepare_puzzle(num, root, skip_button):
	global time
	for i in range(9):
		for j in range(9):
		    s = num[i][j].get()
		    if s == "":
		        b[i][j] = ' '
		    else:
		        b[i][j] = int(s)
	if skip_button.get() == 1 :
		time = 0
	else:
		time = 0.3
	print(skip_button.get())

	root.destroy()
	


def initialization():
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
			if colors[j][i] == '0' :
				e = Entry (root, width=3, textvariable=num[j][i], bg='lightblue', justify="center", font=("Helvetica", "15", "bold"))
			else :
				e = Entry (root, width=3, textvariable=num[j][i], bg='blanchedalmond', justify="center", font=("Helvetica", "15", "bold"))
			e.place(x=x1, y=y1)
	skip_button = IntVar()
	Checkbutton(root, text="Skip showing steps", variable=skip_button).place(x = 150, y=402)
	submit = Button(canvas, text='Solve', command=lambda:prepare_puzzle(num, root, skip_button))
	submit.place(x=180, y=420)

	root.mainloop()


b = [ ['']*9 for i in range(9) ]

initialization()

b1 = deepcopy(b) 
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
		if colors[j][i] == '0' :
			c.create_rectangle(x1, y1, x2, y2, fill='lightblue', width=2)
		else:
			c.create_rectangle(x1, y1, x2, y2, fill='antiquewhite', width=2)
		if b1[j][i]!= ' ':
			c.create_text((x1+x2)/2, (y1+y2)/2, text=str(b[j][i]), font=("Helvetica", "20", "bold"))
		else :
			c.create_text((x1+x2)/2, (y1+y2)/2, text=str(b[j][i]), font=("Helvetica", "18"))

c.create_line(4,0,4,400, width=4)
c.create_line(x*3,0,x*3,400, width=4)
c.create_line(x*6,0,x*6,400, width=4)
c.create_line(x*9,0,x*9,400, width=4)

c.create_line(0, 4, 400, 4, width=4)
c.create_line(0, y*3, 400, y*3, width=4)
c.create_line(0, y*6, 400, y*6, width=4)
c.create_line(0, y*9, 400, y*9, width=4)

if solve(b, b1):
	print('Solved')
else :
	print('Not Solvable')
r1.mainloop()


input()
