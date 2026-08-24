import maze
import search
import visualizer

adjacency_list = maze.recursive_backtracker(20, 1)

visualizer.animate(adjacency_list, search.astar((0,0), (19,19), adjacency_list), 244)
visualizer.animate(adjacency_list, search.dijkstra((0,0), (19,19), adjacency_list), 244)