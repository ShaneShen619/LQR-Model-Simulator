import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_continuous_are

def solve_lqr(A, B, Q, R):
    """
    求解连续时间代数黎卡提方程 (CARE) 并计算反馈增益矩阵 K。
    系统方程: dx/dt = Ax + Bu
    代价函数: J = Integral(x^T Q x + u^T R u) dt
    控制律: u = -Kx
    
    K = R^-1 * B^T * P
    其中 P 是 CARE 的解: A^T P + P A - P B R^-1 B^T P + Q = 0
    """
    P = solve_continuous_are(A, B, Q, R)
    K = np.linalg.inv(R) @ B.T @ P
    return K

def simulate(A, B, K, x0, t_span, dt):
    """
    进行系统仿真。
    """
    steps = int(t_span / dt)
    x = np.array(x0, dtype=float)
    x_history = [x.copy()]
    u_history = []
    
    for _ in range(steps):
        # 计算控制输入 u = -Kx
        u = -K @ x
        u_history.append(u[0])
        
        # 简单的欧拉积分更新状态: x_dot = Ax + Bu
        x_dot = A @ x + B @ u
        x = x + x_dot * dt
        x_history.append(x.copy())
        
    return np.array(x_history), np.array(u_history)

# --- 系统参数 ---
v = 10.0  # 车速 (m/s)
L = 2.5   # 轴距 (m)

# 状态向量 x = [e, theta]^T (偏离距离, 偏离角度)
# 系统矩阵 A = [[0, v], [0, 0]]
# 输入矩阵 B = [[0], [v/L]]
A = np.array([[0, v],
              [0, 0]])
B = np.array([[0],
              [v/L]])

# 仿真参数
x0 = [2.0, 0.0]  # 初始状态: 偏离 2 米，偏离角为 0
t_span = 10.0    # 仿真时长 10s
dt = 0.01        # 步长 10ms
time = np.arange(0, t_span + dt, dt)

# --- 配置 A: 激进型 (Aggressive) ---
# 更加关注减小状态误差，Q 权重较大
Q_a = np.diag([10.0, 1.0])  # 惩罚距离误差权重 10.0, 角度误差 1.0
R_a = np.array([[0.1]])      # 较小的控制惩罚
K_a = solve_lqr(A, B, Q_a, R_a)

# --- 配置 B: 舒适型 (Comfort) ---
# 更加关注驾驶平滑性，R 权重较大
Q_b = np.diag([1.0, 1.0])   # 较小的状态误差惩罚
R_b = np.array([[10.0]])    # 较大的控制惩罚，限制转向角度变化
K_b = solve_lqr(A, B, Q_b, R_b)

# --- 运行仿真 ---
hist_a, u_a = simulate(A, B, K_a, x0, t_span, dt)
hist_b, u_b = simulate(A, B, K_b, x0, t_span, dt)

# --- 可视化 ---
plt.figure(figsize=(12, 8))

# 子图 1: 偏离距离对比
plt.subplot(2, 1, 1)
plt.plot(time, hist_a[:, 0], label='Config A (Aggressive - High Q)', linewidth=2)
plt.plot(time, hist_b[:, 0], label='Config B (Comfort - High R)', linewidth=2)
plt.title('Vehicle Lateral Error (e) over Time')
plt.ylabel('Distance (m)')
plt.grid(True)
plt.legend()

# 子图 2: 控制输入 (转向角) 对比
plt.subplot(2, 1, 2)
plt.plot(time[:-1], np.degrees(u_a), label='Config A (Aggressive)', linewidth=2)
plt.plot(time[:-1], np.degrees(u_b), label='Config B (Comfort)', linewidth=2)
plt.title('Control Input (Steering Angle $\delta$) over Time')
plt.ylabel('Steering Angle (deg)')
plt.xlabel('Time (s)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('lqr_comparison.png')  # 保存结果为图片
plt.show()

print("\n--- LQR 增益矩阵 K 计算结果 ---")
print(f"激进型 (Config A) K: {K_a.flatten()}")
print(f"舒适型 (Config B) K: {K_b.flatten()}")
print("\n仿真完成，结果已保存至 'lqr_comparison.png'。")
