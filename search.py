import heapq
import maze
Coord = tuple[int, int]

class Step:
	current: Coord
	distances:dict[Coord,int]
	queue:list[tuple[float, Coord]]
	walked:set[tuple]
	predecessors:dict[Coord,Coord]

	def __init__(self, start):
		self.current = start
		self.distances = {start:0}
		self.queue = []
		self.walked = set()
		self.predecessors = {start: None}
		pass

def trace_path(predecessors: dict[Coord, Coord], end):
	path = []
	curr = end
	while predecessors[curr]:
		path.insert(0,curr)
		curr = predecessors[curr]
	return list(path)

	

def search_step(step:Step, adjacency_list:dict[Coord,list[Coord]], heuristic):

		step.walked.add(step.current)

		for neighbor in adjacency_list[step.current]:
			if neighbor in step.walked:
				continue
			new_dist = step.distances[step.current] + 1 + heuristic(step.current)
			if neighbor not in step.distances or new_dist < step.distances[neighbor]:
				step.distances[neighbor] = new_dist
				heapq.heappush(step.queue, (new_dist, neighbor))
				step.predecessors[neighbor] = step.current

		if not step.queue:
			return None
		_, next_cell = heapq.heappop(step.queue)
		step.current = next_cell
		return step

def dijkstra_step(step:Step, adjacency_list:dict[Coord,list[Coord]]):
	return search_step(step, adjacency_list, lambda n : 0)

def astar_step(step:Step, adjacency_list:dict[Coord,list[Coord]], end: Coord):
	return search_step(step, adjacency_list, lambda n : abs(end[0] - step.current[0]) + abs(end[1] - step.current[1]))

def dijkstra(start: Coord, end: Coord, adjacency_list: dict[Coord, list[Coord]]):
	step = Step(start)
	while step.current != end:
		step = dijkstra_step(step, adjacency_list)
	return trace_path(step.predecessors, end)

def astar(start: Coord, end: Coord, adjacency_list: dict[Coord, list[Coord]]):
	step = Step(start)
	while step.current != end:
		step = astar_step(step, adjacency_list, end)
	return trace_path(step.predecessors, end)


adjacency_list = maze.recursive_backtracker(20,20)
print(astar((0,0), (19,19), adjacency_list))