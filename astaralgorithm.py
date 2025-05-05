import heapq

class Cell:
  def __init__(self):
    #parent cell's row index
    self.parent_i = 0
    #parent cell's column index
    self.parent_j = 0
    #total cost of the cell (g + h)
    self.f = float('inf')
    #cost from start to this cell
    self.g = float('inf')
    #heristic cost from current cell to destination
    self.h = 0

#check if a cell is valid
def is_valid(row, col, rowMax, colMax):
  return (row >= 0) and (row < rowMax) and (col >= 0) and (col < colMax)

#check if cell is unblocked
def is_unblocked(grid, row, col):
  return grid[row][col] == 1

#check if the cell is the destination
def is_destination(row, col, dest):
  return row == dest[0] and col == dest[1]

#used to calculate heristic for a cell using manhattan distance
def calculate_h_value(row, col, dest):
  return (abs(row-dest[0])+ abs(col-dest[1]))

#used to retrieve path from source to destination using the destination and a series of cell parents
def trace_path(cell_details, dest):
  path = []
  row = dest[0]
  col = dest[1]

  #starting from destination, trace path back to source using parent cells
  while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
    #add current cell
    path.append((row, col))
    #change row and col to refelct parent cell
    temp_row = cell_details[row][col].parent_i
    temp_col = cell_details[row][col].parent_j
    row = temp_row
    col = temp_col

  #source has not yet been added so add source cell
  path.append((row, col))

  #since current path is from destination to source, we reverse it to get source to destination
  path.reverse()

  #return path so it can be used by the program
  return path

#implementation of A*
def a_star_search(grid, src, dest, rowMax, colMax):
  res = []
  #check kf source and destination are valid
  if not is_valid(src[0], src[1], rowMax, colMax) or not is_valid(dest[0], dest[1], rowMax, colMax):
    print("Source or destination is invalid")
    return

  #check if they are not blocked
  if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
    print("Source or the destination is blocked")
    return

  #check if at destination
  if is_destination(src[0], src[1], dest):
    print("We are already at the destination")
    return []

  #initialize the reached list(cells we've already visited)
  reached = [[False for _ in range(colMax)] for _ in range(rowMax)]
  #initialize a details grid for all the cells so we can reference it later
  cell_details = [[Cell() for _ in range(colMax)] for _ in range(rowMax)]

  #intialize the start cell
  i = src[0]
  j = src[1]
  #total cost is zero
  cell_details[i][j].f = 0
  #heuristic is initialized to be zero(this will be calculated in a bit)
  cell_details[i][j].g = 0
  #heuristic is initialized to be zero(this will be calculated in a bit)
  cell_details[i][j].h = 0
  cell_details[i][j].parent_i = i
  cell_details[i][j].parent_j = j

  #initialize the frontier(candidate cells to be visited)
  frontier = []
  #push the src cell onto the heap while ensuring the frontier follows the format of a heap. It is stored on the heap as a tuple
  heapq.heappush(frontier, (0.0, i, j))

  #flag for it destination is found or not
  found_dest = False

  #loop of search, basically always check if there is stuff on the frontier or not
  while len(frontier) > 0:
    #grab cell with smallest f value
    p = heapq.heappop(frontier)

    #put current cell in reached list
    i = p[1]
    j = p[2]
    reached[i][j] = True

    #check each direction the robot can move(up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dir in directions:
      #get coordinate of new position
      new_i = i + dir[0]
      new_j = j + dir[1]

      #checking if we can use the successor 
      #by checking if it is valid, not a border cell, and hasn't been reached yet
      if is_valid(new_i, new_j, rowMax, colMax) and is_unblocked(grid, new_i, new_j) and not reached[new_i][new_j]:
        #if it is destination, retunr the list
        if is_destination(new_i, new_j, dest):
          #set the parent of the dest
          cell_details[new_i][new_j].parent_i = i
          cell_details[new_i][new_j].parent_j = j
          #get the path and return it
          res = trace_path(cell_details, dest)
          found_dest = True
          return res
        else:
          #calculate f, g, and h values for successor
          g_new = cell_details[i][j].g + 1.0
          h_new = calculate_h_value(new_i, new_j, dest)
          f_new = g_new + h_new

          #if cell is not on frontier or the f value is smaller than what already exists on the frontier
          if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
            #add cell to frontier
            heapq.heappush(frontier, (f_new, new_i, new_j))
            #update its details
            cell_details[new_i][new_j].f = f_new
            cell_details[new_i][new_j].g = g_new
            cell_details[new_i][new_j].h = h_new
            cell_details[new_i][new_j].parent_i = i
            cell_details[new_i][new_j].parent_j = j

  # If the destination is not found after visiting all cells
  if not found_dest:
    print("Failed to find the destination cell")
    return res



