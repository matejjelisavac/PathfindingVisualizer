import random
import pygame
from math import sqrt
import heapdict
import maze

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


mazeSize = 20

mz = maze.recursive_backtracker(mazeSize,mazeSize)
game = Visualizer(800, mazeSize)
cell = (0,0)
end = (mazeSize-1,mazeSize-1)


while True:
	while cell != end:
		game.sc.fill(game.bg)
		cell = dijkstraStep(cell, distances, queue, walked, predecessors, mz)
		for coord in predecessors:
			game.fillCell(coord, pygame.Color(100,min(distances[coord], 255), 100))
			# game.drawDistance(coord, distances[coord])
		for coord in mz:
			game.drawWalls(coord, mz)
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