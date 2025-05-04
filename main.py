import pygame
from astaralgorithm import *

# Window dimensions and grid settings
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 720
ROWS, COLS = 10, 10
BLOCK_SIZE = WINDOW_WIDTH // COLS

# Color definitions
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)  # Agent color

def main():
    #create the grid
    grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    #set the src and destination to nothing
    src = None
    dest = None
    path_found = []

    #agent timer
    agent_index = 0
    agent_timer = 0
    agent_speed = 500  # ms

    #initialize pygame
    pygame.init()
    #set the size of the screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #set the clock for delta time
    clock = pygame.time.Clock()
    #variable for running
    running = True
    while running:
        delta_time = clock.tick(1000)
        #get teh event
        for event in pygame.event.get():
            #close program if the event is quit
            if event.type == pygame.QUIT:
                running = False

            #
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #get position of mouse
                x, y = pygame.mouse.get_pos()
                #convert mouse position to coordinates
                col = x // BLOCK_SIZE
                row = y // BLOCK_SIZE
                clicked = [row, col]

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
                #set dest if src is set 
                elif dest is None and clicked != src and src != None:
                    dest = clicked
                elif clicked == dest:
                    dest = None
                    path_found = []
                elif clicked != src and clicked != dest:
                    grid[row][col] = 0 if grid[row][col] == 1 else 1
                    path_found = []

                if src and dest:
                    path_found = a_star_search(grid, src, dest, ROWS, COLS)
                    if path_found is None:
                        path_found = []
                    agent_index = 0
                    agent_timer = 0
                    print("The path is:", path_found)

        if path_found and agent_index < len(path_found):
            agent_timer += delta_time
            if agent_timer >= agent_speed:
                agent_index += 1
                agent_timer = 0

        screen.fill(WHITE)

        for i in range(ROWS):
            for j in range(COLS):
                x = j * BLOCK_SIZE
                y = i * BLOCK_SIZE
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

                if [i, j] == src:
                    color = BLUE
                elif [i, j] == dest:
                    color = GREEN
                elif path_found and [i, j] in path_found:
                    color = RED
                else:
                    color = GREY if grid[i][j] == 1 else BLACK

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

        # Draw moving agent (orange square)
        if path_found and agent_index > 0 and agent_index <= len(path_found):
            row, col = path_found[agent_index - 1]
            rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, ORANGE, rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
