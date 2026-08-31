import os as _os

# pygame greets stdout on import unless this exists; it checks for the name, not a value
_os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame as _pygame

Coord = tuple[int, int]
RGBValue = tuple[int,int,int]

class Visualizer:
	bg = "White"
	wall = "Black"
	font_color = "Black"

	def __init__(self, adjacency_list, display_size=800, fps=60):
		self.adjacency_list = adjacency_list
		self.width  = max(x for x, _ in adjacency_list) + 1
		self.height = max(y for _, y in adjacency_list) + 1
		self.cell_size = round(display_size / max(self.width, self.height))

		_pygame.init()
		self.sc = _pygame.display.set_mode(
			(self.width * self.cell_size, self.height * self.cell_size))
		self.fps = fps
		self._clock = _pygame.time.Clock()
		self._font = _pygame.font.SysFont('Comic Sans MS', max(1, self.cell_size // 4))
		# walls live on their own transparent layer so fills can't cover them
		self._wall_surface = _pygame.Surface(self.sc.get_size(), _pygame.SRCALPHA)

	# Drawing only writes to the surface; call present() to show a finished
	# frame, so any number of draw calls can make up one frame.
	def present(self):
		for event in _pygame.event.get():
			if event.type == _pygame.QUIT:
				_pygame.quit()
				raise SystemExit
		self.sc.blit(self._wall_surface, (0, 0))
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
					_pygame.draw.line(self._wall_surface, self.wall, start, end)

	def fill_cell(self, coord: Coord, color: str | RGBValue):
		top, left, _, _ = self._get_cell(coord)
		_pygame.draw.rect(self.sc, color, (left, top, self.cell_size, self.cell_size))

	def draw_number(self, coord: Coord, number):
		top, left, _, _ = self._get_cell(coord)
		text_surface = self._font.render(str(number), False, _pygame.Color(self.font_color))
		self.sc.blit(text_surface, (left+self.cell_size/2, top+self.cell_size/2))

	def sleep(self, ms):
		# holds the last presented frame, staying responsive to window events
		start = _pygame.time.get_ticks()
		while _pygame.time.get_ticks() - start < ms:
			self.present()
