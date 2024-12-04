import pygame
import random
import time
import pandas as pd
import heapq

size = 1000
tileSet = [4,5,6,7,8,9,10,12,20,25]

trialNum = 200

braidLevel = 1 # 1 in braidLevel dead ends looped at the start
braidSet = [1,4,50,float('inf')]

def resetCells():
    for cell in cells:
        cell.visited = False
        cell.distance = float("inf")
        cell.predecessor = None
        cell.partOfPath = False
        cell.f = float("inf")


#Cell Class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    toSearch = []

    start.distance = 0
    heapq.heappush(toSearch, (start.distance, start.x, start.y, start))

    searchCount = 0

    start_time = time.time()

    while not found:
        searchCount += 1
        current = heapq.heappop(toSearch)[3]
        current.visited = True

        neighbors = current.getTouching()

        for cell in neighbors:
            if not cell.visited:
                new_distance = current.distance + cell.weight
                if new_distance < cell.distance:
                    cell.distance = new_distance
                    cell.predecessor = current  # Set predecessor
                    heapq.heappush(toSearch, (cell.distance, cell.x, cell.y, cell))
                if cell == end:
                    found = True


    # When found.
    path = []
    current = end
    while current and current.predecessor:
        path.append(current)
        current = current.predecessor
        current.partOfPath = True

    end_time = time.time()

    execution_time = end_time - start_time
    return [execution_time, searchCount, len(path), path]

def astar(start, end):
    resetCells()

    found = False

    for cell in cells:
        cell.distanceToEnd = abs(end.x - cell.x) + abs(end.y - cell.y)

    toSearch = []

    start.distance = 0
    start.f = start.distance + start.distanceToEnd
    heapq.heappush(toSearch, (start.f, start.x, start.y, start))

    searchCount = 0

    start_time = time.time()

    while not found:
        searchCount += 1
        current = heapq.heappop(toSearch)[3]
        current.visited = True

        neighbors = current.getTouching()

        for cell in neighbors:
            if not cell.visited:
                new_distance = current.distance + cell.weight
                if new_distance < cell.distance:
                    cell.distance = new_distance
                    cell.predecessor = current  # Set predecessor
                    cell.f = cell.distance + cell.distanceToEnd
                    heapq.heappush(toSearch, (cell.f, cell.x, cell.y, cell))
                if cell == end:
                    found = True

    # When found.
    path = []
    current = end
    while current and current.predecessor:
        path.append(current)
        current = current.predecessor
        current.partOfPath = True

    end_time = time.time()

    execution_time = end_time - start_time
    return [execution_time, searchCount, len(path), path]



dijRawData = [] #2d array for time, cell searched, path length
astRawData = []
rawData = [] #2D array for [trialNum, size,braidlevel]

sizes = []
braidLevels = []
dijTimes = []
astTimes = []
dijLowestTimes = []
dijHighestTimes = []
astLowestTimes = []
astHighestTimes = []
dijWins = []
astWins = []
winner = []
totalCells = []
cellsCoveredDij =[] #Percentage
cellsCoveredAst =[] #Percentage
pathLength = []


for j in range(len(braidSet)):

    braidLevel = braidSet[j]

    for i in range(len(tileSet)):
        tile = tileSet[i]
        dijData = []
        astData = []

        dijWinCount = 0
        astWinCount = 0
        tieCount = 0


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
        start = random.choice(cells)
        next = step(start)
        while visitedStack:
            next = step(next)

        # Braiding
        for i in range(int(round(size/20, 0))):
            braid()


        #Pathing
        start = cells_2d[rows-1][0]
        start.start = True
        end = cells_2d[rows//2][cols//2]
        end.end = True

        for r in range(trialNum):

            ast = astar(start, end)
            astData.append(ast)  # Returns a list with [time taken, cells covered]
            astRawData.append(ast)

            dij = dijkstra(start, end)
            dijData.append(dij) #Returns a list with [time taken, cells covered]
            dijRawData.append(dij)

            rawData.append([r+1,cols,braidLevel])
            print("Trial", r+1, "complete")


            if dij[0] < ast[0]:
                dijWinCount +=1
            elif ast[0] < dij[0]:
                astWinCount +=1
            else:
                tieCount +=1





        sum1 = 0
        dijLowest = 9999999999
        dijHighest = -1
        sum2 = 0
        astLowest = 9999999999
        astHighest = -1
        sum3 = 0
        sum4 = 0
        sum5 = 0
        for i in range(trialNum):
            sum1 = sum1 + dijData[i][0] #Dij Average Time
            if dijData[i][0] < dijLowest: #Finding Lowest Time Dijkstra
                dijLowest = dijData[i][0]
            if dijData[i][0] > dijHighest: #Finding Highest Time Dijkstra
                dijHighest = dijData[i][0]
            sum2 = sum2 + astData[i][0] #Ast Average Time
            if astData[i][0] < astLowest: #Finding Lowest Time Astar
                astLowest = astData[i][0]
            if astData[i][0] > astHighest: #Finding Highest Time Astar
                astHighest = astData[i][0]
            sum3 = sum3 + dijData[i][1]  # Dij Average Cells Covered
            sum4 = sum4 + astData[i][1]  # Ast Average Cells Covered
            sum5 = sum5 + dijData[i][2]

        sizes.append(rows)
        braidLevels.append(round(100/braidLevel,1) if braiding else 0)
        dijTimes.append(round(sum1/len(dijData)*1000, 6)) #In millisecs
        astTimes.append(round(sum2/len(astData)*1000, 6))
        dijLowestTimes.append(round(dijLowest*1000,6))
        dijHighestTimes.append(round(dijHighest*1000,6))
        astLowestTimes.append(round(astLowest*1000,6))
        astHighestTimes.append(round(astHighest*1000,6))
        dijWins.append(dijWinCount)
        astWins.append(astWinCount)
        totalCells.append(len(cells))
        cellsCoveredDij.append(round(sum3/trialNum,1))
        cellsCoveredAst.append(round(sum4/trialNum,1))
        winner.append("A*" if sum2/len(astData) < sum1/len(dijData) else "Dij" if sum1/len(dijData) < sum2/len(astData) else "Tie")
        pathLength.append(sum5/trialNum)


data = {

    "Braiding %" : braidLevels,
    "Maze Size (sizexsize)" : sizes,
    "Number of Trials" : [trialNum for i in range(len(sizes))],
    "Path Length" : pathLength,
    "Average Time Dijkstra (ms)" : dijTimes,
    "Average Time A* (ms)" : astTimes,
    "Time Difference (ms)" : [round(abs(astTimes[i] - dijTimes[i]),6) for i in range(len(astTimes))],
    "Winner" : winner,
    "A* Win Count": astWins,
    "Dijkstra Win Count": dijWins,
    "Lowest Dijkstra Time (ms)" : dijLowestTimes,
    "Highest Dijkstra Time (ms)" : dijHighestTimes,
    "Dijsktra Uncertainty (ms)" : [(dijHighestTimes[i]-dijLowestTimes[i])/2 for i in range(len(dijHighestTimes))],
    "Lowest A* Time (ms)" : astLowestTimes,
    "Highest A* Time (ms)" : astHighestTimes,
    "A* Uncertainty (ms)" : [(astHighestTimes[i]-astLowestTimes[i])/2 for i in range(len(astHighestTimes))],
    "Total Cells" : totalCells,
    "Cells Covered by Dijkstra" : cellsCoveredDij,
    "Cells Covered by A*" : cellsCoveredAst


}

raw = {

    "Braiding %" : [round(100/rawData[i][2],1) for i in range(len(rawData))],
    "Size" : [rawData[i][1] for i in range(len(rawData))],
    "Trial number" : [rawData[i][0] for i in range(len(rawData))],
    "Dijkstra Time (ms)" : [dijRawData[i][0]*1000 for i in range(len(dijRawData))],
    "A* Time (ms)" : [astRawData[i][0]*1000 for i in range(len(astRawData))],
    "Total Cell Count": [rawData[i][1] ** 2 for i in range(len(rawData))],
    "Dijkstra's Cell Search Count" : [dijRawData[i][1] for i in range(len(dijRawData))],
    "A* Cell Search Count" : [astRawData[i][1] for i in range(len(astRawData))],
    "Path length" : [astRawData[i][2] for i in range(len(astRawData))],

}


df = pd.DataFrame(data)
df1 = pd.DataFrame(raw)
#

df.to_csv("/Users/matejjelisavac/Desktop/processed_data.csv")
df1.to_csv("/Users/matejjelisavac/Desktop/raw_data.csv")
