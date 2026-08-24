from math import sqrt as _sqrt
import pygame as _pygame
from search import _Snapshot

Coord = tuple[int, int]

class _Visualizer:
	bg = "White"
	wall = "Black"
	font_color = "Black"

	def __init__(self, adjacency_list, display_size):
		self.adjacency_list = adjacency_list
		self.cell_size = display_size / _sqrt(len(adjacency_list))

		_pygame.init()
		self.sc = _pygame.display.set_mode((display_size, display_size))
		self.clock = _pygame.time.Clock()

	def update(self):
		for event in _pygame.event.get():
			if event.type == _pygame.QUIT:
				_pygame.quit()
		_pygame.display.flip()

	def get_cell(self, coords):
		x,y = coords
		left, top = x * self.cell_size, y * self.cell_size #a coordinate points to top left of the cell
		right, bottom = left + self.cell_size, top + self.cell_size
		return top, left, right, bottom

	def draw_maze(self):
		self.sc.fill(self.bg)
		for coord in self.adjacency_list:
			top, left, right, bottom = self.get_cell(coord)
			neighbors = self.adjacency_list[coord]

			# an unconnected neighbor means a wall on that side
			x, y = coord
			walls = (
				((x, y - 1), (left, top), (right, top)),     #Move up
				((x - 1, y), (left, top), (left, bottom)),   #Move left
				((x + 1, y), (right, top), (right, bottom)),  #Move right
				((x, y + 1), (left, bottom), (right, bottom)),  #Move down
			)

			for neighbor, start, end in walls:
				if neighbor not in neighbors:
					_pygame.draw.line(self.sc, self.wall, start, end)
					
	def fill_cell(self, coords, color):
		top, left, _, _ = self.get_cell(coords)
		_pygame.draw.rect(self.sc, color, (left, top, self.cell_size, self.cell_size))

	def draw_step(self, snapshot: _Snapshot):
		for coord in snapshot.distances:
			self.fill_cell(coord, _pygame.Color(100, min(snapshot.distances[coord], 255), 100))
			# self.draw_distance(coord, snapshot.distances[coord])

	def draw_distance(self, coord, distance):
		top, left, _, _ = self.get_cell(coord)
		font = _pygame.font.SysFont('Comic Sans MS', int(self.cell_size/4))
		text_surface = font.render(str(distance), False, _pygame.Color(self.font_color))
		self.sc.blit(text_surface, (left+self.cell_size/2, top+self.cell_size/2))

def animate(adjacency_list, snapshots, fps=60, display_size=800):
	vis = _Visualizer(adjacency_list, display_size)
	vis.draw_maze()
	vis.update()
	for snapshot in snapshots:
		vis.draw_step(snapshot)
		vis.update()
		vis.clock.tick(fps)

