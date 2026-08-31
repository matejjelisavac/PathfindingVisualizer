from math import sqrt as _sqrt
import pygame as _pygame

Coord = tuple[int, int]

class Visualizer:
	bg = "White"
	wall = "Black"
	font_color = "Black"

	def __init__(self, adjacency_list, display_size=800, fps=60):
		self.adjacency_list = adjacency_list
		self.cell_size = round(display_size / _sqrt(len(adjacency_list)))

		_pygame.init()
		self.sc = _pygame.display.set_mode((display_size, display_size))
		self.fps = fps
		self._clock = _pygame.time.Clock()

	def _update(self):
		for event in _pygame.event.get():
			if event.type == _pygame.QUIT:
				_pygame.quit()
		_pygame.display.flip()
		self._clock.tick(self.fps)

	def _get_cell(self, coords):
		x,y = coords
		left, top = x * self.cell_size, y * self.cell_size #a coordinate points to top left of the cell
		right, bottom = left + self.cell_size, top + self.cell_size
		return top, left, right, bottom

	def draw_maze(self):
		self.sc.fill(self.bg)
		for coord in self.adjacency_list:
			top, left, right, bottom = self._get_cell(coord)
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
		self._update()
					
	def fill_cells(self, coords: list[Coord], color):
		for coord in coords:
			top, left, _, _ = self._get_cell(coord)
			_pygame.draw.rect(self.sc, color, (left, top, self.cell_size, self.cell_size))
		self._update()

	def sleep(self, ms):
		start = _pygame.time.get_ticks()
		while _pygame.time.get_ticks() - start < ms:
			self._update()


	# def draw_distance(self, coord, distance):
	# 	top, left, _, _ = self._get_cell(coord)
	# 	font = _pygame.font.SysFont('Comic Sans MS', int(self.cell_size/4))
	# 	text_surface = font.render(str(distance), False, _pygame.Color(self.font_color))
	# 	self.sc.blit(text_surface, (left+self.cell_size/2, top+self.cell_size/2))

	
