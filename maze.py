import graph
from random import choice, sample

def recursive_backtracker(width, height, braid=0):

	gr = graph.GridGraph.empty(width, height)

	current = choice(list(gr.adjacency_list.keys()))
	path, visited = [current], set([current])

	while path:
		neighbors = gr.grid_neighbors(current)
		candidates = [neighbor for neighbor in neighbors if neighbor not in visited]

		# If all neighbors already visited then backtrack
		if not candidates:
			visited.add(current)
			current = path.pop()

		# Otherwise, if at least 1 neighbor not visited
		else:
			next = choice(candidates)
			gr.add_edge(current, next)
			visited.add(current)
			path.append(current)
			current = next

	# braid = fraction of dead ends removed, sampled uniformly at random.
	# Snapshot the population first so the denominator can't shift as we add edges.
	dead_ends = [coord for coord in gr.adjacency_list if len(gr.adjacency_list[coord]) == 1]

	for coord in sample(dead_ends, round(braid * len(dead_ends))):
		options = [neighbor for neighbor in gr.grid_neighbors(coord) if neighbor not in gr.adjacency_list[coord]]
		if options:
			gr.add_edge(coord, choice(options))

	return gr.adjacency_list

def fully_connected(width, height):
	gr = graph.GridGraph.empty(width, height)
	for coord in gr.adjacency_list:
		for neighbor in gr.grid_neighbors(coord):
			gr.add_edge(coord, neighbor)
	return gr.adjacency_list