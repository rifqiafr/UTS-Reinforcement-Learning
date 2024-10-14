import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Window size
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (160, 160, 160)

# Maze setup
maze = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 1, 0],
    [1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 2]
]

# Define positions
agent_pos = [0, 0]  # Starting position of the agent
exit_pos = [4, 4]   # Exit position

# Reward settings
REWARD_GOAL = 100
REWARD_MOVE = -1
REWARD_OBSTACLE = -50

# Get the dimensions of the maze
GRID_SIZE_X = len(maze)
GRID_SIZE_Y = len(maze[0])
CELL_SIZE_X = WIDTH // GRID_SIZE_Y
CELL_SIZE_Y = HEIGHT // GRID_SIZE_X

# Policy Initialization
policy = np.zeros((GRID_SIZE_X, GRID_SIZE_Y), dtype=int)  # Actions: 0: up, 1: down, 2: left, 3: right

# Bellman Update Function
def update_policy_bellman():
    global policy
    V = np.zeros((GRID_SIZE_X, GRID_SIZE_Y))
    
    for _ in range(100):  # Allow multiple updates to ensure convergence
        for i in range(GRID_SIZE_X):
            for j in range(GRID_SIZE_Y):
                if (i, j) == tuple(exit_pos):
                    V[i, j] = REWARD_GOAL  # Reward for reaching the goal
                    continue
                if maze[i][j] == 1:
                    V[i, j] = REWARD_OBSTACLE  # Penalty for hitting obstacles
                    continue

                q_values = []
                for action in range(4):  # 0: up, 1: down, 2: left, 3: right
                    next_i, next_j = i, j
                    if action == 0 and i > 0:  # Up
                        next_i -= 1
                    elif action == 1 and i < GRID_SIZE_X - 1:  # Down
                        next_i += 1
                    elif action == 2 and j > 0:  # Left
                        next_j -= 1
                    elif action == 3 and j < GRID_SIZE_Y - 1:  # Right
                        next_j += 1

                    if maze[next_i][next_j] == 1:
                        reward = REWARD_OBSTACLE
                    elif (next_i, next_j) == tuple(exit_pos):
                        reward = REWARD_GOAL
                    else:
                        reward = REWARD_MOVE
                    
                    q_value = reward + V[next_i, next_j]  # Bellman update
                    q_values.append(q_value)
                
                V[i, j] = max(q_values)  # Update value function
                policy[i, j] = np.argmax(q_values)  # Update policy

# Function to draw the maze
def draw_maze():
    for i in range(GRID_SIZE_X):
        for j in range(GRID_SIZE_Y):
            rect = pygame.Rect(j * CELL_SIZE_X, i * CELL_SIZE_Y, CELL_SIZE_X, CELL_SIZE_Y)
            pygame.draw.rect(win, WHITE, rect, 1)
            
            if (i, j) == tuple(agent_pos):
                pygame.draw.rect(win, BLUE, rect)
            elif (i, j) == tuple(exit_pos):
                pygame.draw.rect(win, GREEN, rect)
            elif maze[i][j] == 1:
                pygame.draw.rect(win, GRAY, rect)

# Game loop
def game_loop():
    global agent_pos
    running = True

    update_policy_bellman()  # Initialize policy and value function

    while running:
        win.fill(BLACK)
        draw_maze()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Follow policy
        i, j = agent_pos
        action = policy[i, j]  # Get action from policy

        next_pos = agent_pos.copy()  # Copy current position for valid movement
        if action == 0 and i > 0:  # Up
            next_pos[0] -= 1
        elif action == 1 and i < GRID_SIZE_X - 1:  # Down
            next_pos[0] += 1
        elif action == 2 and j > 0:  # Left
            next_pos[1] -= 1
        elif action == 3 and j < GRID_SIZE_Y - 1:  # Right
            next_pos[1] += 1

        # Validate new position before updating
        if maze[next_pos[0]][next_pos[1]] != 1:  # Check if it's not an obstacle
            agent_pos = next_pos  # Update agent's position

        # Check if agent reached the target
        if agent_pos == exit_pos:
            print("You reached the exit!")
            running = False

        # Output agent position
        print(f"Agent position: {agent_pos}")

        # Delay to slow down movement
        pygame.time.delay(500)

    pygame.quit()

# Run the game
game_loop()
