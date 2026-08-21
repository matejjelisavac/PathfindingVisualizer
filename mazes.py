import random
import pygame
from math import sqrt
import heapdict

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

def dijkstraStep(currentCell:tuple, distances:dict[tuple,int], queue:heapdict.heapdict,
                 walked:set[tuple], predecessors:dict[tuple,tuple],
                 adjacencyList:dict[tuple,list[tuple]]):

	walked.add(currentCell)

	for neighbor in adjacencyList[currentCell]:
		if neighbor in walked:
			continue
		newDist = distances[currentCell] + 1
		if neighbor not in distances or newDist < distances[neighbor]:
			distances[neighbor] = newDist
			queue[neighbor] = newDist
			predecessors[neighbor] = currentCell

	if not queue:
		return None
	nextCell, _ = queue.popitem()
	return nextCell

def getPath(predecessors:dict[tuple,tuple], fromCell:tuple, path:list[tuple] = []):
	if predecessors[fromCell] == None:
		# Found starting cell
		return [*path, fromCell]
	else:
		return getPath(predecessors, predecessors[fromCell], [*path, fromCell])


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

		def backtrackStep(current:tuple, path:list[tuple], visited:set[tuple]):
			neighbors = getCellNeighbors(current, self.size)

			# If all neighbors already visited then backtrack
			if all(neighbor in visited for neighbor in neighbors):
				if path:
					visited.add(current)
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
				visited.add(current)
				path.append(current)
				return next

		start = random.choice(self.coords)
		path = []
		visited = set()

		current = backtrackStep(start, path, visited)
		while path:
			current = backtrackStep(current, path, visited)

		count = 0
		for coord in self.adjacency:
			if len(self.adjacency[coord]) == 1:
				count+=1
				if count >= (1 / self.braid):
					addEdge(self.adjacency, coord, random.choice([neighbor for neighbor in getCellNeighbors(coord, self.size) if neighbor not in self.adjacency[coord]]))
					count = 0

		return self.adjacency


class Visualizer:
	bg = "White"
	wall = (63, 22, 81)
	fontColor = "Black"

	def __init__(self, displaySize, mazeSize):

		self.mazeSize = mazeSize
		self.displaySize = displaySize
		self.cellSize = self.displaySize / self.mazeSize

		pygame.init()
		self.sc = pygame.display.set_mode((displaySize, displaySize))
		self.clock = pygame.time.Clock()
	
	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		pygame.display.flip()

	def getCellInfo(self, coords):
		x,y = coords
		left, top = x * self.cellSize, y * self.cellSize #a coordinate points to top left of the cell
		right, bottom = left + self.cellSize, top + self.cellSize
		return top, left, right, bottom

	def drawWalls(self, coords, adjacencyList):
		top, left, right, bottom = self.getCellInfo(coords)
		neighbors = adjacencyList[coords]

		# an unconnected neighbor means a wall on that side
		x, y = coords
		walls = (
			((x, y - 1), (left, top),    (right, top)),     #Move up
			((x - 1, y), (left, top),    (left, bottom)),   #Move left
			((x + 1, y), (right, top),   (right, bottom)),  #Move right
			((x, y + 1), (left, bottom), (right, bottom)),  #Move down
		)
		for neighbor, start, end in walls:
			if neighbor not in neighbors:
				pygame.draw.line(self.sc, self.wall, start, end)


	def fillCell(self, coords, color):
		top, left, _, _ = self.getCellInfo(coords)
		pygame.draw.rect(self.sc, color, (left, top, self.cellSize, self.cellSize))

	def drawDistance(self, coords, distance):
		top, left, _, _ = self.getCellInfo(coords)
		font = pygame.font.SysFont('Comic Sans MS', int(self.displaySize/100))
		text_surface = font.render(str(distance), False, pygame.Color(self.fontColor))
		self.sc.blit(text_surface, (left+self.cellSize/2, top+self.cellSize/2))


mazeSize = 50

maze = Maze().setBraid(0.2).setSize(mazeSize).generate()
game = Visualizer(800, mazeSize)
cell = (0,0)
end = (mazeSize-1,mazeSize-1)
distances, queue, walked, predecessors = {cell:0}, heapdict.heapdict(), set(), {cell:None}



while True:
	while cell != end:
		game.sc.fill(game.bg)
		cell = dijkstraStep(cell, distances, queue, walked, predecessors, maze)
		for coord in predecessors:
			game.fillCell(coord, pygame.Color(100,min(distances[coord], 255), 100))
			# game.drawDistance(coord, distances[coord])
		for coord in maze:
			game.drawWalls(coord, maze)
		game.update()
		# game.clock.tick(60)

	for coord in getPath(predecessors, end):
		game.fillCell(coord, "Orange")
	game.update()

	

# WIP

# filled = set()
# while True:
# 	game.sc.fill(game.bg)
# 	for coord in maze:
# 		game.drawWalls(coord, maze)
# 	while cell != end:
# 		cell = dijkstraStep(cell, distances, queue, walked, predecessors, maze)
# 		tofill = [coord for coord in predecessors if coord not in filled]
# 		for coord in tofill:
# 			game.fillCell(coord, pygame.Color(100,int(distances[coord]/2),100))
# 			filled.add(coord)
# 			# game.drawDistance(coord, distances[coord])
# 		game.update()
# 		game.clock.tick(60)

# 	for coord in getPath(predecessors, end):
# 		game.fillCell(coord, "Orange")

# 	game.update()
# 	game.clock.tick(60)