# main.py
import pygame
import sys
import time
import math
from maze import Maze
from solver import Solver 
pygame.init()
pygame.font.init()
# Cấu hình config window
CELL_SIZE = 24
ROWS, COLS = 25, 35
PANEL_WIDTH = 320
WIDTH = COLS * CELL_SIZE + PANEL_WIDTH
HEIGHT = ROWS * CELL_SIZE
# Màu
COLOR_FREE = (245, 245, 245)
COLOR_WALL_BG = (50, 50, 50)
COLOR_PANEL = (45, 45, 45)
COLOR_TEXT = (230, 230, 230)
COLOR_PATH_BG = (255, 245, 220)
COLOR_VISITED_BG = (220, 235, 255)
# Phông chữ
MAIN_FONT = pygame.font.SysFont("consolas", 18)
TITLE_FONT = pygame.font.SysFont("consolas", 22, bold=True)
# Emoji
EMOJI_START = "🤖"
EMOJI_GOAL = "🎯"
EMOJI_PATH = "⭐"
EMOJI_VISITED = "🔵"
WALL_ICONS = ["🧱", "🌳", "🏠", "🚧", "🏢"]
# =============================================================
def load_emoji_font(size):
    """
    Tải dữ liệu font để hiện icon vật thể.
    """
    candidates = [
        "NotoColorEmoji.ttf",
        "Segoe UI Emoji.ttf",
        "seguiemj.ttf",
        "Apple Color Emoji.ttc",
        "NotoEmoji-Regular.ttf",
        "Symbola.ttf",
    ]
    for name in candidates:
        try:
            return pygame.font.Font(name, size)
        except Exception:
            pass
    sys_candidates = [
        "Segoe UI Emoji",
        "Noto Color Emoji",
        "Apple Color Emoji",
        "Symbola",
        "EmojiOne Mozilla",
    ]
    for name in sys_candidates:
        try:
            return pygame.font.SysFont(name, size)
        except Exception:
            pass

    return pygame.font.SysFont("arial", size)
EMOJI_FONT = load_emoji_font(int(CELL_SIZE * 0.9))
class GUI:
    def __init__(self):
        # start in resizable windowed mode
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Tìm đường mê cung 🧩➡️🎯")
        # Canvas: logical drawing area (we will scale to window size)
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.windowed_size = (WIDTH, HEIGHT)
        self.is_fullscreen = False
        # Maze + start/goal
        self.maze = Maze(ROWS, COLS)
        self.start = None
        self.goal = None
        # visited & path state
        self.visited = set()
        self.path = []
        # reveal-path animation (draw path gradually)
        self.reveal_path = []
        self.path_reveal_start = None
        # animation timestamps
        self.anim_visited_time = {}
        self.anim_path_time = {}
        # solver related
        self.solver_generator = None
        self.solver_start_time = None
        self.solver_live_time_ms = None
        # algorithm & stats
        self.current_algo = "bfs"
        self.last_stats = {}
        # UI
        self.show_wall_icons = True    # Trạng thái tường emoji/icon
        self.use_generator_mode = True # True = generator (hiệu ứng), False = batch (tức thì)
        self.status_message = ""
        # wave animation base time (for subtle per-cell variation)
        self.wave_start_time = time.time()

    # các hiệu ứng nền
    def ease_out(self, t: float) -> float:
        return 1 - (1 - t) * (1 - t)
    def blend(self, c1, c2, t: float):
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )

    def apply_brightness(self, color, factor: float):
        return (
            max(0, min(255, int(color[0] * factor))),
            max(0, min(255, int(color[1] * factor))),
            max(0, min(255, int(color[2] * factor))),
        )

    def random_wave(self, r: int, c: int) -> float:
        t = (time.time() - self.wave_start_time)
        phase = (r * 7 + c * 13) * 0.12
        v = math.sin(t * 2.0 + phase)  # -1 .. 1
        return 1.0 + 0.15 * v
    # ---------------- dynamic cell sizing (for window resize) ----
    def update_cell_size(self):
        """
        Recalculate CELL_SIZE whenever window size changes (keeps crisp rendering).
        This mutates global CELL_SIZE, WIDTH, HEIGHT and reloads EMOJI_FONT.
        """
        win_w, win_h = self.get_window_size()
        # usable grid area (exclude panel)
        grid_w = max(100, win_w - PANEL_WIDTH)
        grid_h = max(100, win_h)
        new_cell_w = grid_w // COLS
        new_cell_h = grid_h // ROWS
        new_size = max(8, min(new_cell_w, new_cell_h))
        global CELL_SIZE, EMOJI_FONT, WIDTH, HEIGHT
        CELL_SIZE = new_size
        EMOJI_FONT = load_emoji_font(int(CELL_SIZE * 0.9))
        WIDTH = COLS * CELL_SIZE + PANEL_WIDTH
        HEIGHT = ROWS * CELL_SIZE
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
    def get_window_size(self):
        return self.screen.get_size()
    # chức năng vẽ emoji
    def draw_emoji_at(self, emoji: str, rect: pygame.Rect):
        """
        Render emoji centered in rect. If emoji font missing, fallback to MAIN_FONT.
        """
        try:
            surf = EMOJI_FONT.render(emoji, True, (255, 255, 255))
        except Exception:
            surf = MAIN_FONT.render(emoji, True, (255, 255, 255))
        sw, sh = surf.get_size()
        x = rect.x + (rect.width - sw) // 2
        y = rect.y + (rect.height - sh) // 2 - 1
        self.canvas.blit(surf, (x, y))
    # =========================================================
    # Cập nhật hiệu ứng đường đi (hoạt ảnh)
    # =========================================================
    def update_path_reveal(self):
        if not self.path or self.path_reveal_start is None:
            return
        speed = 35
        elapsed = time.time() - self.path_reveal_start
        expected_len = int(elapsed * speed)
        if expected_len > len(self.reveal_path):
            expected_len = min(expected_len, len(self.path))
            new_segment = self.path[len(self.reveal_path):expected_len]
            self.reveal_path.extend(new_segment)
            now = time.time()
            for cell in new_segment:
                self.anim_path_time[cell] = now
    # =========================================================
    # DRAW GRID (include START = green background, GOAL = red background)
    # =========================================================
    def draw_grid(self):
        self.canvas.fill((0, 0, 0))
        is_dim = (self.solver_generator is not None)  # làm mờ nền khi thuật toán chạy
        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(
                    c * CELL_SIZE, r * CELL_SIZE,
                    CELL_SIZE - 1, CELL_SIZE - 1
                )
                cell_val = self.maze.grid[r][c]
                wave = self.random_wave(r, c)
                # Điểm start
                if self.start == (r, c):
                    base = (20, 120, 20)   # xanh lá
                    bg = self.apply_brightness(base, wave)
                    pygame.draw.rect(self.canvas, bg, rect)

                    emoji = EMOJI_FONT.render(EMOJI_START, True, (255, 255, 255))
                    sw, sh = emoji.get_size()
                    x = rect.x + (rect.width - sw) // 2
                    y = rect.y + (rect.height - sh) // 2
                    self.canvas.blit(emoji, (x, y))

                    if is_dim:
                        dim = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                        dim.fill((0, 0, 0, 70))
                        self.canvas.blit(dim, (rect.x, rect.y))
                    continue
                # Điểm goal
                if self.goal == (r, c):
                    base = (160, 20, 20)  # đỏ
                    bg = self.apply_brightness(base, wave)
                    pygame.draw.rect(self.canvas, bg, rect)

                    emoji = EMOJI_FONT.render(EMOJI_GOAL, True, (255, 255, 255))
                    sw, sh = emoji.get_size()
                    x = rect.x + (rect.width - sw) // 2
                    y = rect.y + (rect.height - sh) // 2
                    self.canvas.blit(emoji, (x, y))

                    if is_dim:
                        dim = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                        dim.fill((0, 0, 0, 70))
                        self.canvas.blit(dim, (rect.x, rect.y))
                    continue
                # Vẽ đường đi ngắn nhất
                if (r, c) in self.reveal_path:
                    t0 = self.anim_path_time.get((r, c), time.time())
                    t = min((time.time() - t0) / 0.25, 1)
                    t = self.ease_out(t)

                    base = self.blend((255, 255, 170), COLOR_PATH_BG, t)
                    glow = 1.0 + 0.15 * math.sin(time.time() * 6 + r * 0.3 + c * 0.5)
                    col = self.apply_brightness(base, glow)

                    pygame.draw.rect(self.canvas, col, rect)
                    self.draw_emoji_at(EMOJI_PATH, rect)
                    continue
                # Điểm đã đi qua
                if (r, c) in self.visited:
                    t0 = self.anim_visited_time.get((r, c), time.time())
                    t = min((time.time() - t0) / 0.25, 1)
                    t = self.ease_out(t)

                    col = self.blend((255, 255, 255), COLOR_VISITED_BG, t)
                    col = self.apply_brightness(
                        col,
                        1.0 + 0.06 * math.sin(time.time() * 3 + r * 0.3 + c * 0.4)
                    )
                    pygame.draw.rect(self.canvas, col, rect)
                    self.draw_emoji_at(EMOJI_VISITED, rect)
                    continue
                # Tường
                if cell_val == 1:
                    col = self.apply_brightness(COLOR_WALL_BG, wave)
                    pygame.draw.rect(self.canvas, col, rect)
                    if self.show_wall_icons:
                        icon = WALL_ICONS[(r + c) % len(WALL_ICONS)]
                        self.draw_emoji_at(icon, rect)
                    if is_dim:
                        dim = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                        dim.fill((0, 0, 0, 128))
                        self.canvas.blit(dim, (rect.x, rect.y))
                    continue
                # Đường có thể đi
                col = self.apply_brightness(COLOR_FREE, wave)
                pygame.draw.rect(self.canvas, col, rect)
                if is_dim:
                    dim = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    dim.fill((0, 0, 0, 128))
                    self.canvas.blit(dim, (rect.x, rect.y))
    # Bảng UI thông tin
    def draw_panel(self):
        x_panel = COLS * CELL_SIZE
        pygame.draw.rect(self.canvas, COLOR_PANEL, (x_panel, 0, PANEL_WIDTH, HEIGHT))
        y = 14
        self.canvas.blit(TITLE_FONT.render("Bảng thông tin", True, COLOR_TEXT),
                         (x_panel + 16, y))
        y += 40
        algos = ["bfs", "dfs", "dijkstra", "astar"]
        for i, a in enumerate(algos, start=1):
            color = (180, 255, 180) if a == self.current_algo else COLOR_TEXT
            text = f"{i}: {a.upper()}"
            self.canvas.blit(MAIN_FONT.render(text, True, color),
                             (x_panel + 18, y))
            y += 26
        y += 10
        v_now = len(self.visited)
        p_now = len(self.reveal_path)
        self.canvas.blit(MAIN_FONT.render(f"Điểm đi qua: {v_now}", True, COLOR_TEXT),
                         (x_panel + 18, y)); y += 24
        self.canvas.blit(MAIN_FONT.render(f"Độ dài đường đi: {p_now}", True, COLOR_TEXT),
                         (x_panel + 18, y)); y += 24
        # Thời gian
        if self.solver_generator:
            ms = int((time.time() - self.solver_start_time) * 1000)
            self.canvas.blit(MAIN_FONT.render(f"Thực: {ms} ms", True, COLOR_TEXT),
                             (x_panel + 18, y))
        else:
            t = self.solver_live_time_ms if self.solver_live_time_ms is not None else "-"
            self.canvas.blit(MAIN_FONT.render(f"Cuối: {t}", True, COLOR_TEXT),
                             (x_panel + 18, y))
        y += 34
        # Kết quả cuối
        self.canvas.blit(MAIN_FONT.render("Kết quả cuối:", True, COLOR_TEXT),
                         (x_panel + 18, y))
        y += 26
        for a in algos:
            st = self.last_stats.get(a)
            if st:
                line = f"{a.upper()}: {st['time_ms']}ms | v={st['visited_count']} | p={st['path_len']}"
            else:
                line = f"{a.upper()}: -"
            self.canvas.blit(MAIN_FONT.render(line, True, COLOR_TEXT),
                             (x_panel + 18, y))
            y += 22
        y += 24
        self.canvas.blit(MAIN_FONT.render(f"Trạng thái: {self.status_message}", True, COLOR_TEXT),
                         (x_panel + 18, y))
        y += 26
        self.canvas.blit(MAIN_FONT.render("Hướng dẫn:", True, COLOR_TEXT),
                         (x_panel + 18, y))
        y += 22
        for line in [
            "Chuột trái: đặt tường",
            "S: đặt Start",
            "G: đặt Goal",
            "R: tạo mới",
            "Space: tìm đường",
            "1-4: chọn thuật toán",
            "W: hiện/ẩn vật thể",
            "B: chế độ batch/generator",
        ]:
            self.canvas.blit(MAIN_FONT.render(line, True, COLOR_TEXT),
                             (x_panel + 18, y))
            y += 22
    #Chạy
    def start_solver(self):
        if not self.start or not self.goal:
            return
        solver = Solver(self.maze.grid)
        self.visited.clear()
        self.path = []
        self.reveal_path = []
        self.anim_visited_time.clear()
        self.anim_path_time.clear()
        self.wave_start_time = time.time()
        # batch mode / generator mode
        if self.use_generator_mode:
            self.solver_generator = solver.solve(
                self.start, self.goal,
                mode=self.current_algo,
                as_generator=True
            )
        else:
            visited_order, parent, path = solver.solve(
                self.start, self.goal,
                mode=self.current_algo,
                as_generator=False
            )
            self.visited = set(visited_order)
            self.path = path
            self.reveal_path = []
            self.path_reveal_start = time.time()
            self.solver_live_time_ms = 0
            self.solver_generator = None
        self.solver_start_time = time.time()
        self.status_message = f"Đang chạy: {self.current_algo.upper()}..."
        if not self.use_generator_mode:
            # store stats for batch
            self.last_stats[self.current_algo] = {
                "time_ms": 0,
                "visited_count": len(self.visited),
                "path_len": len(self.path),
            }
    # Cập nhật mode
    def update_solver(self):
        if not self.solver_generator:
            return
        try:
            node = next(self.solver_generator)
            self.visited.add(node)
            self.anim_visited_time[node] = time.time()
        except StopIteration as e:
            result = e.value if hasattr(e, "value") else e
            if isinstance(result, dict):
                self.path = result.get("path", [])
                visited_count = result.get("visited_count", 0)
                time_ms = result.get("time_ms", 0)
                now = time.time()
                self.anim_path_time = {p: now for p in self.path}
                self.last_stats[self.current_algo] = {
                    "time_ms": int(time_ms),
                    "visited_count": visited_count,
                    "path_len": len(self.path),
                }
                self.solver_live_time_ms = int(time_ms)
                self.reveal_path = []
                self.path_reveal_start = time.time()
            self.visited.clear()
            self.anim_visited_time.clear()
            self.solver_generator = None
            self.solver_start_time = None
            if not self.path:
                self.status_message = "Không tìm được đường đi"
            else:
                self.status_message = "Đã tìm được đường đi!"
    # Trạng thái key input từ phím / chuột
    def handle_mouse_logical(self, lx, ly, button):
        if lx >= COLS * CELL_SIZE:
            return
        r = ly // CELL_SIZE
        c = lx // CELL_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS:
            # nếu không thay đổi được start / goal
            if (r, c) == self.start or (r, c) == self.goal:
                return
            if button == 1:
                self.maze.toggle_wall(r, c)
                self.status_message = ""
    # Chức năng cửa sổ
    def get_window_size(self):
        return self.screen.get_size()
    def window_to_logical(self, x, y):
        win_w, win_h = self.get_window_size()
        if win_w == 0 or win_h == 0:
            return x, y
        lx = int(x * WIDTH / win_w)
        ly = int(y * HEIGHT / win_h)
        return lx, ly
    # Đặt lại tất cả
    def reset_all(self):
        self.maze = Maze(ROWS, COLS)
        self.start = None
        self.goal = None
        self.visited.clear()
        self.path.clear()
        self.reveal_path.clear()
        self.anim_visited_time.clear()
        self.anim_path_time.clear()
        self.solver_generator = None
        self.solver_start_time = None
        self.solver_live_time_ms = None
        self.path_reveal_start = None
        self.status_message = ""
    # Chương trình chính
    def run(self):
        mode_setter = None
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Thay đổi kích cỡ cửa sổ
                if event.type == pygame.VIDEORESIZE:
                    new_size = (event.w, event.h)
                    self.windowed_size = new_size
                    self.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)
                    self.is_fullscreen = False
                    self.update_cell_size()
                # Key chuột
                if event.type == pygame.MOUSEBUTTONDOWN:
                    lx, ly = self.window_to_logical(*event.pos)
                    if mode_setter == "start":
                        r, c = ly // CELL_SIZE, lx // CELL_SIZE
                        if self.maze.is_valid_cell(r, c):
                            self.start = (r, c)
                        self.status_message = ""
                        mode_setter = None
                    elif mode_setter == "goal":
                        r, c = ly // CELL_SIZE, lx // CELL_SIZE
                        if self.maze.is_valid_cell(r, c):
                            self.goal = (r, c)
                        self.status_message = ""
                        mode_setter = None
                    else:
                        self.handle_mouse_logical(lx, ly, event.button)
                # Key đã nhấn
                if event.type == pygame.KEYDOWN:
                    # SET START
                    if event.key == pygame.K_s:
                        mode_setter = "start"
                        self.status_message = "Đặt Start..."
                    # SET GOAL
                    elif event.key == pygame.K_g:
                        mode_setter = "goal"
                        self.status_message = "Đặt Goal..."
                    # RESET
                    elif event.key == pygame.K_r:
                        self.reset_all()
                    # WALL ICON TOGGLE
                    elif event.key == pygame.K_w:
                        self.show_wall_icons = not self.show_wall_icons
                        self.status_message = (
                            "ẨN vật thể" if not self.show_wall_icons else "HIỆN vật thể"
                        )
                    # START SOLVER
                    elif event.key == pygame.K_SPACE:
                        self.start_solver()
                    # SWITCH ALGORITHM
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        if self.solver_generator:
                            self.status_message = "Không thể đổi khi đang chạy!"
                            break
                        if event.key == pygame.K_1:
                            self.current_algo = "bfs"
                        elif event.key == pygame.K_2:
                            self.current_algo = "dfs"
                        elif event.key == pygame.K_3:
                            self.current_algo = "dijkstra"
                        elif event.key == pygame.K_4:
                            self.current_algo = "astar"
                        self.status_message = f"Thuật toán: {self.current_algo.upper()}"
                    # SWITCH batch / generator mode
                    elif event.key == pygame.K_b:
                        if self.solver_generator:
                            self.status_message = "Đợi chạy xong đã!"
                        else:
                            self.use_generator_mode = not self.use_generator_mode
                            mode = "GENERATOR" if self.use_generator_mode else "BATCH"
                            self.status_message = f"Chế độ: {mode}"
            # cập nhật cách tìm đường
            if self.solver_generator:
                self.update_solver()
            # cập nhật đường đi với hiệu ứng
            self.update_path_reveal()
            # vẽ
            self.draw_grid()
            self.draw_panel()
            # scale với window
            win_w, win_h = self.get_window_size()
            scaled = pygame.transform.smoothscale(self.canvas, (win_w, win_h))
            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()
if __name__ == "__main__":
    gui = GUI()
    gui.run()