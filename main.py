import pygame
from astaralgorithm import *

#height and width of the window
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 720

#Some predefined colors
BLACK = (0,0,0)
WHITE = (200,200,200)
RED = (255,0,0)
GREY = (128,128,128)
BLUE = (0,0,255)
GREEN = (0,255,0)

def main():
  # Define the grid (1 for unblocked, 0 for blocked)
  grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  ]

  # Define the source and destination
  src = [8, 0]
  dest = [0, 0]

  #res path
  res = []

  # Run the A* search algorithm
  res = a_star_search(grid, src, dest)
  print("The path is : ", res)
  print("the length of res is ", len(res))

  #pygame set up
  pygame.init()
  screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  clock = pygame.time.Clock()
  running = True

  
  while running:
    #poll for events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    #fill background of screen with white
    screen.fill(WHITE)

    #render path finding stuff here
    #draw the grid
    #calculate block size from screen width and height
    blockSize = WINDOW_WIDTH//10
    for x in range(0, WINDOW_WIDTH, blockSize):
      for y in range(0, WINDOW_HEIGHT, blockSize):
        #get actual value for coordinates
        coordinateX = x//blockSize
        coordinateY = y//blockSize
        #to check if point is on path
        onPath = False
        rect = pygame.Rect(x, y, blockSize, blockSize)
        #path color is default to red
        color = RED
        #check if source or end node
        if(coordinateX == src[0] and coordinateY == src[1]):
          color = BLUE
        elif(coordinateX == dest[0] and coordinateY == dest[1]):
          color = GREEN
        for point in res:
          if(coordinateX == point[0] and coordinateY == point[1]):
            pygame.draw.rect(screen, color, rect, 0)
            pygame.draw.rect(screen, BLACK, rect, 1)
            onPath = True
        #if point is not on path
        if onPath is False:
         #check if it is an obstacle
         if(grid[coordinateX][coordinateY] == 0):   
          pygame.draw.rect(screen, BLACK, rect, 0)
         else:
          pygame.draw.rect(screen, GREY, rect, 0)
          pygame.draw.rect(screen, BLACK, rect, 1)

    pygame.display.flip()

    clock.tick(60)

  pygame.quit()


if __name__ == "__main__":
    main()