# ✨ Spellbound Ramblers

A top-down survival shooter built with Python and the Pygame library. Navigate through the world, aim your weapon, and fight off endless waves of monsters to survive.

![Gameplay Gif](Assets/gifs/SpellboundRamblers_gameplay.gif)

---

### 🎮 Features

*   **Dynamic Camera System:** The camera smoothly follows the player, allowing exploration of a large map.
*   **360° Aiming & Combat:** Use the mouse to aim your gun and shoot in any direction.
*   **Tiled Map Integration:** Features a detailed world built with Tiled (`.tmx`), including obstacles and collision layers.
*   **Enemy AI:** Hordes of monsters spawn continuously and track the player's position.
*   **Health System:** You have limited lives. Taking damage triggers temporary invulnerability frames with visual blinking effects.
*   **Animated Sprites:** Includes character movement animations and visual feedback for hitting enemies.
*   **Audio Atmosphere:** Complete with shooting sounds, impact effects, and background music.

---

### 🕹️ Controls

| Key / Input | Action       |
| :---------- | :----------- |
| **W A S D** or **↑ ↓ ← →** | Move Character |
| **Mouse Cursor** | Aim Weapon   |
| **Left Mouse Button** | Fire |

---

### ⚙️ Setup and Installation

To run this game, you'll need Python, **Pygame**, and the **PyTMX** library (used for loading the map).

1.  **Install Dependencies:**
    Open your terminal or command prompt and run:
    ```bash
    pip install pygame pytmx
    ```

2.  **Run the Game:**
    Navigate to this directory from the root of the repository and run the main script.
    ```bash
    python main.py
    ```
