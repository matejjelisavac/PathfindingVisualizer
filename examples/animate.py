from pathviz import maze, search
from pathviz.visualizer import Visualizer


def animate(adjacency_list, start, end, steps):
	vis = Visualizer(adjacency_list, 800, 1000)
	vis.draw_maze()
	vis.fill_cell(start, "Orange")
	vis.fill_cell(end, "Orange")
	vis.present()

	for step in steps:
		vis.fill_cell(step.current, (100, min(step.distances[step.current], 255), 100))
		vis.present()

	# predecessors is live, so the last step already holds the finished search
	for coord in search.trace_path(step.predecessors, end):
		vis.fill_cell(coord, "Orange")
	vis.present()

	vis.sleep(250)


if __name__ == "__main__":
	width = 120
	height = 120
	start, end = (0,0), (width-1, height-1)

	adjacency_list = maze.recursive_backtracker(width, height, 1)

	animate(adjacency_list, start, end, search.astar_steps(start, end, adjacency_list))
	animate(adjacency_list, start, end, search.dijkstra_steps(start, end, adjacency_list))
