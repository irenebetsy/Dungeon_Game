import os

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def print_map(grid, seen, footsteps, player_pos):
    from .constants import PLAYER, FOOTSTEP
    print("\n📌 Dungeon Map:")
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[0])):
            if (r, c) == player_pos:
                row += PLAYER + " "
            elif (r, c) in footsteps:
                row += FOOTSTEP + " "
            elif seen[r][c]:
                row += grid[r][c] + " "
            else:
                row += "? "
        print(row)
    print("Legend: ❤️=Life  🪙=Coin  *=Trap  E=Enemy  G=Goal  C=Coin  +=Footstep  P=You")

def render_map(grid, seen, footsteps, player_pos,reveal_temp=False):
    from .constants import PLAYER, FOOTSTEP
    lines = []
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[0])):
            if (r, c) == player_pos:
                row += PLAYER
            elif (r, c) in footsteps:
                row += FOOTSTEP
            elif seen[r][c]:
                cell = grid[r][c]
                row += cell if cell else '.'
            else:
                row += '?'
        lines.append(row)
    return "\n".join(lines)

