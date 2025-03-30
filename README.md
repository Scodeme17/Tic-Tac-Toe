# Tic-Tac-Toe Game 🎮

Welcome to the **Tic-Tac-Toe** game! This is a simple Python-based command-line game where two players take turns to mark `X` and `O` on a 3x3 grid. The first player to align three of their marks in a row, column, or diagonal wins! 🎉

---

## Features ✨
- Two-player mode 👥
- User-friendly command-line interface 🖥️
- Automatic win detection ✅
- Handles invalid inputs and prevents overwriting existing moves ❌
- Simple yet efficient algorithm for game logic 🏆

---

## How to Play 🕹️
1. Run the script using Python:
   ```bash
   python Tic_Tac_toe.py
   ```
2. The game will display the board and prompt players to enter their moves.
3. Players take turns to place their marks (`X` or `O`) by entering a number corresponding to a board position.
4. The game ends when a player wins or if the board is full (resulting in a draw).

---

## Algorithm Used 🧠
This game uses a **sequential checking algorithm** to determine the winner. The algorithm follows these steps:
- Check each row for three identical marks.
- Check each column for three identical marks.
- Check both diagonals for three identical marks.
- If none of the above conditions are met and the board is full, declare a draw.

---

## Example Gameplay 🎲
```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

**Player 1 (X) moves:** 5
```
 1 | 2 | 3
---+---+---
 4 | X | 6
---+---+---
 7 | 8 | 9
```
**Player 2 (O) moves:** 1
```
 O | 2 | 3
---+---+---
 4 | X | 6
---+---+---
 7 | 8 | 9
```
... and so on until a player wins or it's a draw!

---
