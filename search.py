from collections import deque
from heapq import heappop, heappush
from typing import NamedTuple
from collections.abc import Callable

Coord = tuple[int, int]
AdjacencyList = dict[Coord, set[Coord]]


class Step(NamedTuple):
	current: Coord
	discovered: list[Coord]                   # only this step's, freshly built
	distances: dict[Coord, int]               # the search's own dicts, shared by
	predecessors: dict[Coord, Coord | None]   # every step and mutated as it runs


def trace_path(predecessors: dict[Coord, Coord | None], end: Coord) -> list[Coord]:
	if end not in predecessors:
		return []

	path = list[Coord]()
	curr = end
	while curr is not None:
		path.append(curr)
		curr = predecessors[curr]

	path.reverse()
	return path


def _search(start: Coord, end: Coord, adjacency_list: AdjacencyList, heuristic: Callable[[Coord], float]):

	current = start
	distances = dict[Coord, int]({start: 0})
	queue = []
	walked = set[Coord]()
	predecessors = {start: None}

	while True:

		discovered = list[Coord]()

		walked.add(current)
		for neighbor in adjacency_list[current]:
			if neighbor in walked:
				continue
			new_dist = distances[current] + 1
			if neighbor not in distances or new_dist < distances[neighbor]:
				discovered.append(neighbor)
				distances[neighbor] = new_dist
				# store g, prioritise by f = g + h
				heappush(queue, (new_dist + heuristic(neighbor), -new_dist, neighbor))
				predecessors[neighbor] = current

		# yield before exiting so the goal expansion is the final frame
		yield Step(current, discovered, distances, predecessors)

		if current == end or not queue:
			return

		_weight, _tiebreak, current = heappop(queue)


def _manhattan(end: Coord):
	return lambda node: abs(end[0] - node[0]) + abs(end[1] - node[1])


def _drain(steps, end: Coord) -> list[Coord]:
	# maxlen=1 consumes at C speed, keeping only the finished search's state
	last = deque(steps, maxlen=1)
	return trace_path(last[0].predecessors, end) if last else []


# *_steps yields a Step per expansion; the bare name just returns the path

def dijkstra_steps(start: Coord, end: Coord, adjacency_list: AdjacencyList):
	yield from _search(start, end, adjacency_list, lambda _: 0)


def astar_steps(start: Coord, end: Coord, adjacency_list: AdjacencyList):
	yield from _search(start, end, adjacency_list, _manhattan(end))


def dijkstra(start: Coord, end: Coord, adjacency_list: AdjacencyList) -> list[Coord]:
	return _drain(dijkstra_steps(start, end, adjacency_list), end)


def astar(start: Coord, end: Coord, adjacency_list: AdjacencyList) -> list[Coord]:
	return _drain(astar_steps(start, end, adjacency_list), end)
