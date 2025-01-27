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

## Project Overview

This project implements propositional logic to enable an AI agent to solve [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game)), a classic puzzle game.

There are two main files in this project:

- **`runner.py`**: Already implemented, this file contains the code for the graphical interface.
- **`minesweeper.py`**: This file contains the core game logic and the AI that plays the game.

### Classes in `minesweeper.py`

1. **`Minesweeper`**: Handles the gameplay (already implemented).
2. **`Sentence`**: Represents a logical sentence that contains a set of cells and a count, used to infer knowledge about the game.
3. **`MinesweeperAI`**: Manages the AI's reasoning and decision-making, making use of the knowledge base built from logical inference.

### My Task

I was responsible for implementing the following functions:

#### In the `Sentence` class:
- `known_mines()`
- `known_safes()`
- `mark_mine(cell)`
- `mark_safe(cell)`

#### In the `MinesweeperAI` class:
- `add_knowledge(cell, count)`
- `make_safe_move()`
- `make_random_move()`

## Implementation of `Sentence` Class

The `Sentence` class stores information about cells that are not yet known to be mines or safes. When a cell is marked as a mine or safe, it is removed from the sentence, and the knowledge base is updated accordingly.

### Sentence Representation

A `Sentence` is represented as follows: `{A, B, C, D, E} = COUNT`


Where:
- `{A, B, C, D, E}` are the cells in the sentence.
- `COUNT` is the number of mines among these cells.

For example, if `COUNT = 2`, it means that two of the cells `{A, B, C, D, E}` are mines, and the rest are safe.

### Functions in `Sentence`

- **`known_mines()`**:
  - Checks if the number of cells equals the count. If true, all cells in the sentence are mines.
  
- **`known_safes()`**:
  - Checks if the count is zero. If true, all cells in the sentence are safe.
  
- **`mark_mine(cell)`**:
  - If the cell is part of the sentence, it is removed from the sentence, and the count is decreased by 1 since the mine is no longer part of the uncertain set.
  
- **`mark_safe(cell)`**:
  - Similar to `mark_mine`, but no change is made to the count since a safe cell is removed without affecting the number of mines.

## Function: `add_knowledge(cell, count)`

The `add_knowledge()` function is crucial for updating the AI’s knowledge base when a safe cell is revealed. The AI uses this information to infer the status of neighboring cells.

### Parameters

- **`cell`** (tuple): The coordinates of a safe cell, e.g., `(x, y)`.
- **`count`** (int): The number of mines in the neighboring cells around the given `cell`.

### Steps of Execution

1. **Mark the Cell as a Move**:  
   The function starts by adding the cell to the `moves_made` set, indicating that the move has been made.

2. **Mark the Cell as Safe**:  
   The `mark_safe(cell)` method is called to register the cell as safe and remove it from further consideration.

3. **Create a New Sentence**:  
   A new logical `Sentence` is created based on the `cell` and `count`. This sentence represents neighboring cells that might contain mines, with the given `count` indicating how many of them are mines.
   - The function identifies adjacent cells and filters out those already marked as mines or safes.
   - The remaining cells are part of the new sentence, and the count is adjusted based on how many of the neighboring cells are known to be mines.

4. **Mark Known Safe and Mine Cells**:  
   The function updates the `MinesweeperAI`'s `safes` and `mines` sets by marking cells as safe or mines based on the knowledge base.

5. **Sentence Inference**:  
   The function iterates through all pairs of sentences and looks for subsets. If one sentence’s set of cells is a subset of another’s, a new `Sentence` is inferred and added to the knowledge base.

6. **Repeat Inference Until Completion**:  
   The process continues until no new inferences can be made, ensuring that the AI refines its knowledge base as much as possible.

### Key Points

- **Marking Cells**: Cells identified as safe or containing mines are removed from sentences, improving the accuracy of the knowledge base.
- **Logical Reasoning**: The AI uses propositional logic to infer new facts based on relationships between sentences.
- **Efficient Inference**: The AI continuously updates its knowledge base and infers new information until no further inferences can be made.

### Example

Let’s walk through an example:

1. The AI clicks on cell `(2, 2)` and reveals that there is 1 mine in the neighboring cells.
2. The function will:
   - Mark cell `(2, 2)` as safe.
   - Add a sentence for the neighboring cells (e.g., `(1, 1)`, `(1, 2)`, `(1, 3)`, etc.) with a count of 1.
3. The AI will infer new safe and mine cells based on its knowledge base, progressively refining its understanding.

The AI will use this knowledge to make informed decisions in the `make_safe_move()` function.


The `add_knowledge()` function is the backbone of the Minesweeper AI's decision-making process. It allows the AI to gather, process, and apply knowledge about the game board, using propositional logic to systematically infer which cells are safe and which may contain mines.

<br>

## Conclusion

This project has been an insightful journey into the implementation of propositional logic through the creation of an AI for the Minesweeper game. By designing the `Sentence` and `MinesweeperAI` classes and utilizing logical inference, I was able to build a system where the AI can systematically deduce safe moves and identify mines based on the knowledge it accumulates.

Through the process of implementing the various functions—such as `add_knowledge()`, `known_mines()`, and `mark_safe()`—I gained hands-on experience with propositional logic. This project reinforced my understanding of logic-based AI systems and how they can be applied to solve complex problems in games and beyond.