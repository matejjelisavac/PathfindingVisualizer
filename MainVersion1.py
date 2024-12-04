import pygame
import random
import time
import math
import heapq
import pandas as pd

size = 800
tileSet = [5,6,7,10,15,20,30,40,100]

trialNum = 20

braiding = True
braidLevel = 1 # 1 in braidLevel dead ends looped at the start
braidSet = [1,4,50,float('inf')]
visualizeGen = False
visualizePath = False
flash = False
showDistances = False #Will only work on true if visualizePath is true


bgColor = pygame.Color("white")
wallColor = (63, 22, 81)

if visualizeGen or visualizePath:
    pygame.init()
    sc = pygame.display.set_mode((size, size))

    clock = pygame.time.Clock()



def resetCells():
    for cell in cells:
        cell.visited = False
        cell.distance = float("inf")
        cell.predecessor = None
        cell.partOfPath = False
        cell.f = float("inf")

def visualizeCurrent(current):
    sc.fill(pygame.Color(bgColor))
    pygame.draw.rect(sc, (pygame.Color("blue")),
                     [current.xD, current.yD, tile, tile], 0)
    [cell.draw() for cell in cells]

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()


#Cell Class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.xD = x * tile
        self.yD = y * tile
        self.visited = False
        self.topWall = True
        self.leftWall = True
        self.rightWall = True
        self.bottomWall = True

        self.weight = 1
        self.distance = float('inf')
        self.distanceToEnd = float('inf')
        self.f = float("inf")

        self.start = False
        self.end = False
        self.partOfPath = False
        self.predecessor = None

    def draw(self): #Only significant for visuals
        if self.visited and self.distance < float('inf') and self.distance != 0:
            try:
                pygame.draw.rect(sc, (200, 100, self.distance*3),
                                 [self.xD, self.yD, tile, tile], 0)
            except:
                pygame.draw.rect(sc, (200, 100, 255),
                                 [self.xD, self.yD, tile, tile], 0)

        if self.distance < float('inf'):
            if not self.visited:
                pygame.draw.rect(sc, (pygame.Color("white")),
                             [self.xD, self.yD, tile, tile], 0)
            if showDistances and self.f == float('inf'):
                font = pygame.font.SysFont('Comic Sans MS', 20)
                text_surface = font.render(str(self.distance), False, pygame.Color("black"))
                sc.blit(text_surface, (self.xD+tile/2, self.yD+tile/2))
            elif showDistances and self.f < float('inf'):
                font = pygame.font.SysFont('Comic Sans MS', 20)
                text_surface = font.render(str(self.f), False, pygame.Color("black"))
                sc.blit(text_surface, (self.xD + tile / 2, self.yD + tile / 2))


        if self.partOfPath:
            pygame.draw.rect(sc, (pygame.Color("orange")),
                             [self.xD, self.yD, tile, tile], 0)
        if self.start or self.end:
            pygame.draw.rect(sc, (pygame.Color("blue")),
                             [self.xD, self.yD, tile, tile], 0)



        if self.topWall:
            pygame.draw.line(sc, pygame.Color(wallColor), (self.xD, self.yD), (self.xD + tile, self.yD), 2)
        if self.leftWall:
            pygame.draw.line(sc, pygame.Color(wallColor), (self.xD, self.yD), (self.xD, self.yD + tile), 2)
        if self.rightWall:
            pygame.draw.line(sc, pygame.Color(wallColor), (self.xD + tile, self.yD), (self.xD + tile, self.yD + tile), 2)
        if self.bottomWall:
            pygame.draw.line(sc, pygame.Color(wallColor), (self.xD, self.yD + tile), (self.xD + tile, self.yD + tile), 2)



    def getNeighbors(self):
        neighbors = []
        if self.x > 0:
            neighbors.append(cells_2d[self.y][self.x - 1])
        if self.x < cols - 1:
            neighbors.append(cells_2d[self.y][self.x + 1])
        if self.y > 0:
            neighbors.append(cells_2d[self.y - 1][self.x])
        if self.y < rows - 1:
            neighbors.append(cells_2d[self.y + 1][self.x])
        return neighbors

    def getTouching(self):
        neighbors = []
        if not self.topWall and self.y > 0:
            neighbors.append(cells_2d[self.y - 1][self.x])
        if not self.rightWall and self.x < cols - 1:
            neighbors.append(cells_2d[self.y][self.x + 1])
        if not self.bottomWall and self.y < rows - 1:
            neighbors.append(cells_2d[self.y + 1][self.x])
        if not self.leftWall and self.x > 0:
            neighbors.append(cells_2d[self.y][self.x - 1])

        return neighbors

    def goNext(self, visitCheck): #ONLY IN GENERATION OF MAZE
        # VisitCheck is True if you want to access only unvisited neighbors
        neighbors = self.getNeighbors()
        if all(neighbor.visited for neighbor in neighbors) and visitCheck: #If all neighbors have been visited
            if visitedStack:
                return visitedStack.pop() #Return top of stack
            else:
                return self

        else:
            next = random.choice(neighbors)
            while next.visited == True and visitCheck: #Find an unvisited neighbor
                next = random.choice(neighbors)


        #Removing walls
        if next.x == self.x + 1 and next.y == self.y:
            self.rightWall = False
            next.leftWall = False
        elif next.x == self.x - 1 and next.y == self.y:
            self.leftWall = False
            next.rightWall = False
        elif next.x == self.x and next.y == self.y + 1:
            self.bottomWall = False
            next.topWall = False
        elif next.x == self.x and next.y == self.y - 1:
            self.topWall = False
            next.bottomWall = False

        return next

def braid():
    x = 0
    for cell in cells:
        count = 0
        if cell.leftWall:
            count= count+1
        if cell.rightWall:
            count= count+1
        if cell.topWall:
            count= count+1
        if cell.bottomWall:
            count= count+1
        if count == 3:
            x=x+1
            if x % braidLevel == 0:
                next = cell.goNext(False)
                edges.append([(cell.x, cell.y), (next.x, next.y)])

def step(current):
    current.visited = True
    next = current.goNext(True)

    if not next.visited:  # Only append to stack if moving to a new cell
        edges.append([(current.x, current.y), (next.x, next.y)])
        visitedStack.append(current)

    return next



def dijkstra(start, end):

    resetCells()

    found = False

    start_time = time.time()


    toSearch = []

    start.distance = 0
    toSearch.append(start)

    searchCount = 0

    while not found:
        searchCount += 1
        current = min(toSearch, key=lambda cell: cell.distance)
        current.visited = True
        toSearch.remove(current)
        neighbors = current.getTouching()

        for cell in neighbors:
            if not cell.visited:
                new_distance = current.distance + cell.weight
                if new_distance < cell.distance:
                    cell.distance = new_distance
                    cell.predecessor = current  # Set predecessor
                if cell not in toSearch:
                    toSearch.append(cell)
                if cell == end:
                    found = True



        if visualizePath:
            visualizeCurrent(current)
            update()

    # When found.
    path = []
    current = end
    while current and current.predecessor:
        path.append(current)
        current = current.predecessor
        current.partOfPath = True

        if visualizePath:
            visualizeCurrent(current)
            update()

    end_time = time.time()

    execution_time = end_time - start_time
    print("DIJ FOUND IN ", execution_time, "SECONDS")
    print("Searched over ", searchCount, " cells out of ", len(cells))
    print("Path length:", len(path))
    return [execution_time, searchCount, len(path), path]


def astar(start, end):
    resetCells()

    found = False

    start_time = time.time()

    for cell in cells:
        cell.distanceToEnd = abs(end.x - cell.x) + abs(end.y - cell.y)

    toSearch = []

    start.distance = 0
    start.f = start.distance+start.distanceToEnd
    toSearch.append(start)

    searchCount = 0

    while not found:
        searchCount += 1
        current = min(toSearch, key=lambda cell: cell.f)
        current.visited = True
        toSearch.remove(current)
        neighbors = current.getTouching()

        for cell in neighbors:
            if not cell.visited:
                new_distance = current.distance + cell.weight
                if new_distance < cell.distance:
                    cell.distance = new_distance
                    cell.predecessor = current  # Set predecessor
                    cell.f = cell.distance + cell.distanceToEnd
                if cell not in toSearch:
                    toSearch.append(cell)
                if cell == end:
                    found = True



        if visualizePath:
            visualizeCurrent(current)
            update()

    # When found.
    path = []
    current = end
    while current and current.predecessor:
        path.append(current)
        current = current.predecessor
        current.partOfPath = True

        if visualizePath:
            visualizeCurrent(current)
            update()

    end_time = time.time()

    execution_time = end_time - start_time
    print("AST FOUND IN ", execution_time, "SECONDS")
    print("Searched over ", searchCount, " cells out of ", len(cells))
    print("Path length:", len(path))
    return [execution_time, searchCount, len(path), path]


sizes = []
braidLevels = []
dijTimes = []
astTimes = []
dijWins = []
astWins = []
ties = []
winner =[]
totalCells = []
cellsCoveredDij =[] #Percentage
cellsCoveredAst =[] #Percentage


for i in range(len(braidSet)):

    braidLevel = braidSet[i]

    tile = tileSet
    for i in range(len(tileSet)):
        tile = tileSet[i]
        dijData = []
        astData = []

        dijWinCount = 0
        astWinCount = 0
        tieCount = 0

        for r in range(trialNum):
            cells = []
            edges = []
            visitedStack = []

            cols, rows = size // tile, size // tile

            for i in range(cols):
                for j in range(rows):
                    cells.append(Cell(j, i))

            cells_2d = [[None for _ in range(cols)] for _ in range(rows)]

            for cell in cells:
                cells_2d[cell.y][cell.x] = cell

            # Generating maze
                #First Run
            start = random.choice(cells)
            next = step(start)

                #Entire Generation
            while visitedStack:
                next = step(next)
                if visualizeGen:
                    visualizeCurrent(next)
                    update()


                # Braiding
            if braiding:
                for i in range(int(round(size/20, 0))):
                    braid()

                    if visualizeGen:
                        visualizeCurrent(next)
                        update()


            print("GENERATION COMPLETE.")
            print("Edge count: ", len(edges))
            print("Cell count: ", len(cells))
            print("////////////////////////////")


            # pygame.init()
            # sc = pygame.display.set_mode((size, size))
            # sc.fill(pygame.Color(bgColor))
            # [cell.draw() for cell in cells]
            #
            # update()
            #
            # time.sleep(5)

            start = cells_2d[rows-1][0]
            start.start = True
            end = random.choice([cell for cell in cells if not cell.start and cell.x > rows/2 and cell.y < cols/2])
            end.end = True

            dij = dijkstra(start, end)
            dijData.append(dij) #Returns a list with [time taken, cells covered]
            if flash:
                pygame.init()
                sc = pygame.display.set_mode((size, size))
                sc.fill(pygame.Color(bgColor))
                [cell.draw() for cell in cells]
                update()
                time.sleep(0.4)

            ast = astar(start, end)

            astData.append(ast) #Returns a list with [time taken, cells covered]
            if flash:
                pygame.init()
                sc = pygame.display.set_mode((size, size))
                sc.fill(pygame.Color(bgColor))
                [cell.draw() for cell in cells]
                update()
                time.sleep(0.4)

            print("Trial ", r)

            if dij[0] < ast[0]:
                dijWinCount +=1
            elif ast[0] < dij[0]:
                astWinCount +=1
            else:
                tieCount +=1





        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        for i in range(trialNum):
            sum1 = sum1 + dijData[i][0] #Dij Average Time
            sum2 = sum2 + astData[i][0] #Ast Average Time
            sum3 = sum3 + dijData[i][1]  # Dij Average Cells Covered
            sum4 = sum4 + astData[i][1]  # Ast Average Cells Covered

        sizes.append(rows)
        braidLevels.append(round(100/braidLevel,1) if braiding else 0)
        dijTimes.append(round(sum1/len(dijData)*1000, 4)) #In millisecs
        astTimes.append(round(sum2/len(astData)*1000, 4))
        dijWins.append(dijWinCount)
        astWins.append(astWinCount)
        ties.append(tieCount)
        totalCells.append(len(cells))
        cellsCoveredDij.append(round(sum3/trialNum/len(cells)*100,1))
        cellsCoveredAst.append(round(sum4/trialNum/len(cells)*100,1))
        winner.append("A*" if sum2/len(astData) < sum1/len(dijData) else "Dij" if sum1/len(dijData) < sum2/len(astData) else "Tie")


data = {

    "Braiding %" : braidLevels,
    "Maze Size (sizexsize)" : sizes,
    "Number of Trials" : [trialNum for i in range(len(sizes))],
    "Average Time Dijkstra (ms)" : dijTimes,
    "Average Time A* (ms)" : astTimes,
    "Time Difference (ms)" : [round(abs(astTimes[i] - dijTimes[i]),4) for i in range(len(astTimes))],
    "Winner" : winner,
    "A* Win Count" : astWins,
    "Dijkstra Win Count": dijWins,
    "Tie Count" : ties,
    "Total Cells" : totalCells,
    "% Cells Covered by Dijkstra" : cellsCoveredDij,
    "% Cells Covered by A*" : cellsCoveredAst


}


df = pd.DataFrame(data)


df.to_csv("/Users/matejjelisavac/Desktop/data.csv")
