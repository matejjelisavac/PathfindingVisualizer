"""Maze generation, pathfinding and visualisation, connected only by a plain
adjacency list: dict[Coord, set[Coord]].

Nothing is re-exported here on purpose. Import the module you want and you pay
for that one alone:

	from pathviz import maze, search
	from pathviz.visualizer import Visualizer
"""

__version__ = "0.1.0"
