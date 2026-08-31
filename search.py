from heapq import heappop, heappush
Coord = tuple[int, int]

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
				heappush(queue, (new_dist + heuristic(neighbor), -new_dist, neighbor))
				predecessors[neighbor] = current

		# exit after yielding so the goal frame is emitted
		if current == end or not queue:
			steps.append(stats)
			return trace_path(predecessors, end), steps
		
		_weight, _tiebreak, current = heappop(queue)
		stats["next"] = current
		steps.append(stats)

# Algorithms return path, full Step generator

def dijkstra(start: Coord, end: Coord, adjacency_list: dict[Coord, set[Coord]]):
	return _search(start, end, adjacency_list, lambda _ : 0)

def astar(start: Coord, end: Coord, adjacency_list: dict[Coord, set[Coord]]):
	return _search(start, end, adjacency_list, lambda node : abs(end[0] - node[0]) + abs(end[1] - node[1]))
