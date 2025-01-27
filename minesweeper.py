import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """ 
        # if number of cells and number of counts is the same, then these cells are mines
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If count = 0, then all are safes
        if self.count == 0:
            return self.cells 
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """

        # 1. Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2. Mark the cell as safe
        self.mark_safe(cell)

        # 3. Add a new sentence to the AI's knowledge base, based on the value of `cell` and `count`
        x, y = cell
        adjacent_cells = {
            (x-1, y-1), 
            (x-1, y), 
            (x-1, y+1), 
            (x, y-1), 
            (x, y+1), 
            (x+1, y-1), 
            (x+1, y), 
            (x+1, y+1)
        }

        # Filter out cells outside the valid range
        filtered_cells = {
            (cx, cy) for cx, cy in adjacent_cells
            if 0 <= cx <= self.height-1 and 0 <= cy <= self.width-1
        }

        cells_to_add = set()
        mines_count = 0
        for cell in filtered_cells:
            if cell in self.mines:
                mines_count += 1
            elif cell not in self.safes:
                cells_to_add.add(cell)

        # Remove known mines. We don't want to count mines that are already known to us (similar to Sentence's mark_mine() function)
        adjusted_count = count - mines_count

        if cells_to_add:
            new_sentence = Sentence(cells_to_add, adjusted_count)
            self.knowledge.append(new_sentence)

        # 4. Mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base  
        while True:
            safe_cells = set()
            mine_cells = set()
            for sentence in self.knowledge:
                known_mines = sentence.known_mines()
                known_safes = sentence.known_safes()
                safe_cells.update(known_safes)
                mine_cells.update(known_mines) 
            
            # Breaks loop when no more inferences can be made (a.k.a if no new cells were found) 
            if not safe_cells and not mine_cells:
                break

            for cell in safe_cells:
                if cell not in self.safes:
                    self.mark_safe(cell)
            for cell in mine_cells:
                if cell not in self.mines:
                    self.mark_mine(cell)

            # Clear empties
            self.knowledge = [s for s in self.knowledge if s.cells]

        # 5. Add any new sentences to the AI's knowledge base
        #   if they can be inferred from existing knowledge
        
        # While no more knowledge can be inferred
        while True:
            knowledge_copy = self.knowledge[:]
            found_inferred_sentence = False

            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    # Ensure s1 != s2
                    if s1 != s2 and s1.cells.issubset(s2.cells):
                        inferred_cells = s2.cells - s1.cells
                        inferred_count = s2.count - s1.count

                        # Create inferred sentence
                        inferred_sentence = Sentence(inferred_cells, inferred_count)

                        # Avoid duplicates
                        if inferred_sentence not in knowledge_copy:
                            found_inferred_sentence = True
                            knowledge_copy.append(inferred_sentence)

            # Update knowledge
            self.knowledge = knowledge_copy

            # Exit if no new sentences were inferred
            if not found_inferred_sentence:
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        """
        safes_not_played = self.safes - self.moves_made

        if safes_not_played:
            return next(iter(safes_not_played))
        else: 
            return None
            
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        """
        mines = self.mines 
        moves_made = self.moves_made
        board_cells = {(r, c) for r in range(self.width + 1) for c in range(self.height + 1)}
        board_cells = board_cells - moves_made - mines
     
        random_num = random.randint(0, len(board_cells) - 1)
        
        sorted_cells = sorted(board_cells)
        x, y = sorted_cells[random_num]

        new_set = set((x, y))
        return new_set


# if __name__ == "__main__": 
    # # DEBUG
