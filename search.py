import heapq
import copy
Coord = tuple[int, int]

# class Step:
# 	# NOTE: distances/walked/predecessors are the search's live objects, not copies.
# 	# Reading them mid-iteration (as the visualizer does) is correct; holding onto
# 	# snapshots is not — every held snapshot shows the final state.

# 	def __init__(self, current: Coord, distances: dict[Coord, int], walked: set[Coord], predecessors: dict[Coord, Coord]):
# 		self.current = current
# 		self.distances = distances
# 		self.walked = walked
# 		self.predecessors = predecessors

def trace_path(predecessors: dict[Coord, Coord], end):
	if end not in predecessors:
		return []

	path = list[Coord]()
	curr = end
	while curr is not None:
		path.append(curr)
		curr = predecessors[curr]

	path.reverse()
	return path

def _search(start: Coord, end: Coord, adjacency_list:dict[Coord,set[Coord]], heuristic):

	current = start
	distances = dict[Coord, int]({start: 0})
	queue = []
	walked = set[Coord]()
	predecessors = {start: None}

	steps = []
	
	while True:

		stats = {
		   "current":current, 
		   "next":None,
		   "visited":[], 
		   "elapsed":0
		   }

		walked.add(current)
		for neighbor in adjacency_list[current]:
			if neighbor in walked:
				continue
			new_dist = distances[current] + 1
			if neighbor not in distances or new_dist < distances[neighbor]:
				stats["visited"].append(neighbor)
				distances[neighbor] = new_dist
				# store g, prioritise by f = g + h
				heapq.heappush(queue, (new_dist + heuristic(neighbor), -new_dist, neighbor))
				predecessors[neighbor] = current

		# stats["queue"] = copy.deepcopy(queue)

		# exit after yielding so the goal frame is emitted
		if current == end or not queue:
			steps.append(stats)
			return trace_path(predecessors, end), steps
		
		weight, tiebreak, current = heapq.heappop(queue)
		stats["next"] = current
		steps.append(stats)

# Algorithms return path, full Step generator

def dijkstra(start: Coord, end: Coord, adjacency_list: dict[Coord, set[Coord]]):
	return _search(start, end, adjacency_list, lambda _ : 0)

def astar(start: Coord, end: Coord, adjacency_list: dict[Coord, set[Coord]]):
	return _search(start, end, adjacency_list, lambda node : abs(end[0] - node[0]) + abs(end[1] - node[1]))
