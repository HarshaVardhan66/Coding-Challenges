from math import sqrt
from random import random
from os import system
from time import sleep
from copy import deepcopy
from tkinter import *
import tkinter.messagebox

class Node() :
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.f = 0
		self.g = 0
		self.h = 0
		self.parent = None
		self.neighbours = []
		self.obstacle = False
			
	def show(self, canvas, color):
		x1 = self.j*x+2
		y1 = self.i*y+2
		temp = canvas.create_rectangle(x1 , y1, x1+x, y1+y, fill=color)
		return temp


	def Neighbours(self, grid):
		global row, column
		i = self.i
		j = self.j
		if i < row - 1  and not grid[i+1][j].obstacle:
			self.neighbours.append(grid[i+1][j])

		if i > 0 and not grid[i-1][j].obstacle:
			self.neighbours.append(grid[i-1][j])

		if j < column-1 and not grid[i][j+1].obstacle :
			self.neighbours.append(grid[i][j+1])

		if j > 0 and not grid[i][j-1].obstacle:
			self.neighbours.append(grid[i][j-1])

		if i > 0 and j > 0  and not grid[i-1][j-1].obstacle:
			if not grid[i-1][j].obstacle or not grid[i][j-1].obstacle:
				self.neighbours.append(grid[i-1][j-1])

		if i < row-1 and j > 0 and not grid[i+1][j-1].obstacle:
			if not grid[i+1][j].obstacle or not grid[i][j-1].obstacle:
				self.neighbours.append(grid[i+1][j-1])

		if i > 0 and j < column-1 and not grid[i-1][j+1].obstacle:
			if not grid[i-1][j].obstacle or not grid[i][j+1].obstacle:
				self.neighbours.append(grid[i-1][j+1])

		if i < row-1 and j < column-1 and not grid[i+1][j+1].obstacle:
			if not grid[i+1][j].obstacle or not grid[i][j+1].obstacle:
				self.neighbours.append(grid[i+1][j+1])

def heuristic(a, b):
	return abs(a.i - b.i) + abs(a.j - b.j) 


def start_solve(root, canvas):
	if points==0 :
		tkinter.messagebox.showerror(title='Error', message='Enter Values')
		return
	global path, start, end
	create_maze()
	

	openSet = [start]
	closedSet = []

	sol = False


	while len(openSet) > 0:
		win = 0
		for i in range(len(openSet)):
			if openSet[i].f < openSet[win].f:
				win = i
		current = openSet[win]		
		openSet.remove(current)
		closedSet.append(current)

		
		if current == end:
			temp = current 
			path = [temp]
			while temp.parent:
				path.append(temp.parent)
				temp = temp.parent
			d = draw_path(path, canvas)		
			sol = True
			break


		neighbours = current.neighbours

		for i in neighbours :
			if i not in closedSet and not i.obstacle:
				temp = current.g + 1
				newPath = False
				if i in openSet:
					if temp < i.g :
						i.g = temp
						newPath = True
				else :
					i.g = temp
					newPath = True
					openSet.append(i)

				if newPath:
					i.h = heuristic(i, end)
					i.f = i.g + i.h
					i.parent = current
		temp = current 
		path = [temp]
		while temp.parent:
			path.append(temp.parent)
			temp = temp.parent
		d = draw_path(path, canvas)
		sleep(0.1)
		canvas.update()
		for h in range(len(path)):
			canvas.delete(d[h])
	canvas.unbind('<B1-Motion>')
	if sol :
		tkinter.messagebox.showinfo(title='Solved', message='Total Path Length : '+str(len(path) ))
		skip_button = Button(canvas, text='Exit   ', command=root.destroy)
		skip_button.place(x=180, y=460)
	else :
		tkinter.messagebox.showinfo(title='Invalid Maze', message='No Solution Found' )


def draw_path(path, canvas):
	d = ['']*len(path)
	for h in range(len(path)):
		if path[h] == start or path[h] == end :
			d[h] = path[h].show(canvas, 'red')
		else :
			d[h] = path[h].show(canvas, 'green2')
	return d



def create_maze():
	global row, column
	for i in range(row):
		for j in range(column):
			if walls[i][j] == 1 :
				grid[i][j].obstacle=True
	for i in range(row):
		for j in range(column):
			if grid[i][j].obstacle == True :
				continue
			grid[i][j].Neighbours(grid)

	
def draw_maze(event, canvas):
	global points
	if points!=2 :
		tkinter.messagebox.showerror(title='Error', message='Determine Starting and Ending Points')
		return
	i, j = event.x, event.y
	i, j = (i//x)*x + 2, (j//y)*y+ 2
	i1 = int((i-2)//x)
	j1 = int((j-2)//y)
	if i<402 and j<402  :
		if grid[j1][i1]==start or grid[j1][i1]==end :
			return
		canvas.create_rectangle(i, j , i+x, j+y, fill='black')
		walls[j1][i1] = 1


def set_start_and_end(event, canvas) :
	global points, start, end
	i, j = event.x, event.y
	i1, j1 = (i//x)*x + 2, (j//y)*y+ 2
	i = int((i1-2)//x)
	j = int((j1-2)//y)
	if i1<402 and j1<402  :
		if points == 0 :
			start = grid[j][i]
			canvas.create_rectangle(i1, j1 , i1+x, j1+y, fill='red')
			points = points+1
		elif points == 1:
			canvas.create_rectangle(i1, j1 , i1+x, j1+y, fill='red')
			end = grid[j][i]
			points = points+1
		else :
			canvas.unbind('<Button-3>')


row = 25
column = 25
points = 0
start = None
end = None
root = None
canvas = None
x = 400/row
y = 400/column
path = None



def main():
	global points, start, end, path, grid, walls
	points = 0
	root = Tk()
	root.resizable(False, False)
	canvas = Canvas(root, width=402, height=500)
	grid = [['']*column for i in range(row)]
	walls = [[' ']*column for i in range(row)]
	for i in range(row):
		for j in range(column):
			grid[i][j] = Node(i, j)
	canvas.pack()
	for j in range(row):
		for i in range(column):
			x1 = x * i+2
			y1 = y * j+2
			x2 = x1 + x
			y2 = y1 + y
			canvas.create_rectangle(x1, y1, x2, y2)

	canvas.bind('<Button-3>', lambda event, canvas=canvas:set_start_and_end(event, canvas))
	canvas.bind('<B1-Motion>', lambda event, canvas=canvas:draw_maze(event, canvas))

	label1 = Label(canvas, text='Step 1) Mouse Left click to set starting and ending points', font=("Helvetica", "10"))
	label1.place(x=50, y=405)
	label2 = Label(canvas, text='Step 2) Hold and drag with mouse right click to draw maze', font=("Helvetica", "10"))
	label2.place(x=50, y=425)

	next_button = Button(canvas, text='Solve', command=lambda:start_solve(root, canvas))
	next_button.place(x=180, y=460)

	root.mainloop()

retry = True
while retry:
	main()
	r1= Tk()
	r1.withdraw()
	MsgBox = tkinter.messagebox.askquestion(title='Retry', message='Do you want to try again ?')
	if MsgBox == 'no':
		retry = False
