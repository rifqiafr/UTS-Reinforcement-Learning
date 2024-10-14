import pygame
import numpy as np
import random

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

# Grid size
GRID_SIZE_X = 5
GRID_SIZE_Y = 5
CELL_SIZE_X = WIDTH // GRID_SIZE_Y
CELL_SIZE_Y = HEIGHT // GRID_SIZE_X

# Initial positions
agent_pos = [0, 0]  # Starting position of the agent
goal_pos = [4, 4]   # Goal position

# Spread obstacles throughout the grid
obstacle_positions = [(0, 2), (1, 1), (2, 3), (3, 4)]  # Obstacles scattered

# Q-values initialization
Q = np.zeros((GRID_SIZE_X, GRID_SIZE_Y, 4))  # 4 possible actions: up, down, left, right

# Reward settings
REWARD_GOAL = 100
REWARD_MOVE = -1
REWARD_OBSTACLE = -50
DISCOUNT_FACTOR = 0.9
LEARNING_RATE = 0.1

# Function to get next state and reward based on action
def get_next_state_and_reward(pos, action):
    next_pos = pos.copy()
    if action == 0 and pos[0] > 0:  # Up
        next_pos[0] -= 1
    elif action == 1 and pos[0] < GRID_SIZE_X - 1:  # Down
        next_pos[0] += 1
    elif action == 2 and pos[1] > 0:  # Left
        next_pos[1] -= 1
    elif action == 3 and pos[1] < GRID_SIZE_Y - 1:  # Right
        next_pos[1] += 1

    # Calculate reward
    if tuple(next_pos) in obstacle_positions:
        reward = REWARD_OBSTACLE
    elif next_pos == goal_pos:
        reward = REWARD_GOAL
    else:
        reward = REWARD_MOVE

    return next_pos, reward

# Q-learning update function
def q_learning_update():
    global agent_pos
    for episode in range(100):  # Number of episodes
        state = agent_pos
        while state != goal_pos:
            action = np.argmax(Q[state[0], state[1]])  # Choose action with max Q-value

            # Get next state and reward
            next_state, reward = get_next_state_and_reward(state, action)

            # Update Q-value using the Q-learning formula
            Q[state[0], state[1], action] += LEARNING_RATE * (reward + DISCOUNT_FACTOR * np.max(Q[next_state[0], next_state[1]]) - Q[state[0], state[1], action])

            state = next_state  # Move to the next state

# Function to draw the grid
def draw_grid():
    for i in range(GRID_SIZE_X):
        for j in range(GRID_SIZE_Y):
            rect = pygame.Rect(j * CELL_SIZE_X, i * CELL_SIZE_Y, CELL_SIZE_X, CELL_SIZE_Y)
            pygame.draw.rect(win, WHITE, rect, 1)

            if (i, j) == tuple(agent_pos):
                pygame.draw.rect(win, BLUE, rect)
            elif (i, j) == tuple(goal_pos):
                pygame.draw.rect(win, GREEN, rect)
            elif (i, j) in obstacle_positions:
                pygame.draw.rect(win, GRAY, rect)

# Game loop
def game_loop():
    global agent_pos
    running = True

    q_learning_update()  # Initialize Q-values through learning

    while running:
        win.fill(BLACK)
        draw_grid()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Follow policy using learned Q-values
        action = np.argmax(Q[agent_pos[0], agent_pos[1]])  # Choose action with max Q-value

        next_pos, reward = get_next_state_and_reward(agent_pos, action)

        # Update agent position if it's valid
        if tuple(next_pos) not in obstacle_positions:
            agent_pos = next_pos

        # Check if agent reached the goal
        if agent_pos == goal_pos:
            print("You reached the goal!")
            running = False

        # Output agent position
        print(f"Agent position: {agent_pos}")

        # Delay to slow down movement
        pygame.time.delay(500)

    pygame.quit()

# Run the game
game_loop()
