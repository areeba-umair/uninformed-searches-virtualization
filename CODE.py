import pygame
from collections import deque
import heapq
#the perfect code 
# --- Configuration (Point 4 & User Requirements) ---
WIDTH, HEIGHT = 600, 650
GRID_SIZE = 10 
CELL_SIZE = WIDTH // GRID_SIZE
TITLE = "SEARCHES VISULIZATION"

# Visualization Colors
BG_GRAY = (211, 211, 211)  # Default cell color (0)
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GREEN, BLUE = (46, 204, 113), (52, 152, 219) # Start (S), Target (T)
YELLOW = (241, 196, 15)                      # Frontier (Point 4.1)
EXPLORED_COLOR = (180, 180, 180)             # Explored (Point 4.2)
PATH_COLOR = (155, 89, 182)                  # Final Path (Point 4.3)

class AIPathfinder:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.font = pygame.font.SysFont('Arial', 18, bold=True)
        self.reset_all()

    def reset_all(self):
        self.start = None
        self.target = None
        self.reset_search_data()

    def reset_search_data(self):
        self.frontier, self.explored = [], set()
        self.path, self.parent = [], {}

    def get_neighbors(self, node):
        """
        STRICT CLOCKWISE ORDER (Main Diagonal only):
        1. Up (-1, 0)
        2. Right (0, 1)
        3. Bottom (1, 0)
        4. Bottom-Right (1, 1)
        5. Left (0, -1)
        6. Top-Left (-1, -1)
        """
        r, c = node
        # The specific 6 directions requested
        directions = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]
        res = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                res.append((nr, nc))
        return res

    def draw(self, status="1st Click: Start | 2nd Click: Target"):
        self.screen.fill(WHITE)
        # Status Text
        txt = self.font.render(status, True, BLACK)
        self.screen.blit(txt, (10, 10))
        # Controls Text
        ctrl = self.font.render("1-BFS, 2-DFS, 3-UCS, 4-DLS, 5-IDDFS, 6-Bidir | R-Reset", True, (80,80,80))
        self.screen.blit(ctrl, (10, 30))

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)
                p = (r, c)
                color, label = BG_GRAY, "0"
                
                # Visual hierarchy
                if p == self.start: color, label = GREEN, "S"
                elif p == self.target: color, label = BLUE, "T"
                elif p in self.path: color = PATH_COLOR
                elif p in self.frontier: color = YELLOW
                elif p in self.explored: color = EXPLORED_COLOR
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1) # Grid lines
                l_surf = self.font.render(label, True, BLACK)
                self.screen.blit(l_surf, l_surf.get_rect(center=rect.center))
        pygame.display.flip()

    def animate(self, name):
        """Point 4.4: Dynamic updates with slight delay"""
        self.draw(f"Search: {name} (Running...)")
        pygame.time.delay(70)

    def reconstruct(self, node=None, p_map=None):
        m = p_map if p_map else self.parent
        curr = node if node else self.target
        while curr in m and m[curr] is not None:
            self.path.append(curr)
            curr = m[curr]
        self.draw("Search Complete: Path Found")

    # --- Search Algorithms (Strict Order Applied) ---

    def run_bfs(self):
        if not self.start or not self.target: return
        self.reset_search_data()
        q = deque([self.start])
        self.parent = {self.start: None}
        self.explored.add(self.start)
        while q:
            curr = q.popleft()
            for n in self.get_neighbors(curr):
                if n not in self.explored:
                    self.parent[n] = curr
                    if n == self.target: return self.reconstruct(n)
                    self.explored.add(n)
                    q.append(n)
            self.frontier = list(q)
            self.animate("BFS")

    def run_dfs(self):
        if not self.start or not self.target: return
        self.reset_search_data()
        stack = [self.start]
        self.parent = {self.start: None}
        while stack:
            curr = stack.pop()
            if curr == self.target: return self.reconstruct()
            if curr not in self.explored:
                self.explored.add(curr)
                # Reverse to keep clockwise priority in LIFO stack
                for n in reversed(self.get_neighbors(curr)):
                    if n not in self.explored:
                        self.parent[n] = curr
                        stack.append(n)
                self.frontier = list(stack)
                self.animate("DFS")

    def run_ucs(self):
        if not self.start or not self.target: return
        self.reset_search_data()
        pq = [(0, self.start)]
        costs = {self.start: 0}
        self.parent = {self.start: None}
        while pq:
            cost, curr = heapq.heappop(pq)
            if curr == self.target: return self.reconstruct()
            if curr not in self.explored:
                self.explored.add(curr)
                for n in self.get_neighbors(curr):
                    new_cost = costs[curr] + 1
                    if n not in costs or new_cost < costs[n]:
                        costs[n] = new_cost
                        self.parent[n] = curr
                        heapq.heappush(pq, (new_cost, n))
                self.frontier = [x[1] for x in pq]
                self.animate("UCS")

    def run_dls(self, limit, is_iddfs=False):
        if not is_iddfs: self.reset_search_data()
        found = self._dls_logic(self.start, limit, 0)
        if found and not is_iddfs: self.reconstruct()
        return found

    def _dls_logic(self, node, limit, depth):
        if node == self.target: return True
        if depth >= limit: return False
        self.explored.add(node)
        self.animate(f"DLS (Limit: {limit})")
        for n in self.get_neighbors(node):
            if n not in self.explored:
                self.parent[n] = node
                if self._dls_logic(n, limit, depth + 1): return True
        return False

    def run_iddfs(self):
        if not self.start or not self.target: return
        self.reset_search_data()
        for d in range(GRID_SIZE * GRID_SIZE):
            self.explored = set()
            self.parent = {self.start: None}
            if self.run_dls(d, is_iddfs=True): return self.reconstruct()

    def run_bidir(self):
        if not self.start or not self.target: return
        self.reset_search_data()
        f_q, b_q = deque([self.start]), deque([self.target])
        f_par, b_par = {self.start: None}, {self.target: None}
        f_exp, b_exp = {self.start}, {self.target}
        while f_q and b_q:
            # Forward
            cf = f_q.popleft()
            for n in self.get_neighbors(cf):
                if n in b_exp:
                    self.reconstruct(cf, f_par); self.reconstruct(n, b_par)
                    return self.draw("Bidirectional Connected")
                if n not in f_exp:
                    f_par[n] = cf; f_exp.add(n); f_q.append(n)
            # Backward
            cb = b_q.popleft()
            for n in self.get_neighbors(cb):
                if n in f_exp:
                    self.reconstruct(n, f_par); self.reconstruct(cb, b_par)
                    return self.draw("Bidirectional Connected")
                if n not in b_exp:
                    b_par[n] = cb; b_exp.add(n); b_q.append(n)
            self.frontier = list(f_q) + list(b_q)
            self.explored = f_exp.union(b_exp)
            self.animate("Bidirectional")

    def main_loop(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[1] > 50:
                        grid_pos = ((pos[1]-50)//CELL_SIZE, pos[0]//CELL_SIZE)
                        if not self.start: self.start = grid_pos
                        elif not self.target and grid_pos != self.start: self.target = grid_pos
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.run_bfs()
                    if event.key == pygame.K_2: self.run_dfs()
                    if event.key == pygame.K_3: self.run_ucs()
                    if event.key == pygame.K_4: self.run_dls(12)
                    if event.key == pygame.K_5: self.run_iddfs()
                    if event.key == pygame.K_6: self.run_bidir()
                    if event.key == pygame.K_r: self.reset_all()
        pygame.quit()

if __name__ == "__main__":
    AIPathfinder().main_loop()
