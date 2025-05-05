import pygame
from astaralgorithm import *
import random

#dimensions and grid settings
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
ROWS, COLS = 50, 50
BLOCK_SIZE = WINDOW_WIDTH // COLS

#predefined colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

def main():
    #create the grid
    grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    #set the src and destination to nothing
    src = None
    dest = None
    path_found = []


    #index for accessting the 
    agent_index = 0
    agent_timer = 0
    agent_speed = 100  # ms


    #initialize pygame
    pygame.init()
    #set the size of the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #set the clock for delta time
    clock = pygame.time.Clock()
    #variable for running
    running = True

#creating random obsctacles without blocking the start or the goal
    def ranObstacles(gen=0.3):
        #only genrated when the start and goal block are in the grid 
        if not src or not dest:
            return
        while True:
            #loop around the grid to place the ranObstacles 
            for row in range(ROWS):
                for col in range(COLS):
                    if [row,col]==src or [row,col]==dest:
                        grid[row][col]=1
                    else:
                        grid[row][col] = 0 if random.random()<gen else 1
            test_path =a_star_search(grid,src,dest,ROWS,COLS)
            if test_path:
                break
    #var for checking if a button is pressed
    isPressed = False
    #var for checking whether to draw border block or delete border block. If True, draw border block, other wise don't
    drawBorder = False
    while running:
        #process events
        delta_time = clock.tick(1000)
        #get the inputs
        for event in pygame.event.get():
            #close program if the event is quit
            if event.type == pygame.QUIT:
                running = False
            #click o will generated random obstcal and rest the path,vistied block by agent,agent move, and agent timer
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                   ranObstacles()
                   #regenerate the path
                   path_found=a_star_search(grid, src, dest, ROWS, COLS)
                   agent_index=0
                   agent_timer=0
            #rest all everything on the grid if you click r on the keyboard 
                if event.key == pygame.K_r:
                    grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
                    #regenerate path
                    path_found = a_star_search(grid, src, dest, ROWS, COLS)
                    agent_index=0
                    agent_timer=0
                if event.key ==pygame.K_b:
                    drawBorder = not drawBorder
                    print("Draw Border: ", drawBorder)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                isPressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                isPressed = False

            #process events       
            if isPressed == True:
                #get position of mouse
                x, y = pygame.mouse.get_pos()
                #convert mouse position to coordinates
                col = x // BLOCK_SIZE
                row = y // BLOCK_SIZE
                clicked = (row, col)
                #if src is none, set src to clicked coordinates
                if src is None:
                    src = clicked
                #if src is set, and you clicked it again, un set it
                elif clicked == src:
                    #set src to none
                    src = None
                    #set path found to nothing
                    path_found = []
                    #set destination to nothing
                    dest = None
                    #set the path to empty becuase it is not vaild anymore  
                #set dest if src is set 
                elif dest is None and clicked != src and src != None:
                    dest = clicked
                #if not setting src of dest, set barrier
                elif clicked != src and clicked != dest:
                    if(drawBorder == True):
                        grid[row][col] = 0
                    else:
                        grid[row][col] = 1
                #if src and dest are found, get the path
                if src and dest:
                    #get the path if it exists
                    path_found = a_star_search(grid, src, dest, ROWS, COLS)
                    #if path found just doesn't return any
                    if path_found is None:
                        path_found = []
                    #otherwise agent index and timer is set to 0
                    agent_index = 0
                    agent_timer = 0
                        # print("The path is:", path_found)
                        # print("The visited path is: ", visited_path)
        #handle agent movement logic
        if path_found:
            agent_timer += delta_time
            if agent_timer >= agent_speed:
                #move the agent
                if(path_found and len(path_found) > 1):
                    print("src being set")
                    src = path_found[1]
                    path_found = a_star_search(grid, src, dest, ROWS, COLS)
                agent_timer = 0
                if(src == dest):
                    path_found = []
                    dest = None
                if(path_found and len(path_found) > 0):
                    print("path found: ", path_found)

        #display outputs
        screen.fill(WHITE)
        #for every row and column
        for i in range(ROWS):
            for j in range(COLS):
                # print("path found: ", path_found)
                # print("current coord: ", (i,j))
                #get actual coordinate on screen
                x = j * BLOCK_SIZE
                y = i * BLOCK_SIZE
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                #if current coordinate is the source, make rect blue
                if (i, j) == src:
                    color = BLUE
                #if current coordinate is the dest, make it green
                elif (i, j) == dest:
                    color = GREEN
                #color the path red when it is visited by the agent 
                elif path_found and (i, j) in path_found:
                    color = RED
                #other wise print it as grey
                else:
                    color = GREY if grid[i][j] == 1 else BLACK
                pygame.draw.rect(screen, color, rect, 0)
                pygame.draw.rect(screen, BLACK, rect, 1)

        # Draw moving agent (orange square)
        if path_found and agent_index > 0 and agent_index <= len(path_found):
            row, col = path_found[agent_index - 1]
            rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, ORANGE, rect, 0)
            pygame.draw.rect(screen, BLACK, rect, 1)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
