import random
import pygame
from math import sqrt
import heapq

def getCellNeighbors(cell: tuple, mazeSize: int):

	x = cell[0]
	y = cell[1]

	possibilities = [
		(x, y - 1), #Move up
		(x - 1, y), #Move left
		(x+1,y),  #Move right
		(x, y+1),  #Move down
	]

	neighbors = [(x,y) for x,y in possibilities if 0 <= x <= mazeSize-1 and 0 <= y <= mazeSize-1 ]

	return neighbors

def addEdge(adjacencyList: dict[tuple, list[tuple]], cellFrom: tuple, cellTo:tuple):
	adjacencyList[cellFrom].append(cellTo)
	adjacencyList[cellTo].append(cellFrom)

class Maze:

	size = None # Maze becomes sizexsize
	braid = None # 0->1. % of dead ends culled.
	distances = False

	def __init__(self):
		pass

	def setSize(self, size):
		self.size = size
		return self

	def setBraid(self, braid):
		if braid > 1 or braid <- 0:
			raise ValueError(braid + " out of range 0 to 1")
		self.braid = braid
		return self

	def showDistances(self):
		self.distances = True
		return self

	def hideDistances(self):
		self.distances = False

	def generate(self):

		if not self.braid or not self.size:
			raise SyntaxError("Cannot run if missing size or braid values.")

		# start = (random.randint(0,self.size-1),random.randint(0,self.size-1))
		self.coords = [(x,y) for x in range(self.size) for y in range(self.size)]
		self.adjacency = {coord:[] for coord in self.coords}

		def backtrackStep(current:tuple, path:list[tuple], visited:list[tuple]):
			neighbors = getCellNeighbors(current, self.size)

			# If all neighbors already visited then backtrack
			if all(neighbor in visited for neighbor in neighbors):
				if path:
					visited.append(current)
					return path.pop()
				# If path is empty then we are finished
				else: 
					return 

			# Otherwise, if at least 1 neighbor not visited
			else:
				next = random.choice(neighbors)
				while next in visited:
					next = random.choice(neighbors)
				addEdge(self.adjacency, current, next)
				visited.append(current)
				path.append(current)
				return next

		start = random.choice(self.coords)
		path = []
		visited = []

		current = backtrackStep(start, path, visited)
		while path:
			current = backtrackStep(current, path, visited)

		count = 0
		for coord in self.adjacency:
			if len(self.adjacency[coord]) == 1:
				count+=1
				if count == 1 / self.braid:
					addEdge(self.adjacency, coord, random.choice(getCellNeighbors(coord, self.size)))

		return self.adjacency


class Visualizer:
	bg = pygame.Color("white")
	wall = (63, 22, 81)

	def __init__(self, displaySize, mazeSize):

		self.mazeSize = mazeSize
		self.displaySize = displaySize

		pygame.init()
		self.sc = pygame.display.set_mode((displaySize, displaySize))
		self.clock = pygame.time.Clock()
	
	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		pygame.display.flip()

	def draw(self, coords, adjacencyList):
		cellSize = self.displaySize / self.mazeSize
		x, y = coords
		left, top = x * cellSize, y * cellSize #a coordinate points to top left of the cell
		right, bottom = left + cellSize, top + cellSize
		neighbors = adjacencyList[coords]

		# an unconnected neighbor means a wall on that side
		walls = (
			((x, y - 1), (left, top),    (right, top)),     #Move up
			((x - 1, y), (left, top),    (left, bottom)),   #Move left
			((x + 1, y), (right, top),   (right, bottom)),  #Move right
			((x, y + 1), (left, bottom), (right, bottom)),  #Move down
		)
		for neighbor, start, end in walls:
			if neighbor not in neighbors:
				pygame.draw.line(self.sc, self.wall, start, end)


maze = Maze().setBraid(0.5).setSize(20).generate()
game = Visualizer(200, 20)
while True:
	game.sc.fill(game.bg)
	for coord in maze:
		game.draw(coord, maze)
	game.update()
	game.clock.tick(60)

