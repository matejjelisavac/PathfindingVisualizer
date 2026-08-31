Coord = tuple[int, int]

class GridGraph:
	width: int
	height: int
	adjacency_list: dict[Coord, set[Coord]]


	def __init__(self, width, height, adjacency_list):
		self.width, self.height, self.adjacency_list = width, height, adjacency_list

	@classmethod
	def empty(cls, width, height):
		nodes = [(x, y) for x in range(width) for y in range(height)]
		return cls(width, height, {n: set() for n in nodes})

	def add_edge(self, a, b):
		# sets make a repeated edge a no-op rather than a duplicate
		self.adjacency_list[a].add(b)
		self.adjacency_list[b].add(a)

	def grid_neighbors(self, node):   # adjacent in space — what generators consider
		x, y = node
		return [(nx, ny) for nx, ny in ((x, y-1), (x-1, y), (x+1, y), (x, y+1))
				if 0 <= nx < self.width and 0 <= ny < self.height]