# LQR Racing Simulator | LQR 赛车控制与手感模拟器

A Python and Web-based racing game prototype designed to intuitively demonstrate the application of the **LQR (Linear Quadratic Regulator)** control algorithm in vehicle steering actuation systems.

这是一个基于 Python 和 Web 的赛车游戏原型，旨在直观展示 **LQR (线性二次型调节器)** 控制算法在车辆转向执行系统中的应用。

---

## 🇺🇸 English Version

### 🚀 Key Features
*   **Dual Mode Support**: Run locally via Pygame or deploy globally on Vercel as a Web App.
*   **Real-time LQR Tuning**: Adjust $Q$ (Precision) and $R$ (Comfort) parameters to change the "feel" of the steering.
*   **Dynamic Difficulty**: Vehicle speed increases over time, with diverse obstacles (Wide, Moving).
*   **High Score Persistence**: Locally saved to `highscore.txt` and displayed in real-time.

### 🛠️ Requirements
*   Python 3.x
*   Libraries: `pygame`, `numpy`, `scipy`

### 🎮 How to Run
#### 1. Local Version (Pygame)
```bash
pip install pygame numpy scipy
python3 lqr_racing.py
```
#### 2. Web Version (Vercel)
The project is ready for Vercel deployment. It uses a Python Serverless function (`api/solve_lqr.py`) for math and HTML5 Canvas for rendering.

### ⌨️ Controls
*   **Menu**: Use Arrow Keys to adjust Q/R, Space to Start.
*   **Driving**: Left/Right Arrow Keys to steer.
*   **Indicator**: The yellow line on the car shows the actual wheel angle calculated by LQR.

### 🧠 LQR Theory
| Parameter | Driving Feel (High Value) |
| :--- | :--- |
| **Q (Precision)** | **Sport Mode**: Extremely fast steering response, but can be twitchy. |
| **R (Comfort)** | **Comfort Mode**: Silky smooth filtering of inputs, but may feel laggy at high speeds. |

---

## 🇨🇳 中文版

### 🚀 核心特性
*   **双模式支持**：既可以作为本地 Pygame 程序运行，也可以通过 Vercel 部署为网页版。
*   **LQR 实时调参**：通过调整 $Q$ (精度) 和 $R$ (舒适度) 参数，改变转向手感。
*   **动态难度系统**：车速随时间提升，拥有多种障碍物（宽幅障碍、移动障碍）。
*   **最高纪录持久化**：本地保存至 `highscore.txt`，并在界面实时显示。

### 🛠️ 环境要求
*   Python 3.x
*   依赖库：`pygame`, `numpy`, `scipy`

### 🎮 如何运行
#### 1. 本地版 (Pygame)
```bash
pip install pygame numpy scipy
python3 lqr_racing.py
```
#### 2. 网页版 (Vercel)
项目已适配 Vercel 部署。使用 Python 云函数 (`api/solve_lqr.py`) 进行数学计算，使用 HTML5 Canvas 进行画面渲染。

### ⌨️ 操作指南
*   **菜单界面**：使用方向键调整 Q/R，空格键开始游戏。
*   **驾驶界面**：使用左/右方向键控制赛车。
*   **指示线**：赛车上的黄色线条代表 LQR 计算出的实际车轮转角。

### 🧠 LQR 参数直观解释
| 参数 | 驾驶感受 (高数值) |
| :--- | :--- |
| **Q (精度)** | **运动模式**：转向响应极快，指哪打哪，但在高速下可能过于灵敏。 |
| **R (舒适)** | **舒适模式**：转向动作极其平滑丝滑，但在高速避障时会有延迟感（“推头”）。 |

---

## 📁 File Structure | 文件结构
*   `lqr_racing.py`: Main Pygame application | 本地 Pygame 主程序。
*   `public/index.html`: Web frontend | 网页版前端。
*   `api/solve_lqr.py`: LQR calculation API | LQR 计算后端接口。
*   `vercel.json`: Vercel config | Vercel 部署配置。
*   `highscore.txt`: High score data | 最高纪录存储。
