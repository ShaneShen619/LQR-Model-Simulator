import pygame
import numpy as np
import random
from scipy.linalg import solve_continuous_are

# --- LQR Math ---
def solve_lqr(A, B, Q, R):
    try:
        P = solve_continuous_are(A, B, Q, R)
        K = np.linalg.inv(R) @ B.T @ P
        return K
    except:
        return np.array([[0.0, 0.0]])

# --- Constants ---
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 40, 80
FPS = 60
ROAD_WIDTH = 400
ROAD_L = (WIDTH - ROAD_WIDTH) // 2
ROAD_R = ROAD_L + ROAD_WIDTH

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)

class LQRController:
    def __init__(self, v=15.0, L=2.5):
        self.v = v
        self.L = L
        # x = [e, theta]
        self.A = np.array([[0, v],
                           [0, 0]])
        self.B = np.array([[0],
                           [v/L]])
        self.q_val = 10.0
        self.r_val = 1.0
        self.K = self.update_k()

    def update_k(self):
        Q = np.diag([self.q_val, 1.0])
        R = np.array([[self.r_val]])
        self.K = solve_lqr(self.A, self.B, Q, R)
        return self.K

    def get_steering(self, e, theta):
        x = np.array([[e], [theta]])
        u = -self.K @ x
        return u[0, 0]

class Car:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.theta = 0.0  # Heading angle in radians (0 is up)
        self.v = 15.0     # Speed
        self.target_x = WIDTH // 2
        self.steering = 0.0

    def update(self, dt, controller):
        # Calculate errors
        e = self.x - self.target_x
        theta_err = self.theta # Assuming target heading is 0 (up)
        
        # Get LQR control
        self.steering = controller.get_steering(e, theta_err)
        
        # Limit steering angle
        self.steering = np.clip(self.steering, -np.radians(30), np.radians(30))
        
        # Simple Bicycle Model Kinematics
        # dx/dt = v * sin(theta)
        # dtheta/dt = v / L * tan(steering)
        L = controller.L
        self.x += self.v * np.sin(self.theta) * dt * 20 # Scale for pixels
        self.theta += (self.v / L) * np.tan(self.steering) * dt

    def draw(self, surface):
        # Rotate car image
        car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, BLUE, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=5)
        # Draw "headlights" to see direction
        pygame.draw.rect(car_surface, YELLOW, (5, 0, 10, 5))
        pygame.draw.rect(car_surface, YELLOW, (CAR_WIDTH-15, 0, 10, 5))
        
        rotated_car = pygame.transform.rotate(car_surface, -np.degrees(self.theta))
        rect = rotated_car.get_rect(center=(self.x, self.y))
        surface.blit(rotated_car, rect.topleft)

class Obstacle:
    def __init__(self):
        self.x = random.randint(ROAD_L + 50, ROAD_R - 50)
        self.y = -50
        self.speed = 5
        self.w, self.h = 30, 30

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x - self.w//2, self.y - self.h//2, self.w, self.h))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("LQR Racing - Q vs R")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    controller = LQRController()
    car = Car()
    obstacles = []
    spawn_timer = 0
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    controller.q_val *= 1.5
                    controller.update_k()
                if event.key == pygame.K_DOWN:
                    controller.q_val /= 1.5
                    controller.update_k()
                if event.key == pygame.K_RIGHT:
                    controller.r_val *= 1.5
                    controller.update_k()
                if event.key == pygame.K_LEFT:
                    controller.r_val /= 1.5
                    controller.update_k()
                
                # Snap to reasonable bounds
                controller.q_val = np.clip(controller.q_val, 0.1, 1000.0)
                controller.r_val = np.clip(controller.r_val, 0.01, 100.0)

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 90:
            obstacles.append(Obstacle())
            spawn_timer = 0

        # Update obstacles and target
        new_target_x = WIDTH // 2
        for obs in obstacles:
            obs.update()
            # Simple obstacle avoidance logic:
            # If obstacle is ahead, shift target x
            if obs.y < car.y and obs.y > car.y - 250:
                if abs(obs.x - car.x) < 80:
                    if obs.x < WIDTH // 2:
                        new_target_x = ROAD_R - 70
                    else:
                        new_target_x = ROAD_L + 70
        
        car.target_x = new_target_x
        car.update(dt, controller)

        # Remove old obstacles
        obstacles = [o for o in obstacles if o.y < HEIGHT + 50]

        # Draw
        screen.fill(GREEN) # Background
        # Road
        pygame.draw.rect(screen, GRAY, (ROAD_L, 0, ROAD_WIDTH, HEIGHT))
        pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
        
        # Target path visualization
        pygame.draw.circle(screen, YELLOW, (int(car.target_x), int(car.y)), 5)

        for obs in obstacles:
            obs.draw(screen)
        
        car.draw(screen)

        # UI
        ui_bg = pygame.Surface((220, 150))
        ui_bg.set_alpha(180)
        ui_bg.fill(BLACK)
        screen.blit(ui_bg, (10, 10))

        q_text = font.render(f"Q (Precision): {controller.q_val:.2f} [UP/DN]", True, WHITE)
        r_text = font.render(f"R (Comfort): {controller.r_val:.2f} [L/R]", True, WHITE)
        k_text = font.render(f"K: {controller.K.flatten()}", True, WHITE)
        steer_text = font.render(f"Steer: {np.degrees(car.steering):.2f} deg", True, WHITE)
        
        screen.blit(q_text, (20, 20))
        screen.blit(r_text, (20, 50))
        screen.blit(k_text, (20, 80))
        screen.blit(steer_text, (20, 110))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
