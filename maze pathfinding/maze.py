import random

class Maze:
    def __init__(self, rows=25, cols=35):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.goal = None
        self.generate_prim()

    # ---------------- BASIC CHECKS ----------------
    def is_in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_valid_cell(self, r, c):
        if not self.is_in_bounds(r, c):
            return False
        return self.grid[r][c] == 0

    # ---------------- GETTERS ----------------
    def get_start(self):
        return self.start

    def get_goal(self):
        return self.goal

    # ---------------- SETTERS ----------------
    def set_start(self, pos):
        r, c = pos
        if not self.is_valid_cell(r, c):
            raise ValueError("Start không hợp lệ (out of bounds hoặc là tường).")
        if self.goal == pos:
            raise ValueError("Start không được trùng với Goal.")
        self.start = pos
        self.grid[r][c] = 0

    def set_goal(self, pos):
        r, c = pos
        if not self.is_valid_cell(r, c):
            raise ValueError("Goal không hợp lệ (out of bounds hoặc là tường).")
        if self.start == pos:
            raise ValueError("Goal không được trùng với Start.")
        self.goal = pos
        self.grid[r][c] = 0

    # ---------------- WALL TOGGLE ----------------
    def toggle_wall(self, r, c):
        if self.grid[r][c] == 1:
            self.grid[r][c] = 0
        else:
            self.grid[r][c] = 1

    # ---------------- GENERATORS ----------------
    def generate_empty(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def generate_random(self, density=0.28):
        self.grid = [
            [1 if random.random() < density else 0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    # ---------------- PERFECT MAZE (PRIM) ----------------
    def generate_prim(self):
        # Khởi tạo toàn bộ là tường
        self.grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        # Chọn ô lẻ làm điểm bắt đầu
        r = random.randrange(1, self.rows, 2)
        c = random.randrange(1, self.cols, 2)
        self.grid[r][c] = 0

        walls = []

        # Thêm tường cách 2 ô
        def add_walls(rr, cc):
            for dr, dc in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                r2, c2 = rr + dr, cc + dc
                if self.is_in_bounds(r2, c2) and self.grid[r2][c2] == 1:
                    walls.append((rr, cc, r2, c2))

        add_walls(r, c)

        while walls:
            idx = random.randint(0, len(walls) - 1)
            r1, c1, r2, c2 = walls.pop(idx)

            if self.grid[r2][c2] == 1:
                # Mở tường ở giữa
                mid_r = (r1 + r2) // 2
                mid_c = (c1 + c2) // 2
                self.grid[mid_r][mid_c] = 0
                self.grid[r2][c2] = 0

                add_walls(r2, c2)

    # ---------------- GET WALL MAP ----------------
    def get_walls(self):
        return self.grid


# OPTIONAL: TEST (in ASCII)
if __name__ == "__main__":
    m = Maze(25, 35)
    for row in m.grid:
        print("".join("█" if cell == 1 else " " for cell in row))
