# CS50AI | Lecture 1 - Knowledge | Project 2 - [`Minesweeper`](https://cs50.harvard.edu/ai/2024/projects/1/minesweeper/)

This project is a mandatory assignment from **CS50AI – Lecture 1: "Knowledge"**.

### 📌 Usage

To run the project locally, follow these steps:

1. **Clone the repository** to your local machine.

2. **Navigate to the project directory**:

   ```sh
   cd path/to/minesweeper
   ```

3. Install `requirements.txt`
 
4. Run `python runner.py` to play the game

<br>

### Project Overview

The project's task is to implement propositional logic for the AI agent to be able to solve [minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game)), a classic puzzle game.

There are two main files in this project: `runner.py` and `minesweeper.py`. `minesweeper.py` contains all of the logic the game itself and for the AI to play the game. `runner.py` was already implemented, and contains all of the code to run the graphical interface for the game. 

In `minesweeper.py`, there are three classes defined, `Minesweeper`, which handles the gameplay (already implemented); `Sentence`, which represents a logical sentence that contains both a set of cells and a count; and `MinesweeperAI`, which handles inferring which moves to make based on knowledge. 

My task was to implement the following functions:

For the `Sentence` class:
- `known_mines()`
- `known_safes()`
- `mark_mine(cell)`
- `mark_safe(cell)`

For the `MinesweeperAI` class:
- `add_knowledge()`
- `make_safe_move()`
- `make_random_move()`


### Implementation of `Sentence` class

The sentence must only be holding information for cells that we don't know if they are mines or safes. This means that whenever we mark a cell as a safe or mine, we need to update our knowledge base so that this cell is removed (since we now know about it).

The Sentence representation is as follows:
`{A, B, C, D, E} = COUNT`, where letters are cells, and COUNT is an int representing how many of these cells are mines. So, if count was "2", it would mean that two of A, B, C, D, or E are mines, and the rest are safe cells.

**`known_mines()`**:
In this function, I am checking if the number of cells is same as the count. If count equals length, it means that all of these cells are munes.

**`known_safes()`**:
In this function, I am checking if count is zero, cause if it is, I know for sure that all cells are safes.

**`mark_mine(cell)`**:
I am checking if cell is part of my Sentence's cells. If yes, I am removing it since the sentence should not hold information about known cells. I am also decreasing the count by 1, since the knowledge should be about cells we are not sure about.

**`mark_safe(cell)`**:
Similarly to `known_mine(cell)`, I am checking if cell is part of my Sentence's cells. If yes, I am removing it from the sentence. There is no need to update count in this case since we did not remove a mine.