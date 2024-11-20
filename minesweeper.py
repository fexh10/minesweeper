import graphics
from random import randint
    
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
            if i + x >= 0 and i + x < graphics.ROWS and j + y >= 0 and j + y < graphics.COLS and not flags[i + x][j + y]:
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
            if i + x >= 0 and i + x < graphics.ROWS and j + y >= 0 and j + y < graphics.COLS:
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

    cells = [[0 for _ in range(graphics.COLS)] for _ in range(graphics.ROWS)]

    # generate mines
    for i in range(40):
        x, y = randint(0, graphics.ROWS - 1), randint(0, graphics.COLS - 1)
        while cells[x][y] == -1:
            x, y = randint(0, graphics.ROWS - 1), randint(0, graphics.COLS - 1)
        cells[x][y] = -1

    # generate numbers
    for i in range(graphics.ROWS):
        for j in range(graphics.COLS):
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
    i = x // graphics.CELLSIZE
    j = y // graphics.CELLSIZE
    return i, j

def restartVar() -> tuple[list[list[bool]], list[list[bool]], list[list[int]], int]:
    """
    Restarts the game variables and the time.

    Returns:
        tuple[list[list[bool]], list[list[bool]], list[list[int]], int]: The updated game variables.
    """
    clicked_cells = [[False for _ in range(graphics.COLS)] for _ in range(graphics.ROWS)]
    flags = [[False for _ in range(graphics.COLS)] for _ in range(graphics.ROWS)]
    cells = populateCells()
    flagsCount = 40
    graphics.startTime = graphics.time.time()
    return clicked_cells, flags, cells, flagsCount
                            
def main() -> None:
    """
    Main function for the game.
    This function initializes the game and runs the game loop.
    """
    graphics.pygame.init()
    screen = graphics.pygame.display.set_mode((graphics.WIDTH, graphics.HEIGHT))
    graphics.pygame.display.set_caption("Minesweeper")
    icon = graphics.pygame.image.load("./assets/icon.png")
    icon = graphics.pygame.transform.scale(icon, (32, 32))
    graphics.pygame.display.set_icon(icon)
    clock = graphics.pygame.time.Clock()

    running = True
    clicked_cells = [[False for _ in range(graphics.COLS)] for _ in range(graphics.ROWS)]
    flags = [[False for _ in range(graphics.COLS)] for _ in range(graphics.ROWS)]
    flagsCount = 40

    cells = populateCells()

    while running:
        for event in graphics.pygame.event.get():
            if event.type == graphics.pygame.QUIT:
                running = False
            elif event.type == graphics.pygame.MOUSEBUTTONDOWN:
                cell = getCellFromMouse(graphics.pygame.mouse.get_pos())
                if cell:
                    i, j = cell
                    if j >= graphics.COLS: continue
                    if event.button == 1 and not clicked_cells[i][j] and not flags[i][j]:
                        if cells[i][j] == 0:
                            clicked_cells = checkEmptyCells(i, j, cells, clicked_cells, flags)
                        elif cells[i][j] == -1:
                            if graphics.gameOver(screen, cells, flags):
                                clicked_cells, flags, cells, flagsCount = restartVar()
                        else:
                            clicked_cells[i][j] = True
                    elif event.button == 3:
                        if (flagsCount > 0 or flags[i][j]) and not clicked_cells[i][j]:
                            flags[i][j] = not flags[i][j]
                            if flags[i][j]:
                                flagsCount -= 1
                            else:
                                flagsCount += 1        
        screen.fill("black")
        graphics.drawBottomBar(screen, flagsCount)
        graphics.drawGrid(screen, clicked_cells, cells, flags)
        graphics.pygame.display.flip()
        clock.tick(60)
        #check for win
        if flagsCount == 0 and graphics.checkWin(screen, clicked_cells, cells, flags):
            clicked_cells, flags, cells, flagsCount = restartVar()

    graphics.pygame.quit()

if __name__ == "__main__":
    main()