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


### Function: `add_knowledge(cell, count)`

The `add_knowledge()` function is a core method in the `MinesweeperAI` class, responsible for updating the AI’s knowledge base when a safe cell is revealed. This method allows the AI to infer the status of neighboring cells, whether they are safe or contain mines, by utilizing logical reasoning.

#### Parameters:
- `cell` (tuple): A tuple representing the coordinates of a safe cell, e.g., `(x, y)`, which the Minesweeper board reveals.
- `count` (int): The number of mines in the neighboring cells around the given `cell`. This information is provided by the game when a safe cell is clicked.

#### Steps of Execution:
1. **Mark the Cell as a Move**:  
   The function first marks the given cell as a move that has been made by adding it to the `moves_made` set.

2. **Mark the Cell as Safe**:  
   The `mark_safe(cell)` method is called to record that the current cell is safe. This removes the cell from any future consideration regarding mines.

3. **Create a New Sentence**:  
   Based on the given `cell` and `count`, the function generates a new logical `Sentence`. A `Sentence` represents a group of cells that *may* contain mines, and `count` tells how many mines are present within that group.

   - It identifies all adjacent cells to the given `cell` by creating a set of potential neighboring coordinates using `itertools.product`.
   - It then filters out any adjacent cells that are either already marked as mines or already marked as safe.
   - The remaining cells are part of the `Sentence`, and their mine count is adjusted by subtracting the number of neighboring cells already known to be mines.

4. **Mark Known Safe and Mine Cells**:  
   After adding the new `Sentence` to the knowledge base, the function tries to infer new information. It looks for cells that are known to be safe or mines across all sentences in the knowledge base and updates the `MinesweeperAI`'s `safes` and `mines` sets accordingly.

   - If new safe cells are identified, they are marked as safe.
   - Similarly, if new mine cells are identified, they are marked as mines.

5. **Sentence Inference**:  
   The function then iterates over all pairs of sentences in the knowledge base to see if new inferences can be drawn:
   - It checks if one sentence’s set of cells is a subset of another’s. If so, it infers a new `Sentence` that represents the remaining cells from the larger sentence, which could potentially be safe or contain mines.
   - This inferred sentence is then added to the knowledge base.

6. **Repeat Inference until Completion**:  
   The function continues this process of marking safe and mine cells and inferring new sentences until no more new information can be deduced. This loop ensures that the AI can make as many logical inferences as possible.

#### Key Points:
- **Marking Cells**: As cells are identified as safe or containing mines, they are removed from sentences, allowing the knowledge base to become progressively more accurate.
- **Logical Reasoning**: The AI uses propositional logic to infer new facts, such as identifying safe cells or mines based on the relationships between sentences.
- **Efficient Inference**: The function continuously refines its knowledge base, adding new inferred sentences, until no further inferences can be made.

#### Example:
Let’s consider an example to illustrate how `add_knowledge()` works:

1. Suppose the AI clicks on cell `(2, 2)` and the game reveals that there are 1 mine in the neighboring cells.
2. The function will:
   - Mark cell `(2, 2)` as safe.
   - Add a sentence representing the neighboring cells (e.g., `(1, 1)`, `(1, 2)`, `(1, 3)`, `(2, 1)`, `(2, 3)`, `(3, 1)`, `(3, 2)`, `(3, 3)`) with a count of 1, indicating that one of these cells is a mine.
3. The AI will continue to infer from its knowledge base. If other cells are marked as safe or mined, those will be removed from the sentence, and new inferences will be made.

The AI continues to expand its knowledge base, allowing it to make more informed decisions on the next safe moves to make, which are covered by the `make_safe_move()` function.

#### Conclusion:
The `add_knowledge()` function is central to how the MinesweeperAI gathers, processes, and applies knowledge about the game’s board. It uses propositional logic to systematically update the AI’s understanding of which cells are safe and which may contain mines.
