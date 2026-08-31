import maze
import search
import visualizer
import time

def animate(adjacency_list, start, end, path, steps):
	vis = visualizer.Visualizer(adjacency_list, 800, 1000)
	vis.draw_maze()
	vis.fill_cells([start, end], "Purple")

	for step in steps:
		vis.fill_cells([step["next"]], "Orange")
		vis.fill_cells([step["current"]], "Blue")
		# vis.fill_cells(step["visited"], "Yellow")
	vis.fill_cells(path,"Orange")
	vis.sleep(250)

maze_size = 250
start, end = (0,0), (maze_size/2, maze_size/2)

adjacency_list = maze.recursive_backtracker(maze_size, 1)
# adjacency_list = maze.fully_connected(maze_size)

path, steps = search.astar(start, end, adjacency_list)
animate(adjacency_list, start, end, path, steps)

path, steps = search.dijkstra(start, end, adjacency_list)
animate(adjacency_list, start, end, path, steps)