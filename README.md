# Two-Player Console Battleship

This is a two-player, console-based implementation of the classic board game **Battleship**. The game setup, including board size and ship definitions, is loaded from a **configuration file**, allowing for flexible gameplay.

---

## Getting Started

### Prerequisites

This program relies on custom local modules/classes. Ensure your project structure includes the necessary files for the following imports:
* `battleship.files.Files`
* `battleship.player.Player`
* `battleship.board.Board`

### 1. Prepare a Configuration File

A configuration text file is required to define the board dimensions and ship properties. Each required piece of data must be on its own line: the number of **rows**, the number of **columns**, a blank separator line, and subsequent lines defining ships with the format `[Ship_Letter] [Ship_Size]`.

### 2. Execute the Script

Run the main Python file from your terminal:

```bash
python your_main_file.py
```

---

## Gameplay

### Follow the Prompts

The program will guide you through the initial setup:
1. Enter the **path to the configuration file**.
2. Players will be asked to enter their **names**.
3. The game immediately enters the **Ship Placement Phase**.

### Ship Placement Phase

Each player places their ships based on the definitions in the configuration file. For each ship, the player must enter:
* The desired **orientation** (`vertical` or `horizontal`).
* The **starting location** in the format `row col`.

The program validates placement against board boundaries and existing ships. The board is displayed after each successful placement.

### Firing Phase

Players take alternating turns.
1. Before firing, the current player is shown their **Firing Board** (tracking opponent hits/misses) and their **Placement Board** (showing their own ships).
2. The player enters the firing location as `row col`.
3. The program announces a **Hit**, a **Miss**, or a **Sink** if a ship is entirely destroyed.

The first player to destroy **all** of the opponent's ships wins.
