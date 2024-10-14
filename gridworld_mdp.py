import pygame
import numpy as np
import random

# Inisialisasi pygame
pygame.init()

# Ukuran window
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (160, 160, 160)

# Ukuran grid
GRID_SIZE = 6
CELL_SIZE = WIDTH // GRID_SIZE

# Posisi awal agen dan target
agent_pos = [0, 0]
target_pos = [5, 5]

# Definisi rintangan di grid
obstacle_positions = [(2, 2), (3, 2), (3, 3), (4, 1), (1, 4)]

# Algoritma Value Iteration yang diperbaiki
def value_iteration(grid_size, obstacles, target, theta=0.001, discount_factor=0.9):
    V = np.zeros((grid_size, grid_size))
    policy = np.zeros((grid_size, grid_size))  # Kebijakan berisi 0-3 (up, down, left, right)
    
    # Arah aksi: up, down, left, right
    actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # (delta_row, delta_col)

    while True:
        delta = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if (i, j) == target:
                    continue  # Skip the terminal state
                if (i, j) in obstacles:
                    V[i, j] = -1000  # Penalti sangat besar untuk menabrak rintangan
                    continue

                old_v = V[i, j]
                q_values = []

                for action_idx, (di, dj) in enumerate(actions):
                    next_i, next_j = i + di, j + dj
                    
                    # Validasi agar tetap di dalam grid
                    if 0 <= next_i < grid_size and 0 <= next_j < grid_size:
                        if (next_i, next_j) in obstacles:
                            reward = -1000  # Penalti besar di sekitar rintangan
                        elif (next_i, next_j) == target:
                            reward = 1000  # Reward besar untuk mencapai tujuan
                        else:
                            # Reward lebih besar jika mendekati target
                            distance_to_goal = abs(next_i - target[0]) + abs(next_j - target[1])
                            reward = -1 + (-0.5 * distance_to_goal)
                        q_value = reward + discount_factor * V[next_i, next_j]
                        q_values.append(q_value)
                    else:
                        # Penalti besar jika mencoba keluar dari grid
                        q_values.append(-100)

                # Update nilai V dan kebijakan optimal
                V[i, j] = max(q_values)
                policy[i, j] = np.argmax(q_values)
                delta = max(delta, np.abs(old_v - V[i, j]))

        if delta < theta:
            break

    return V, policy

# Fungsi untuk menggambar grid
def draw_grid(agent_pos, obstacles, target_pos):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(win, WHITE, rect, 1)
            
            if [i, j] == agent_pos:
                pygame.draw.rect(win, BLUE, rect)
            elif [i, j] == target_pos:
                pygame.draw.rect(win, GREEN, rect)
            elif (i, j) in obstacles:
                pygame.draw.rect(win, GRAY, rect)

# Game loop
def game_loop():
    agent_pos = [0, 0]
    target_pos = [5, 5]
    obstacles = [(2, 2), (3, 2), (3, 3), (4, 1), (1, 4)]
    
    # Jalankan value iteration untuk menghitung kebijakan optimal
    V, policy = value_iteration(GRID_SIZE, obstacles, target_pos)

    stuck_counter = 0  # Counter untuk mendeteksi jika agen stuck
    running = True
    exploration_rate = 0.2  # Probabilitas untuk mencoba aksi acak
    max_exploration_rate = 0.5  # Probabilitas maksimum untuk eksplorasi acak
    while running:
        win.fill(BLACK)
        draw_grid(agent_pos, obstacles, target_pos)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Gerakan otomatis berdasarkan kebijakan optimal atau eksplorasi acak
        i, j = agent_pos
        
        if random.uniform(0, 1) < exploration_rate:
            # Eksplorasi acak
            action = random.randint(0, 3)
            print("Agen mencoba aksi acak!")
        else:
            # Menggunakan kebijakan optimal
            action = int(policy[i, j])

        # Arah gerakan berdasarkan kebijakan atau aksi acak
        if action == 0 and i > 0:  # up
            next_pos = [i - 1, j]
        elif action == 1 and i < GRID_SIZE - 1:  # down
            next_pos = [i + 1, j]
        elif action == 2 and j > 0:  # left
            next_pos = [i, j - 1]
        elif action == 3 and j < GRID_SIZE - 1:  # right
            next_pos = [i, j + 1]
        else:
            next_pos = agent_pos  # Jika tidak ada pergerakan valid

        # Jika agen terus berada di posisi yang sama, tambahkan penalti
        if next_pos == agent_pos:
            stuck_counter += 1
            reward = -10  # Penalti lebih besar jika agen stuck
            exploration_rate = min(max_exploration_rate, exploration_rate + 0.05)  # Tingkatkan eksplorasi
        else:
            stuck_counter = 0
            exploration_rate = max(0.1, exploration_rate - 0.05)  # Kurangi eksplorasi jika ada kemajuan

        # Hitung reward atau penalti untuk posisi berikutnya
        if tuple(next_pos) in obstacles:
            reward = -1000  # Penalti untuk menabrak rintangan
        elif next_pos == target_pos:
            reward = 1000  # Reward besar untuk mencapai tujuan
        else:
            reward = -1

        # Outputkan kebijakan dan reward
        print(f"Policy at position ({i}, {j}): {policy[i, j]}, Reward/Penalty: {reward}")
        
        # Update posisi agen
        agent_pos = next_pos

        # Jika agen stuck dalam jumlah langkah tertentu, coba aksi lain
        if stuck_counter > 5:
            print("Agen terjebak, memilih aksi lain.")
            stuck_counter = 0
            action = (action + 1) % 4  # Coba aksi lain
        
        # Cek apakah agen mencapai target
        if agent_pos == target_pos:
            print("You reached the goal!")
            running = False

        # Delay untuk memperlambat pergerakan
        pygame.time.delay(500)

    pygame.quit()

# Jalankan permainan
game_loop()
