# LQR Racing Simulator

A Python and Pygame-based racing game prototype designed to intuitively demonstrate the application of the **LQR (Linear Quadratic Regulator)** control algorithm in vehicle steering actuation systems. By adjusting control parameters in real-time, you can experience how different driving styles—from aggressive sport to ultra-smooth comfort—affect obstacle avoidance performance.

## 🚀 Key Features

*   **Real-time LQR Tuning**: Freely adjust $Q$ (Precision) and $R$ (Comfort) parameters before starting the game.
*   **Manual Driving Mode**: You control the target steering input via keyboard, while the LQR algorithm acts as the execution layer to drive the wheels precisely or smoothly.
*   **Dynamic Difficulty System**:
    *   **Continuous Acceleration**: Vehicle speed increases over time, testing the stability of your control tuning at high speeds.
    *   **Diverse Obstacles**: Includes standard obstacles, wide barriers, and horizontally moving challenges.
*   **Stats & Persistence**:
    *   Real-time mileage tracking (KM).
    *   Persistent High Score saved automatically to `highscore.txt`.

## 🛠️ Requirements

Ensure you have Python 3.x installed, then install the dependencies:

```bash
pip install pygame numpy scipy
```

## 🎮 How to Run

Execute the following command in your terminal:

```bash
python3 lqr_racing.py
```

## ⌨️ Controls

### Menu Screen (Configuration)
*   **UP / DOWN Arrows**: Adjust **Q** (State Cost). Higher values make steering more precise and aggressive.
*   **LEFT / RIGHT Arrows**: Adjust **R** (Control Cost). Higher values make steering smoother and more filtered.
*   **SPACE**: Confirm parameters and start the engine.

### Game Screen (Driving)
*   **LEFT / RIGHT Arrows**: Control the vehicle's steering.
*   **Yellow Indicator Line**: Represents the actual wheel steering angle.
*   **Goal**: Avoid Red, Orange, and Purple obstacles and travel as far as possible.

## 🧠 Intuitive LQR Explanation

This project applies LQR to the steering actuator. The state vector is the angular error, and the control input is the steering velocity.

| Parameter | Physical Meaning | Driving Feel (High Value) |
| :--- | :--- | :--- |
| **Q (Precision)** | Penalty on angular error | **Sport Mode**: Extremely fast steering response with zero perceived lag, but can feel "twitchy" at high speeds. |
| **R (Comfort)** | Penalty on control effort | **Comfort Mode**: Silky smooth steering transitions that filter out jerky movements. However, may lead to "understeer" feel during rapid obstacle avoidance. |

## 📁 File Structure

*   `lqr_racing.py`: The main game application.
*   `highscore.txt`: Automatically generated file for high score persistence.
*   `lqr_lateral_control.py`: (Legacy) Original script for generating Matlab-style comparison plots.

## 📝 License

This project is for educational and algorithmic demonstration purposes only.