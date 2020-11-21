# Imports
import pygame
import math
from queue import PriorityQueue
from Utils.RGBcolors import AllColors as Colors

# Constants
WIDTH = 800
HEIGHT = WIDTH

ROWS = 50

SHOWSTEPS = True

# Creates Window

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("A* Pathfinding")

# Creates Node Class - Used as points that the pathfinding algorithm navigates through
class Node():
    def __init__(self,row,col,size,total_rows,showsteps):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.type = "TRAVERSABLE"
        self.color =  Colors.WHITE
        self.neighbors = []
        self.size = size
        self.totalRows = total_rows
        self.showSteps = showsteps

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.type == "CLOSED"

    def is_open(self):
        return self.type == "OPEN"

    def is_wall(self):
        return self.type == "WALL"

    def is_path(self):
        return self.type == "PATH"

    def is_start(self):
        return self.type == "START"

    def is_end(self):
        return self.type == "END"

    def settype_traverseable(self):
        self.type = "TRAVERSABLE"
        self.color = Colors.WHITE

    def settype_closed(self):
        self.type = "CLOSED"
        if self.showSteps:
            self.color = Colors.RED

    def settype_open(self):
        self.type = "OPEN"
        if self.showSteps:
            self.color = Colors.ORANGE

    def settype_wall(self):
        self.type = "WALL"
        self.color = Colors.BLACK

    def settype_start(self):
        self.type = "START"
        self.color = Colors.PURPLE 

    def settype_end(self):
        self.type = "END"
        self.color = Colors.TURQUOISE

    def settype_path(self):
        self.type = "PATH"
        self.color = Colors.GREEN

    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.size,self.size))

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.totalRows - 1  and not grid[self.row + 1][self.col].is_wall(): # Checks Node Below
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0  and not grid[self.row - 1][self.col].is_wall(): # Checks Node Above
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # Checks Node To The Left
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].is_wall(): # Checks Node To The Right
            self.neighbors.append(grid[self.row][self.col + 1])


    def __lt__(self,other):
        return False

def h(p1,p2):
    """ Gets Manhatten Distance between two points

    Args:
        p1 (tuple): Position of The First Point
        p2 (tuple): Position of The Second Point

    Returns:
        [int]: Manhatten Distance between the given points
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def create_final_path(cameFrom, current, draw, showSteps):
    while current in cameFrom:
        current = cameFrom[current]
        current.settype_path()
        if showSteps:
            draw()
    
    if not showSteps:
        draw()


def compute(draw,grid,start,end,showsteps):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    gScore = {node: float("inf") for row in grid for node in row}
    gScore[start] = 0
    fScore = {node: float("inf") for row in grid for node in row}
    fScore[start] = h(start.get_pos(), end.get_pos())

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == end:
            create_final_path(cameFrom, end, draw, showsteps)
            end.settype_end()
            start.settype_start()
            return True

        for neighbor in current.neighbors:
            tempGScore = gScore[current] + 1

            if tempGScore < gScore[neighbor]: 
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.settype_open()

        if showsteps:
            draw()

        if current != start:
            current.settype_closed()

    return False



def make_grid(rows,screen_width, showsteps):
    """ Generates Grid Data Structure

    Args:
        rows (int): Number of Rows
        scren_width (int): Width/Height of Game Window

    Returns:
        list: The Completed Grid Data Set
    """
    grid = []
    gap = screen_width // rows
    for r in range(rows):
        grid.append([])
        for c in range(rows):
            node = Node(r,c,gap,rows, showsteps)
            grid[r].append(node)



    return grid


def draw_grid(win,rows,screen_width):
    """ Draws Grid Lines

    Args:
        win (Surface): The Game Window
        rows (int): Number of rows
        screen_width (int): Width/Height Of Game Window
    """
    gap = screen_width // rows
    for r in range(rows):
        pygame.draw.line(win, Colors.GREY,(0, r * gap),(screen_width, r * gap))

    for c in range(rows):
        pygame.draw.line(win, Colors.GREY,(c * gap, 0),(c*gap, screen_width))


def reset_pathfind(grid):
    for row in grid:
        for node in row:
            if node.is_closed() or node.is_open() or node.is_path():
                node.settype_traverseable()

def draw(win,grid,rows,screen_width):
    """ Manages Screen Drawing

    Args:
        win (Surface): The Game Window
        grid (list): The Grid List
        rows (int): Number of rows
        screen_width (int): WIdth/Height of Game Window
    """
    win.fill(Colors.WHITE)


    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win,rows,screen_width)
    pygame.display.update()


def get_click_pos(mouse_pos,rows,screen_width):
    """ Gets Postion of Mouse in the form of a row and col

    Args:
        mouse_pos (tuple): Pixel Position of mouse
        rows (int): Number Of Rows
        screen_width (int): Width/Height Of Game Window

    Returns:
        ints: Row and Column Position
    """
    gap = screen_width // rows
    y, x = mouse_pos

    row = y // gap
    col = x // gap

    return row, col

def main(win,screen_width,rows, showsteps):
    grid = make_grid(rows,screen_width, showsteps)

    start = None
    end = None

    running = True # Is main loop running
    active = False # Is Algorithm Running

    while running:
        draw(win,grid,rows,screen_width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if active:
                continue


            if pygame.mouse.get_pressed()[0]: # Left Mouse Button
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos,rows,screen_width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.settype_start()
                elif not end and node != start:
                    end = node
                    end.settype_end()
                elif node != start and node != end:
                    node.settype_wall()
            elif pygame.mouse.get_pressed()[2]: # Right Mouse Button
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos,rows,screen_width)
                node = grid[row][col]
                node.settype_traverseable()

                if node == start:
                    start = None
                elif node == end:
                    end = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if start != None and end != None:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)

                        compute(lambda: draw(win,grid,rows,screen_width), grid, start, end, showsteps)

                elif event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(rows,screen_width, showsteps)


                elif event.key == pygame.K_s:
                    showsteps = not showsteps

                elif event.key == pygame.K_r:
                    reset_pathfind(grid)


    pygame.quit()


main(win, WIDTH, ROWS, SHOWSTEPS)
