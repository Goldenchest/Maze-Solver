mazeFile = "sampleMaze2.txt"

# This function reads a maze file, filename, and creates a maze, m.
# Please declare "m" as a list before calling the function and then pass it in. 
def readMaze(m, filename):
  mazeFile = open(filename, "r")
  lines = mazeFile.readlines()
  for line in lines:
    line = line.strip()
    row = [c for c in line]
    m.append(row)

'''
Various helper functions
'''
class StartInexistantError(Exception):
	def warning(self):
		print "Start position does not exist."
def findStart(maze):
	for row in maze:
		if "S" in row: # if S found in maze
			return (maze.index(row), row.index("S"))
	raise StartInexistantError # if S not present in maze

# checks if a position is inside the maze
def inMaze(maze, position):
	width = len(maze[0]) # width is the length of each row
	depth = len(maze) # depth is the number of rows in the maze
	# if position inside the boundaries of the maze:
	return (position[0] >= 0 and position[1] >= 0 and\
			position[0] < depth and position[1] < width)

def mazeAt(maze, position): # return the letter at a position in the maze
	return maze[position[0]][position[1]]
def changeAtPosition(maze, initMarker, finalMarker): # helper function to change the letter at a position
	maze[initMarker[0]][initMarker[1]] = finalMarker
def mark(maze, position): # mark an "X" on positions you've passed
	if mazeAt(maze, position) in ["P","S"]:
		changeAtPosition(maze, position, "X") # change position letter to "X"
def marked(maze, position): # checks if current position has been marked
	return mazeAt(maze, position) == "X"
def onPath(maze, position): # checks if current position is on a valid path
	return mazeAt(maze, position) in ["P","S","F"]
def isFinished(maze, position): # checks if current position is at finish position
	return mazeAt(maze, position) == "F"
	
# function to print maze
def printMaze(maze):
	file = open(mazeFile,'r')
	print file.read()
	file.close()

# function to move to a new position (takes in current position and a direction)
def move(position, direction):
	position = list(position)
	if (direction == "right"):
		position[1] += 1 # move position right
	elif (direction == "left"):
		position[1] -= 1 # move position left
	elif (direction == "up"):
		position[0] -= 1 # move position up
	elif (direction == "down"):
		position[0] += 1 # move position down
	return tuple(position)
'''
mazeSolver() should accept a maze (list of lists) as an input and return True if the maze is solvable, and False otherwise.
'''
def solveMaze(maze, position, path):
	if not inMaze(maze, position): return False # if current position is not inside the maze, return false
	if marked(maze, position): return False # if the current position has already been visited
	if not onPath(maze, position): return False # if current position is not on the path (if it hits a wall)
	if isFinished(maze, position):
		path.append(position) # append position to path
		return True # if at the finish position, return True
	mark(maze, position) # mark the current position
	# call solveMaze for the positions above, below, to the left, and to the right of the current position
	success = (solveMaze(maze, move(position, "up"), path) or solveMaze(maze, move(position, "down"), path) or\
			   solveMaze(maze, move(position, "left"), path) or solveMaze(maze, move(position, "right"), path))
	if success: # if successful path found
		path.append(position) # append position to path (through backtracking)
		return success # if maze solution found, return True. Otherwise, return False
	
m = [] # declares maze as an empty list
	
def mazeSolver(maze):
	maze = [] # maze is initally an empty list
	mazeSolution = [] # list to store path through mass
	readMaze(maze, mazeFile) # read the maze file into maze (constructs the maze)
	shadowMaze = maze[:] # creates a shadow copy of the maze (to edit without changing original maze)
	printMaze(shadowMaze) # print the maze (as a reference)
	try: # if possible:
		startPosition = findStart(maze) # find start position in maze
	except StartInexistantError: # if start position could not be found:
		print "Could not find start position." # output an error message
		return # exit the function
	# if maze is solvable:
	if solveMaze(shadowMaze, findStart(maze), mazeSolution):
		mazeSolution.reverse() # reverse solution list (because positions were appended from finish to start)
		print mazeSolution # print solution list
		return True # return True
	else: # if maze is not solvable:
		print "No solution found."
		return False # return False

mazeSolver(m)
