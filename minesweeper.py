import pygame
from random import randint

# Constants
CELLSIZE = 50
WIDTH, HEIGHT = 900, 700
ROWS, COLS = 18, 14

colors = {
    "green1": (185, 221, 119),
    "green2": (191, 225, 125),
    "brown1": (215, 184, 153),
    "brown2": (229, 194, 159),
    "-1": (0, 0, 0),
    "1": (0, 0, 255),
    "2": (0, 128, 0),
    "3": (255, 0, 0),
    "4": (0, 0, 128),
    "5": (128, 0, 0),
    "6": (0, 128, 128),
    "7": (1, 3, 1),
    "8": (128, 128, 128)
}

def checkEmptyCells(i: int, j: int, cells: list[list[int]], clicked_cells: list[list[bool]], flags: list[list[bool]]) -> list[list[bool]]:
    """
    If (i, j) is an empty cell, show all the empty cells around it until a number cell is reached.

    Args:
        i (int): The row index of the cell.
        j (int): The column index of the cell.
        cells (list[list[int]]): The cells with mines and numbers.
        clicked_cells (list[list[bool]]): The cells that have been clicked.
        flags (list[list[bool]]): The cells that have been flagged.

    Returns:
        list[list[bool]]: The updated clicked cells.
    """
    clicked_cells[i][j] = True
    for x in range(-1, 2):
        for y in range(-1, 2):
            if i + x >= 0 and i + x < ROWS and j + y >= 0 and j + y < COLS and not flags[i + x][j + y]:
                if not clicked_cells[i + x][j + y] and cells[i + x][j + y] == 0:
                    clicked_cells = checkEmptyCells(i + x, j + y, cells, clicked_cells, flags)
                else:
                    clicked_cells[i + x][j + y] = True

    return clicked_cells

def checkCell(i: int, j: int, cells: list[list[int]]) -> int:
    """
    Checks the number of mines around a cell.

    Args:
        i (int): The row index of the cell.
        j (int): The column index of the cell.
        cells (list[list[int]]): The cells with mines and numbers.
    
    Returns:
        int: The number of mines around the cell.
    """

    number = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if i + x >= 0 and i + x < ROWS and j + y >= 0 and j + y < COLS:
                if cells[i + x][j + y] == -1:
                    number += 1
    return number

def populateCells() -> list[list[int]]:
    """
    Populates the cells with mines and numbers.
    The total number of mines is 40.
    The cells are represented as follows:
    - If a cell has a mine, it is represented by -1.
    - If a cell has no mines, it is represented by 0.
    - If a cell has n mines, it is represented by n.
    
    Returns:
        list[list[int]]: The cells with mines and numbers.
    """

    cells = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # generate mines
    for i in range(40):
        x, y = randint(0, ROWS - 1), randint(0, COLS - 1)
        while cells[x][y] == -1:
            x, y = randint(0, ROWS - 1), randint(0, COLS - 1)
        cells[x][y] = -1

    # generate numbers
    for i in range(ROWS):
        for j in range(COLS):
            if cells[i][j] != -1:
               cells[i][j] = checkCell(i, j, cells)

    return cells

def getCellFromMouse(pos: tuple[int, int]) -> tuple[int, int]:
    """
    Returns the cell coordinates (i, j) from the mouse position.

    Args:
        pos (tuple[int, int]): The mouse position.
    
    Returns:
        tuple[int, int]: The cell coordinates (i, j).
    """
    x, y = pos
    i = x // CELLSIZE
    j = y // CELLSIZE
    return i, j

def drawGrid(screen: pygame.Surface, clicked_cells: list[list[bool]], cells: list[list[int]], flags: list[list[bool]]) -> None:
    """
    Draws a 18 x 14 grid on the screen.
    If a cell has been clicked, the cell is shown.

    Args:
        screen (pygame.Surface): The screen to draw the grid on.
        clicked_cells (list[list[bool]]): The cells that have been clicked.
        cells (list[list[int]]): The cells with mines and numbers.
        flags (list[list[bool]]): The cells that have been flagged.
    """
    font = pygame.font.Font(None, 36)
    flagImage = pygame.image.load("./assets/flag.svg")
    flagImage = pygame.transform.scale(flagImage, (CELLSIZE // 2, CELLSIZE // 2))

    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(i * 50, j * 50, 50, 50)
            color1 = colors["brown1"] if clicked_cells[i][j] else colors["green1"]
            color2 = colors["brown2"] if clicked_cells[i][j] else colors["green2"]
            pygame.draw.rect(screen, color1 if (i + j) % 2 == 0 else color2, rect)

            if clicked_cells[i][j] and cells[i][j] != 0:
                text = font.render(str(cells[i][j]), True, colors[str(cells[i][j])])
                screen.blit(text, rect.move((CELLSIZE - text.get_width()) // 2, (CELLSIZE - text.get_height()) // 2))
            elif flags[i][j] and not clicked_cells[i][j]:
                screen.blit(flagImage, rect.move((CELLSIZE - flagImage.get_width()) // 2, (CELLSIZE - flagImage.get_height()) // 2))

def main() -> None:
    """
    Main function for the game.
    This function initializes the game and runs the game loop.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    running = True
    clicked_cells = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flags = [[False for _ in range(COLS)] for _ in range(ROWS)]

    cells = populateCells()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = getCellFromMouse(pygame.mouse.get_pos())
                if cell:
                    i, j = cell
                    if event.button == 1 and not clicked_cells[i][j] and not flags[i][j]:
                        if cells[i][j] == 0:
                            clicked_cells = checkEmptyCells(i, j, cells, clicked_cells, flags)
                        clicked_cells[i][j] = True
                    elif event.button == 3:
                        flags[i][j] = not flags[i][j]
                
        screen.fill("black")
        drawGrid(screen, clicked_cells, cells, flags)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()