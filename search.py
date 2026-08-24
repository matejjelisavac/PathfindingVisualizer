import heapq
Coord = tuple[int, int]

class _Snapshot:
	# NOTE: distances/walked/predecessors are the search's live objects, not copies.
	# Reading them mid-iteration (as the visualizer does) is correct; holding onto
	# snapshots is not — every held snapshot shows the final state.

	def __init__(self, current: Coord, distances: dict[Coord, int], walked: set[Coord], predecessors: dict[Coord, Coord]):
		self.current = current
		self.distances = distances
		self.walked = walked
		self.predecessors = predecessors

def trace_path(predecessors: dict[Coord, Coord], end):
	if end not in predecessors:
		return []

	path = []
	curr = end
	while curr is not None:
		path.append(curr)
		curr = predecessors[curr]

	path.reverse()
	return path

def _search(start, end, adjacency_list:dict[Coord,list[Coord]], heuristic):

	current = start
	distances = {start: 0}
	queue = []
	walked = set()
	predecessors = {start: None}

	while True:
		walked.add(current)

		for neighbor in adjacency_list[current]:
			if neighbor in walked:
				continue
			new_dist = distances[current] + 1
			if neighbor not in distances or new_dist < distances[neighbor]:
				distances[neighbor] = new_dist
				# store g, prioritise by f = g + h
				heapq.heappush(queue, (new_dist + heuristic(neighbor), neighbor))
				predecessors[neighbor] = current

		yield _Snapshot(current, distances, walked, predecessors)

		# exit after yielding so the goal frame is emitted
		if current == end or not queue:
			return
		_, current = heapq.heappop(queue)

# Algorithms return path, full _Snapshot generator

def dijkstra(start: Coord, end: Coord, adjacency_list: dict[Coord, list[Coord]]):
	return _search(start, end, adjacency_list, lambda _ : 0)

def astar(start: Coord, end: Coord, adjacency_list: dict[Coord, list[Coord]]):
	return _search(start, end, adjacency_list, lambda node : abs(end[0] - node[0]) + abs(end[1] - node[1]))
