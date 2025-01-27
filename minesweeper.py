import itertools
import random
from collections import Counter

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

        # # Add mines randomly
        # while len(self.mines) != mines:
        #     i = random.randrange(height)
        #     j = random.randrange(width)
        #     if not self.board[i][j]:
        #         self.mines.add((i, j))
        #         self.board[i][j] = True

        # # FOR DEBUG # Add mines NOT Randomly
        self.mines.add((0, 3))
        self.board[0][3] = True


 

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

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1. mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2. mark the cell as safe
        self.mark_safe(cell)

        # 3. add a new sentence to the AI's knowledge base, based on the value of `cell` and `count`
        x, y = cell
        adjacent_cells = {
                (x-1,y-1), 
                (x-1,y), 
                (x-1,y+1), 
                (x,y-1), 
                (x,y+1), 
                (x+1,y-1), 
                (x+1,y), 
                (x+1,y+1)
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

        print("CELLS TO ADD: ", cells_to_add)
        print("NEW COUNT: ", adjusted_count)

        if cells_to_add:
            new_sentence = Sentence(cells_to_add, adjusted_count)
            self.knowledge.append(new_sentence)
        
        # 4) [WIP] Mark any additional cells as safe or as mines
        #          if it can be concluded based on the AI's knowledge base  
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



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        raise NotImplementedError


# FOR DEBUG

def printGame(height=3, width=3, mines=1):
    game = Minesweeper(height, width, mines)
    print("===============")
    game.print()
    print()
    print("Height: ",game.height)
    print("Width: ", game.width)
    print("Mines: ",game.mines)
    # print("Board: ",game.board)
    print("Mines found: ",game.mines_found)
    print()
    print("Is it a mine? ", game.is_mine((0,1)))
    print("Which mines nearby? ", game.nearby_mines((0,1)))
    print("===============")
    print()

def printai(height=3, width=3):
    ai = MinesweeperAI(height, width)

    ai.add_knowledge((1,1), 0)
    print()

    
    print("KNOWLEDGE: ")
    for sentence in ai.knowledge:
        print("Sentence: ", sorted(sentence.cells))
        print("Count: ", sentence.count)
    print("========")
    print("SAFES: ", sorted(ai.safes))
    print("MINES: ", sorted(ai.mines))

def printSentence():
    sentence = Sentence(cells={(4,1),(4,2),(4,3), (5,1),(5,3), (6,1), (6,2), (6,3)}, count=2)
    print("Sentence: ", sentence)
    sentence.mark_safe((5,3))
    print("Sentence after marking: ", sentence)
    print(sentence.known_mines())
    print(sentence.known_safes())



if __name__ == "__main__":
    
    # # DEBUG
    height=4
    width=4
    mines=4
    printGame(height, width, mines)
    printai(height, width)

    
