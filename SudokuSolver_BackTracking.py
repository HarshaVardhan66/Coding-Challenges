b = [	 [5, 3, 0, 0, 7, 0, 0, 0, 0],
		 [6, 0, 0, 1, 9, 5, 0, 0, 0],
		 [0, 9, 8, 0, 0, 0, 0, 6, 0],
		 [8, 0, 0, 0, 6, 0, 0, 0, 3],
		 [4, 0, 0, 8, 0, 3, 0, 0, 1],
		 [7, 0, 0, 0, 2, 0, 0, 0, 6],
		 [0, 6, 0, 0, 0, 0, 2, 8, 0],
		 [0, 0, 0, 4, 1, 9, 0, 0, 5],
		 [0, 0, 0, 0, 8, 0, 0, 7, 9]     ]


def find_empty(b):
	for i in range(9):
		if 0 in b[i]:
			return (i, b[i].index(0))
	return None


def valid(b, num, pos):
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


def solve(b):
	find = find_empty(b)
	if not find:
		return True
	
	for i in range(1, 10):
		if valid(b, i, find):
			b[find[0]][find[1]] = i 
			if solve(b):
				return True
			b[find[0]][find[1]] = 0
	return False


solve(b)
for i in range(0, 9):
	print(b[i])

input()
