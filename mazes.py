import random
import pygame
from math import sqrt

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
		return self

	def generate(self):

		# start = (random.randint(0,self.size-1),random.randint(0,self.size-1))
		self.coords = [(x,y) for x in range(self.size) for y in range(self.size)]
		self.adjacency = {coord:[] for coord in self.coords}

		def getCellNeighbors(coords):

			x = coords[0]
			y = coords[1]

			# possibilities = [
			# 	(x, y - 1) if y - 1 >= 0 #Move up
			# 	(x - 1, y) if x - 1 >= 0 #Move left
			# 	(x+1,y) if x + 1 <= self.size - 1 #Move right
			# 	(x, y+1) if y + 1 <= self.size - 1 #Move down
			# ]
			possibilities = [
				(x, y - 1), #Move up
				(x - 1, y), #Move left
				(x+1,y),  #Move right
				(x, y+1),  #Move down
			]

			neighbors = [(x,y) for x,y in possibilities if 0 <= x <= self.size-1 and 0 <= y <= self.size-1 ]

			return neighbors

		def addEdge(cellFrom: tuple, cellTo:tuple):
			print(cellTo)
			self.adjacency[cellFrom].append(cellTo)
			self.adjacency[cellTo].append(cellFrom)

		def backtrackStep(current:tuple, path:list[tuple], visited:list[tuple]):
			neighbors = getCellNeighbors(current)

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
				addEdge(current, next)
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
			if self.adjacency[coord].length == 1:
				count+=1
				if count == 1/braid:
					addEdge(coord, random.choice(getCellNeighbors(coord)))

		return self.adjacency


Maze().setBraid(0.5).setSize(4).generate()


class Visualizer:
	bg = pygame.Color("white")
	wall = (63, 22, 81)

	def __init__(self, displaySize, adjacencyList):

		self.adjacency = adjacencyList
		self.size = sqrt(len(self.adjacency))
		self.displaySize = displaySize

		pygame.init()
		sc = pygame.display.set_mode((displaySize, displaySize))
		clock = pygame.time.Clock()
	
	def update():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		pygame.display.flip()

	def drawCell(self, coords):
		cellSize = self.displaySize / self.size
		cellPos = coords * cellSize #a coordinate points to top left of the cell
		cellPos + cellSize
		# ...
