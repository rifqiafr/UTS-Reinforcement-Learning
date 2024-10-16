import pygame
import sys
import random

# Constants
GRID_SIZE = 5
CELL_SIZE = 100
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
START = (4, 2)
GOAL = (0, 4)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Grid definition
grid = [
    [0, 0, 0, 0, 3],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 2, 0, 0]
]

# Player starting position
player = list(START)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MDP AI Grid')
font = pygame.font.SysFont(None, 24)

# Transition Probability: 80% correct move, 20% random move
MOVE_PROB = 0.8

def draw_grid():
    """Menggambar grid berdasarkan nilai pada matriks `grid`."""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = WHITE
            if grid[i][j] == 1:
                color = GRAY  # Dinding
            elif grid[i][j] == 2:
                color = GREEN  # Reward
            elif grid[i][j] == 3:
                color = BLUE  # Goal
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_player():
    """Menggambar pemain sebagai lingkaran merah di posisi pemain saat ini."""
    pygame.draw.circle(screen, RED, (player[1] * CELL_SIZE + CELL_SIZE // 2, player[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

def display_details():
    """Menampilkan detail posisi pemain dan reward dari setiap aksi yang tersedia."""
    details = f"Current Position: ({player[0]}, {player[1]})"
    actions = ['up', 'down', 'left', 'right']
    for action in actions:
        next_state = get_next_state(player, action)
        if is_valid_move(next_state):
            reward = get_reward(next_state)
            details += f"\nMove {action}: Next State ({next_state[0]}, {next_state[1]}), Reward: {reward}"
        else:
            details += f"\nMove {action}: Invalid Move"
    detail_surf = font.render(details, True, BLACK)
    screen.blit(detail_surf, (10, HEIGHT + 10))

def get_next_state(state, action):
    """Mengembalikan posisi berikutnya berdasarkan aksi yang dilakukan."""
    x, y = state
    if action == 'up':
        x -= 1
    elif action == 'down':
        x += 1
    elif action == 'left':
        y -= 1
    elif action == 'right':
        y += 1
    return [x, y]

def is_valid_move(state):
    """Memeriksa apakah gerakan valid (tidak mengenai dinding atau keluar grid)."""
    x, y = state
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[x][y] != 1

def get_reward(state):
    """Menghitung reward berdasarkan posisi saat ini."""
    x, y = state
    if not is_valid_move(state):
        return -float('inf')  # Invalid move
    elif grid[x][y] == 3:
        return 10  # Goal tercapai
    elif grid[x][y] == 2:
        return 5  # Special reward cell
    else:
        return -manhattan_distance(state, GOAL)  # Penalti jarak ke goal

def manhattan_distance(state1, state2):
    """Menghitung jarak Manhattan antara dua posisi di grid."""
    return abs(state1[0] - state2[0]) + abs(state1[1] - state2[1])

def stochastic_transition(player, action):
    """Melakukan transisi stochastik dengan probabilitas transisi."""
    if random.random() < MOVE_PROB:  # 80% chance the intended action happens
        return get_next_state(player, action), action
    else:  # 20% chance to take a random action
        random_action = random.choice(['up', 'down', 'left', 'right'])
        return get_next_state(player, random_action), random_action

def ai_move(player):
    """Fungsi AI yang menggerakkan pemain berdasarkan jarak terdekat ke goal."""
    actions = ['up', 'down', 'left', 'right']
    best_move = None
    best_distance = float('inf')
    chosen_action = None

    for action in actions:
        next_pos, action_taken = stochastic_transition(player, action)  # Menggunakan transisi stochastik
        if is_valid_move(next_pos):
            distance = manhattan_distance(next_pos, GOAL)
            if distance < best_distance:
                best_distance = distance
                best_move = next_pos
                chosen_action = action_taken

    if best_move:
        print(f"Player moves {chosen_action} to position {best_move}")  # Output pergerakan
    return best_move if best_move else player

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI automatically moves the player using MDP
    next_pos = ai_move(player)
    if next_pos:
        player = next_pos

    # Check for goal reached
    if grid[player[0]][player[1]] == 3:
        print('Goal reached!')
        running = False

    screen.fill(WHITE)
    draw_grid()
    draw_player()
    display_details()
    pygame.display.flip()

    clock.tick(1)  # AI moves once per second

pygame.quit()
sys.exit()
