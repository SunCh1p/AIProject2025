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
    grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    src = None
    dest = None
    res = []

    agent_index = 0
    agent_timer = 0
    agent_speed = 500  # ms

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                col = x // BLOCK_SIZE
                row = y // BLOCK_SIZE
                clicked = [row, col]

                if src is None:
                    src = clicked
                elif clicked == src:
                    src = None
                    res = []
                elif dest is None and clicked != src:
                    dest = clicked
                elif clicked == dest:
                    dest = None
                    res = []
                elif clicked != src and clicked != dest:
                    grid[row][col] = 0 if grid[row][col] == 1 else 1
                    res = []

                if src and dest:
                    res = a_star_search(grid, src, dest, ROWS, COLS)
                    if res is None:
                        res = []
                    agent_index = 0
                    agent_timer = 0
                    print("The path is:", res)

        if res and agent_index < len(res):
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
                elif res and [i, j] in res:
                    color = RED
                else:
                    color = GREY if grid[i][j] == 1 else BLACK

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

        # Draw moving agent (orange square)
        if res and agent_index > 0 and agent_index <= len(res):
            row, col = res[agent_index - 1]
            rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, ORANGE, rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
