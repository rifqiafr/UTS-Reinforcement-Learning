import pygame
import sys
import random
import numpy as np

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
    [0, 0, 0, 0, 3],  # 0: Empty space, 1: Wall, 2: Reward, 3: Goal
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 2, 0, 0]
]

# Player starting position
player = list(START)

# Initialize Q-table and Value Table
Q = np.zeros((GRID_SIZE, GRID_SIZE, 4))  # Q-Table: 4 actions (up, down, left, right)
V = np.zeros((GRID_SIZE, GRID_SIZE))  # Value Table untuk setiap state
gamma = 0.9  # Discount factor
theta = 0.0001  # Threshold untuk konvergensi Value Iteration
alpha = 0.1  # Learning rate untuk Q-Learning
epsilon = 0.2  # Exploration rate untuk Q-Learning

# Actions and directions
actions = ['up', 'down', 'left', 'right']
action_map = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Q-Learning + Value Iteration Grid')
font = pygame.font.SysFont(None, 24)

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

def value_iteration():
    """Algoritma value iteration untuk memperbarui nilai dari setiap state."""
    global V
    delta = float('inf')  # Perubahan maksimum antar iterasi
    
    while delta > theta:  # Lakukan sampai perubahan nilai menjadi sangat kecil (konvergen)
        delta = 0
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if grid[x][y] == 1:  # Jika ini dinding, lewati
                    continue
                v = V[x, y]  # Simpan nilai state saat ini
                
                # Evaluasi untuk setiap aksi, hitung nilai maksimal
                max_value = -float('inf')
                for action in actions:
                    next_state = get_next_state([x, y], action)
                    if is_valid_move(next_state):
                        reward = get_reward(next_state)
                        value = reward + gamma * V[next_state[0], next_state[1]]
                        if value > max_value:
                            max_value = value
                
                # Update nilai state dengan nilai terbaik dari semua aksi
                V[x, y] = max_value
                delta = max(delta, abs(v - V[x, y]))  # Update delta untuk mengecek konvergensi

def initialize_q_from_value():
    """Inisialisasi Q-table menggunakan value dari Value Iteration."""
    global Q
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] != 1:  # Bukan dinding
                for action_index, action in enumerate(actions):
                    next_state = get_next_state([x, y], action)
                    if is_valid_move(next_state):
                        reward = get_reward(next_state)
                        Q[x, y, action_index] = reward + gamma * V[next_state[0], next_state[1]]

def choose_action(state, epsilon):
    """Memilih action menggunakan epsilon-greedy strategy."""
    if random.uniform(0, 1) < epsilon:
        return random.choice([0, 1, 2, 3])  # Explore
    else:
        return np.argmax(Q[state[0], state[1]])  # Exploit

def update_q_table(state, action, reward, next_state):
    """Update Q-table menggunakan aturan Q-Learning."""
    next_max = np.max(Q[next_state[0], next_state[1]])  # Cari nilai maksimum di state berikutnya
    Q[state[0], state[1], action] = Q[state[0], state[1], action] + alpha * (reward + gamma * next_max - Q[state[0], state[1], action])

def print_grid():
    """Print the current grid state to the terminal."""
    print("\nCurrent Grid State:")
    for i in range(GRID_SIZE):
        row = ""
        for j in range(GRID_SIZE):
            if [i, j] == player:
                row += " P "  # Player's position
            elif grid[i][j] == 1:
                row += " # "  # Wall
            elif grid[i][j] == 3:
                row += " G "  # Goal
            elif grid[i][j] == 2:
                row += " R "  # Reward cell
            else:
                row += " . "  # Empty space
        print(row)

# Main game loop
running = True
clock = pygame.time.Clock()

# Lakukan value iteration terlebih dahulu untuk menghitung value table
value_iteration()

# Inisialisasi Q-table dari Value Table hasil Value Iteration
initialize_q_from_value()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pilih aksi terbaik untuk pemain menggunakan epsilon-greedy strategy
    action_index = choose_action(player, epsilon)
    action = action_map[action_index]
    
    next_pos = get_next_state(player, action)
    
    if is_valid_move(next_pos):
        reward = get_reward(next_pos)
        update_q_table(player, action_index, reward, next_pos)
        player = next_pos  # Pindahkan pemain

        # Cetak kondisi grid ke terminal
        print_grid()

    # Check for goal reached
    if grid[player[0]][player[1]] == 3:
        print('Goal reached!')
        running = False

    screen.fill(WHITE)
    draw_grid()
    draw_player()
    pygame.display.flip()

    clock.tick(1)  # AI moves once per second

pygame.quit()
sys.exit()