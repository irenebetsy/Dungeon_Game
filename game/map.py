import random
from .constants import EMPTY, GOAL, TRAP, ENEMY, COIN

def create_grid(size):
    return [[EMPTY for _ in range(size)] for _ in range(size)]

def place_items(grid, player_pos):
    size = len(grid)
    items = [GOAL] + [TRAP]*3 + [ENEMY]*2 + [COIN]*3
    for item in items:
        while True:
            r, c = random.randint(0, size-1), random.randint(0, size-1)
            if grid[r][c] == EMPTY and (r, c) != player_pos:
                grid[r][c] = item
                break
    return grid

def update_seen(seen, pos, radius):
    x, y = pos
    for dx in range(-radius, radius+1):
        for dy in range(-radius, radius+1):
            nx, ny = x+dx, y+dy
            if 0 <= nx < len(seen) and 0 <= ny < len(seen):
                seen[nx][ny] = True
