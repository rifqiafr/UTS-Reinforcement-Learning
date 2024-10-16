import pygame
import numpy as np
import random
import sys

# Constants
GRID_SIZE = 5
CELL_SIZE = 100
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
START = (4, 2)  # Posisi awal sesuai dengan layout baru
GOAL = (0, 4)   # Posisi goal sesuai dengan layout baru

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define the grid (layout baru)
grid = [
    [0, 0, 0, 0, 3],  # 3: Goal
    [0, 1, 1, 0, 0],  # 1: Wall
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 2, 0, 0]   # 2: Starting position
]

# Robot starting position
robot = list(START)

# Define parameters for Policy Iteration
actions = ['up', 'down', 'left', 'right']
action_map = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
gamma = 0.9  # Discount factor
theta = 0.0001  # Threshold for convergence
policy = np.random.choice([0, 1, 2, 3], size=(GRID_SIZE, GRID_SIZE))  # Random initial policy
V = np.zeros((GRID_SIZE, GRID_SIZE))  # Initialize value table

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Grindworld (Policy Iteration)")
font = pygame.font.SysFont(None, 24)

def draw_grid():
    """Draw the grid grid."""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = WHITE
            if grid[i][j] == 1:
                color = GRAY  # Wall
            elif grid[i][j] == 3:
                color = BLUE  # Goal
            elif grid[i][j] == 2:
                color = GREEN  # Start
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_robot():
    """Draw the robot as a red circle."""
    pygame.draw.circle(screen, RED, (robot[1] * CELL_SIZE + CELL_SIZE // 2, robot[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

def get_next_state(state, action):
    """Returns the next state based on the current state and action."""
    x, y = state
    if action == 'up' and x > 0:
        x -= 1
    elif action == 'down' and x < GRID_SIZE - 1:
        x += 1
    elif action == 'left' and y > 0:
        y -= 1
    elif action == 'right' and y < GRID_SIZE - 1:
        y += 1
    return [x, y]

def is_valid_move(state):
    """Check if a move is valid (not hitting a wall or out of bounds)."""
    x, y = state
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[x][y] != 1

def get_reward(state):
    """Returns the reward for reaching a given state."""
    x, y = state
    if grid[x][y] == 3:  # Reaching the goal
        return 10
    else:
        return -1  # Default step cost

def policy_evaluation():
    """Policy evaluation step: updates the value function based on the current policy."""
    global V
    while True:
        delta = 0
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if grid[x][y] == 1:  # Skip walls
                    continue
                v = V[x, y]
                action = policy[x, y]
                next_state = get_next_state([x, y], action_map[action])
                if is_valid_move(next_state):
                    reward = get_reward(next_state)
                    V[x, y] = reward + gamma * V[next_state[0], next_state[1]]
                delta = max(delta, abs(v - V[x, y]))
        if delta < theta:
            break

def policy_improvement():
    """Policy improvement step: updates the policy to be greedy with respect to the value function."""
    policy_stable = True
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == 1:  # Skip walls
                continue
            old_action = policy[x, y]
            best_action = old_action
            best_value = -float('inf')
            for action_index, action in enumerate(actions):
                next_state = get_next_state([x, y], action)
                if is_valid_move(next_state):
                    reward = get_reward(next_state)
                    value = reward + gamma * V[next_state[0], next_state[1]]
                    if value > best_value:
                        best_value = value
                        best_action = action_index
            policy[x, y] = best_action
            if old_action != best_action:
                policy_stable = False
    return policy_stable

def policy_iteration():
    """Performs Policy Iteration: alternating between Policy Evaluation and Policy Improvement."""
    while True:
        policy_evaluation()
        if policy_improvement():
            break

def print_grid():
    """Print the current grid state to the terminal."""
    print("\nCurrent grid State:")
    for i in range(GRID_SIZE):
        row = ""
        for j in range(GRID_SIZE):
            if [i, j] == robot:
                row += " R "  # Robot's position
            elif grid[i][j] == 1:
                row += " # "  # Wall
            elif grid[i][j] == 3:
                row += " G "  # Goal
            else:
                row += " . "  # Free space
        print(row)

# Run Policy Iteration once to get an optimal policy
policy_iteration()

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the robot according to the optimal policy
    best_action = action_map[policy[robot[0], robot[1]]]
    next_pos = get_next_state(robot, best_action)
    
    if is_valid_move(next_pos):
        robot = next_pos  # Move the robot
    
    # Print the current grid state to the terminal
    print_grid()

    # Check if the robot reaches the goal
    if grid[robot[0]][robot[1]] == 3:
        print("Goal reached!")
        running = False

    # Draw the game state
    screen.fill(WHITE)
    draw_grid()
    draw_robot()
    pygame.display.flip()

    clock.tick(2)  # Move the robot every 2 seconds

pygame.quit()
sys.exit()
