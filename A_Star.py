from math import sqrt
from random import random
from os import system
from time import sleep
from copy import deepcopy

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
		if random() < 0.2:
			self.obstacle = True
			

	def Neighbours(self, grid):
		i = self.i
		j = self.j
		row = len(grid)
		column = len(grid[0])
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



row = 25
column = 25

puzzle = [[' ']*column for i in range(row)]
grid = [[0]*column for i in range(row)]

for i in range(row):
	for j in range(column):
		grid[i][j] = Node(i, j)

grid[0][0].obstacle = False
grid[-1][-1].obstacle = False
for i in range(len(grid)):
	for j in range(len(grid[0])):
		if grid[i][j].obstacle:
			puzzle[i][j] = '|'


for i in range(row):
	for j in range(column):
		if grid[i][j].obstacle == True :
			continue
		grid[i][j].Neighbours(grid)

start  = grid[0][0]
end = grid[row-1][column-1]
visiting = [start]
visited = []
path = []


sol = False


while len(visiting) > 0:
	win = 0
	for i in range(len(visiting)):
		if visiting[i].f < visiting[win].f:
			win = i
	current = visiting[win]		
	visiting.remove(current)
	visited.append(current)


	if current == end:
		path = []
		temp = current 
		path = [temp]
		while temp.parent:
			path.append(temp.parent)
			temp = temp.parent
		for x in path:
			puzzle[x.i][x.j] = '*'
		for i in range(row):
			for j in range(column):
				print(puzzle[i][j], end =' ')
			print()
		print('DONE PATH LENGTH = ' + str(len(path)))
		sol = True
		break


	neighbours = current.neighbours;
	for i in neighbours :
		if i not in visited and not i.obstacle:
			temp = current.g + 1
			newPath = False
			if i in visiting:
				if temp < i.g :
					i.g = temp
					newPath = True
			else :
				i.g = temp
				newPath = True
				visiting.append(i)

			if newPath:
				i.h = heuristic(i, end)
				i.f = i.g + i.h
				i.parent = current


	path = []
	pt = deepcopy(puzzle)
	temp = current 
	path = [temp]
	while temp.parent:
		path.append(temp.parent)
		temp = temp.parent
	for x in path:
		pt[x.i][x.j] = '*'
	for i in range(row):
		for j in range(column):
			print(pt[i][j], end =' ')
		print()
	sleep(0.05)
	system('cls')
	

if not sol :
	for x in path:
		puzzle[x.i][x.j] = '*'
	for i in range(row):
		for j in range(column):
			print(puzzle[i][j], end =' ')
		print()
	print('NO SOLUTION')
input()