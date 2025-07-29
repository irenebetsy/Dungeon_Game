import time
from .constants import *
from .display import print_map, clear
from .map import create_grid, place_items, update_seen
from .save_load import load_level, save_level

def run_game():
    level = load_level()
    while True:
        size = min(6 + level // 3, 12)
        player_pos = (0, 0)
        grid = create_grid(size)
        grid = place_items(grid, player_pos)
        seen = [[False]*size for _ in range(size)]
        footsteps = set()
        lives = 2
        coins = 0
        update_seen(seen, player_pos, REVEAL_RADIUS)

        while True:
            clear()
            print(f"🎮 Level {level}    ❤️ Lives: {lives}   🪙 Coins: {coins}/3")
            print_map(grid, seen, footsteps, player_pos)

            move = input("Move (U/D/L/R) or type REVEAL or EXIT: ").upper()
            if move == 'EXIT':
                print("Exiting game...")
                save_level(level)
                return
            if move == 'REVEAL':
                for r in range(size):
                    for c in range(size):
                        seen[r][c] = True
                continue
            if move not in DIRS:
                continue

            dx, dy = DIRS[move]
            nx, ny = player_pos[0] + dx, player_pos[1] + dy
            if not (0 <= nx < size and 0 <= ny < size):
                continue

            footsteps.add(player_pos)

            seen[nx][ny] = True
            clear()
            print(f"🎮 Level {level}    ❤️ Lives: {lives}   🪙 Coins: {coins}/3")
            print("🕵️  You peek into the next tile...")
            print_map(grid, seen, footsteps, player_pos)
            time.sleep(1)
            seen[nx][ny] = False

            player_pos = (nx, ny)
            update_seen(seen, player_pos, REVEAL_RADIUS)

            tile = grid[nx][ny]
            if tile == GOAL:
                clear()
                print(f"🎉 Congrats! You completed Level {level}!")
                level += 1
                save_level(level)
                time.sleep(2)
                break
            elif tile == TRAP or tile == ENEMY:
                lives -= 1
                if lives == 0:
                    clear()
                    reason = "a trap" if tile == TRAP else "an enemy"
                    print(f"💀 You died by {reason}. Game over at Level {level}.")
                    save_level(1)
                    return
            elif tile == COIN:
                coins += 1
                grid[nx][ny] = EMPTY
