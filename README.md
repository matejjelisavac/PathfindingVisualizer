# pathviz

Generate mazes, run pathfinding algorithms on them, and watch the search happen.

Maze generation, search and drawing are three independent modules. The only thing
they share is a plain adjacency list, `dict[(x, y), set[(x, y)]]`, so you can use
any one of them without the other two, and drop your own algorithm in anywhere.

## Install

```bash
pip install pathviz
```

pygame comes with it, for the visualiser. Everything else is standard library.

## A path

```python
from pathviz.maze import recursive_backtracker
from pathviz.search import astar

maze = recursive_backtracker(40, 40, braid=0.2)
path = astar((0, 0), (39, 39), maze)
```

`braid` is the fraction of dead ends removed, so `0` is a perfect maze with exactly
one route between any two cells, and `1` is a maze with no dead ends at all.

## Watching it search

Every algorithm has a `_steps` twin that yields one `Step` per expansion instead of
returning a path. You write the loop, so what gets drawn is entirely up to you:

```python
from pathviz.maze import recursive_backtracker
from pathviz.search import astar_steps, trace_path
from pathviz.visualizer import Visualizer

maze = recursive_backtracker(60, 60, braid=0.2)
start, end = (0, 0), (59, 59)

vis = Visualizer(maze)
vis.draw_maze()

for step in astar_steps(start, end, maze):
    vis.fill_cell(step.current, "Blue")
    vis.present()

for coord in trace_path(step.predecessors, end):
    vis.fill_cell(coord, "Orange")
vis.present()
vis.sleep(2000)
```

Drawing writes to a surface and nothing appears until `present()`, so one frame can
be built from as many `fill_cell` calls as you like.

A `Step` carries `current`, `discovered` (the cells first reached this expansion),
and live references to the search's own `distances` and `predecessors`. Reading them
is free, but they mutate as the search runs, so copy anything you want to keep.

## Your own algorithm

Nothing in pathviz requires a `Step`. Yield whatever you measure and draw it however
you want. The visualiser only ever sees coordinates and colours:

```python
from collections import deque

def bfs(start, end, adjacency_list):
    queue, seen = deque([start]), {start}
    while queue:
        current = queue.popleft()
        yield current, len(queue)          # your own shape
        if current == end:
            return
        for neighbor in adjacency_list[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)

for current, fringe_size in bfs(start, end, maze):
    vis.fill_cell(current, (0, min(fringe_size * 8, 255), 120))
    vis.present()
```

The same is true going the other way: any `dict[node, set[node]]` works as input, so
`astar` and `dijkstra` will run on a graph that has nothing to do with a grid.

## Modules

| Module | What it does | Depends on |
| --- | --- | --- |
| `pathviz.graph` | `GridGraph`, used to build an adjacency list | stdlib only |
| `pathviz.maze` | `recursive_backtracker`, `fully_connected` | `pathviz.graph` |
| `pathviz.search` | `dijkstra`, `astar`, their `_steps` twins, `trace_path` | stdlib only |
| `pathviz.visualizer` | `Visualizer`, draws mazes, cells and numbers | `pygame` |

Nothing is re-exported from the top level, so importing one module doesn't drag in
the others. `pathviz.search` imports nothing but the standard library, and code that
never touches `pathviz.visualizer` never loads pygame.

Both import forms work, whichever reads better where you are:

```python
from pathviz.search import astar          # astar(...)
from pathviz import search                # search.astar(...)
```

## Examples

```bash
python examples/animate.py
```
