import graph
from random import choice

def recursive_backtracker(width, height):

	gr = graph.GridGraph.empty(width, height)

	current = choice(list(gr.adjacency.keys()))
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

	return gr.adjacency

	# count = 0
	# for coord in adjacency:
	# 	if len(adjacency[coord]) == 1:
	# 		count+=1
	# 		if count >= (1 / braid):
	# 			addEdge(adjacency, coord, random.choice([neighbor for neighbor in getCellNeighbors(coord, size) if neighbor not in adjacency[coord]]))
	# 			count = 0

# print(recursive_backtracker(20,20))