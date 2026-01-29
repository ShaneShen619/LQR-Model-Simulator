import pygame
import numpy as np
import random
import os
from scipy.linalg import solve_continuous_are

# --- LQR 核心计算 ---
def solve_lqr(A, B, Q, R):
    try:
        P = solve_continuous_are(A, B, Q, R)
        K = np.linalg.inv(R) @ B.T @ P
        return K
    except:
        return np.array([[0.0, 0.0]])

# --- 常量与颜色 ---
WIDTH, HEIGHT = 800, 600
FPS = 60
BLUE = (50, 120, 200)
RED = (200, 50, 50)
ORANGE = (255, 140, 0)
PURPLE = (138, 43, 226)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 215, 0)
GREEN = (50, 200, 50)
HI_SCORE_FILE = "highscore.txt"

class Obstacle:
    def __init__(self, speed_factor):
        types = ["NORMAL"] * 6 + ["WIDE"] * 2 + ["MOVING"] * 2
        self.type = random.choice(types)
        self.y = -50
        self.vx = 0
        
        if self.type == "NORMAL":
            self.w, self.h = 40, 40
            self.color = RED
        elif self.type == "WIDE":
            self.w, self.h = 100, 40
            self.color = ORANGE
        elif self.type == "MOVING":
            self.w, self.h = 40, 40
            self.color = PURPLE
            self.vx = random.choice([-2, 2]) * (1 + speed_factor * 0.5)

        self.x = random.randint(150 + self.w//2, 650 - self.w//2)

    def update(self, speed):
        self.y += speed
        self.x += self.vx
        if self.x < 150 + self.w//2 or self.x > 650 - self.w//2:
            self.vx *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.w//2, self.y - self.h//2, self.w, self.h), border_radius=5)

class RacingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("LQR Racing - Pro Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.bold_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.state = 0 # 0: MENU, 1: DRIVING
        self.q_val = 10.0
        self.r_val = 1.0
        self.high_score = self.load_high_score()
        self.reset_game()

    def load_high_score(self):
        if os.path.exists(HI_SCORE_FILE):
            try:
                with open(HI_SCORE_FILE, "r") as f:
                    return float(f.read())
            except:
                return 0.0
        return 0.0

    def save_high_score(self):
        with open(HI_SCORE_FILE, "w") as f:
            f.write(f"{self.high_score:.2f}")

    def reset_game(self):
        self.car_x = WIDTH // 2
        self.car_y = HEIGHT - 100
        self.car_theta = 0.0
        self.current_steer = 0.0
        self.target_steer = 0.0
        self.v = 6.0          
        self.max_v = 30.0     
        self.score = 0
        self.distance = 0.0   # 公里数
        self.obstacles = []
        self.spawn_timer = 0

    def get_lqr_gain(self):
        A = np.array([[0, 1], [0, 0]])
        B = np.array([[0], [1]])
        Q = np.diag([self.q_val, 0.1])
        R = np.array([[self.r_val]])
        return solve_lqr(A, B, Q, R)

    def draw_text(self, text, pos, color=WHITE, center=False, bold=False):
        f = self.bold_font if bold else self.font
        surf = f.render(text, True, color)
        if center:
            rect = surf.get_rect(center=pos)
        else:
            rect = surf.get_rect(topleft=pos)
        self.screen.blit(surf, rect)

    def handle_menu(self):
        self.screen.fill(GRAY)
        self.draw_text("LQR Racing: Pro Edition", (WIDTH//2, 100), YELLOW, center=True, bold=True)
        self.draw_text(f"BEST RECORD: {self.high_score:.2f} KM", (WIDTH//2, 150), GREEN, center=True)
        
        self.draw_text(f"Q (Sportiness): {self.q_val:.1f}  [UP/DOWN]", (WIDTH//2, 240), center=True)
        self.draw_text(f"R (Comfort): {self.r_val:.1f}  [LEFT/RIGHT]", (WIDTH//2, 280), center=True)
        self.draw_text("Press SPACE to Start", (WIDTH//2, 450), WHITE, center=True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: self.q_val *= 1.5
                if event.key == pygame.K_DOWN: self.q_val /= 1.5
                if event.key == pygame.K_RIGHT: self.r_val *= 1.5
                if event.key == pygame.K_LEFT: self.r_val /= 1.5
                if event.key == pygame.K_SPACE:
                    self.K = self.get_lqr_gain()
                    self.reset_game()
                    self.state = 1
                self.q_val = np.clip(self.q_val, 0.1, 5000)
                self.r_val = np.clip(self.r_val, 0.01, 1000)
        return True

    def handle_driving(self):
        self.screen.fill((20, 20, 20)) 
        
        # --- 赛道绘制 ---
        pygame.draw.rect(self.screen, (40, 40, 40), (150, 0, 500, HEIGHT))
        pygame.draw.line(self.screen, WHITE, (150, 0), (150, HEIGHT), 3)
        pygame.draw.line(self.screen, WHITE, (650, 0), (650, HEIGHT), 3)
        
        dt = 1.0 / FPS
        
        # 速度与公里数计算
        if self.v < self.max_v:
            self.v += 0.004
        
        # 假设 1 pixel/frame 在这个缩放比例下对应的公里数
        # 我们用一个比例系数让它看起来像真实里程
        self.distance += (self.v * 0.001) 
        
        if self.distance > self.high_score:
            self.high_score = self.distance
            self.save_high_score()

        # 障碍物逻辑
        self.spawn_timer += 1
        spawn_interval = max(12, 60 - int(self.v * 2))
        if self.spawn_timer > spawn_interval:
            self.obstacles.append(Obstacle(self.v / 10.0))
            self.spawn_timer = 0

        # 控制逻辑
        keys = pygame.key.get_pressed()
        max_steer = np.radians(35)
        if keys[pygame.K_LEFT]: self.target_steer = -max_steer
        elif keys[pygame.K_RIGHT]: self.target_steer = max_steer
        else: self.target_steer = 0

        error = self.current_steer - self.target_steer
        x = np.array([[error], [0]])
        u = -self.K @ x
        self.current_steer += u[0, 0] * dt
        self.current_steer = np.clip(self.current_steer, -max_steer, max_steer)

        # 物理模拟
        self.car_theta += (self.v / 3.0) * np.tan(self.current_steer) * dt
        self.car_x += self.v * np.sin(self.car_theta) * 1.5
        
        # 障碍物渲染
        for obs in self.obstacles[:]:
            obs.update(self.v * 0.8)
            obs.draw(self.screen)
            if abs(obs.x - self.car_x) < (obs.w/2 + 15) and abs(obs.y - self.car_y) < (obs.h/2 + 25):
                self.state = 0
            if obs.y > HEIGHT + 50:
                self.obstacles.remove(obs)
                self.score += 1

        if self.car_x < 150 or self.car_x > 650:
            self.state = 0

        # 赛车绘制
        car_surf = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.rect(car_surf, BLUE, (0, 0, 40, 70), border_radius=8)
        pygame.draw.line(car_surf, YELLOW, (20, 20), (20 + 30*np.sin(self.current_steer*2), 20 - 30*np.cos(self.current_steer*2)), 4)
        rotated_car = pygame.transform.rotate(car_surf, -np.degrees(self.car_theta))
        self.screen.blit(rotated_car, rotated_car.get_rect(center=(int(self.car_x), int(self.car_y))))

        # --- UI 显示 ---
        # 顶端历史最高纪录
        pygame.draw.rect(self.screen, (0, 0, 0, 150), (WIDTH//2 - 150, 5, 300, 30), border_radius=5)
        self.draw_text(f"BEST RECORD: {self.high_score:.2f} KM", (WIDTH//2, 20), GREEN, center=True, bold=True)
        
        # 实时公里数与速度
        self.draw_text(f"DISTANCE: {self.distance:.2f} KM", (20, 20), WHITE, bold=True)
        self.draw_text(f"SPEED: {self.v*5:.1f} KM/H", (20, 50), WHITE)
        self.draw_text(f"Q: {self.q_val:.1f} R: {self.r_val:.1f}", (20, 80), YELLOW)
        self.draw_text(f"SCORE: {self.score}", (20, 110), ORANGE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
        return True

    def run(self):
        running = True
        while running:
            if self.state == 0:
                running = self.handle_menu()
            else:
                running = self.handle_driving()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    game = RacingGame()
    game.run()
