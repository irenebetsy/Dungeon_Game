import time
from .constants import *
from .display import clear
from .map import create_grid, place_items, update_seen
from .save_load import load_level, save_level

class GameEngine:
    def __init__(self):
        self.level = load_level()
        self.size = min(6 + self.level // 3, 12)
        self.grid = create_grid(self.size)
        self.player_pos = (0, 0)
        self.grid = place_items(self.grid, self.player_pos)
        self.seen = [[False] * self.size for _ in range(self.size)]
        self.footsteps = set()
        self.lives = 2
        self.coins = 0
        update_seen(self.seen, self.player_pos, REVEAL_RADIUS)
        self.reveal_temp = False
        self.game_over = False
        self.victory = False
        self.msg = ""
        

    def to_dict(self):
        return {
            "level": self.level,
            "size": self.size,
            "grid": self.grid,
            "player_pos": self.player_pos,
            "seen": self.seen,
            "footsteps": list(self.footsteps),
            "lives": self.lives,
            "coins": self.coins,
            "game_over": self.game_over,
            "reveal_temp":self.reveal_temp
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls.__new__(cls)
        obj.level = data["level"]
        obj.size = data["size"]
        obj.grid = data["grid"]
        obj.player_pos = tuple(data["player_pos"])
        obj.seen = data["seen"]
        obj.footsteps = set(tuple(x) for x in data["footsteps"])
        obj.lives = data["lives"]
        obj.coins = data["coins"]
        obj.game_over = data.get("game_over", False)
        obj.victory = False
        obj.msg = ""
        obj.reveal_temp = data.get("reveal_temp", False)
        return obj

    def move(self, direction):
        if self.game_over:
            return
        if direction not in DIRS:
            return

        dx, dy = DIRS[direction]
        nx, ny = self.player_pos[0] + dx, self.player_pos[1] + dy

        if not (0 <= nx < self.size and 0 <= ny < self.size):
            self.msg = "❌ Invalid move!"
            return

        self.footsteps.add(self.player_pos)
        self.seen[nx][ny] = True
        self.player_pos = (nx, ny)
        update_seen(self.seen, self.player_pos, REVEAL_RADIUS)

        tile = self.grid[nx][ny]
        if tile == GOAL:
            self.msg = f"🎉 Congrats! You completed Level {self.level}! Level {self.level+1} Started..."
            self.level += 1
            save_level(self.level)
            self.victory = True
            self.reset_game()

            """# Reset state for next level
            self.size = min(6 + self.level // 3, 12)
            self.grid = create_grid(self.size)
            self.player_pos = (0, 0)
            self.grid = place_items(self.grid, self.player_pos)
            self.seen = [[False] * self.size for _ in range(self.size)]
            self.footsteps = set()
            self.coins = 0
            self.reveal_temp = False
            self.game_over = False
            update_seen(self.seen, self.player_pos, REVEAL_RADIUS)
            self.msg += f"\n🎮 Level {self.level} started!"
            return"""
        
        elif tile == TRAP:
            if self.lives>0:
                self.lives -= 1
            self.msg = "💥 Ouch! You stepped on a trap!"
        elif tile == ENEMY:
            if self.lives>0:
                self.lives -= 1
            self.msg = "👹 An enemy attacked you!"
        elif tile == COIN:
            self.coins += 1
            self.grid[nx][ny] = EMPTY
            self.msg = "🪙 Coin collected!"
        else:
            self.msg = "✅ You moved."

        if self.lives <= 0:
            self.msg += f"💀 You died at Level {self.level}!"
            save_level(self.level)
            self.game_over = True
            self.reset_game(level=self.level)
            self.msg += f"🔁Level {self.level} Restarted..."

    def reset_game(self, level=None):
        if level is not None:
            self.level = level
        self.size = min(6 + self.level // 3, 12)
        self.grid = create_grid(self.size)
        self.player_pos = (0, 0)
        self.grid = place_items(self.grid, self.player_pos)
        self.seen = [[False] * self.size for _ in range(self.size)]
        self.footsteps = set()
        self.lives = 2
        self.coins = 0
        self.reveal_temp = False
        self.game_over = False
        self.victory = False
        #self.msg = ""
        update_seen(self.seen, self.player_pos, REVEAL_RADIUS)


    def reveal_all(self):
        for r in range(self.size):
            for c in range(self.size):
                self.seen[r][c] = True
        self.msg = "👁️ Full map revealed!"
    
    def handle_input(self, action):
        if self.game_over:
            self.reset_game(level=self.level)
            return self.msg

        if action in ["U", "D", "L", "R"]:
            self.move(action)
        elif action == "REVEAL":
            self.reveal_all()

        elif action == "EXIT":
            self.msg = "🚪 You exited the game."
        else:
            self.msg = "❓ Unknown command"

        return self.msg

        
