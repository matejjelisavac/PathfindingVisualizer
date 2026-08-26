import maze
import search
import visualizer

def animate(adjacency_list, start, end, path, steps):
	vis = visualizer.Visualizer(adjacency_list)
	vis.draw_maze()
	vis.fill_cells([start, end], "Purple")

	for step in steps:
		vis.fill_cells([step["current"]], "Blue")
		# vis.fill_cells(step["visited"], "Yellow")
		# print(step["queue"])
	# visualizer.animate(adjacency_list, search.astar((0,0), (19,19), adjacency_list))
	vis.fill_cells(path,"Orange")

maze_size = 30
start, end = (0,0), (maze_size/2, maze_size/2)

adjacency_list = maze.recursive_backtracker(maze_size, 1)
# adjacency_list = maze.fully_connected(maze_size)

path, steps = search.astar(start, end, adjacency_list)
animate(adjacency_list, start, end, path, steps)

path, steps = search.dijkstra(start, end, adjacency_list)
animate(adjacency_list, start, end, path, steps)