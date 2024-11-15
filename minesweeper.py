import pygame

# Constants
GREEN1 = (185, 221, 119)
GREEN2 = (191, 225, 125)
CELLSIZE = 50
WIDTH, HEIGHT = 900, 700

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

def drawGrid(screen: pygame.Surface) -> None:
    """
    Draws a 18 x 14 grid on the screen.
    The cells are clickable and the grid is drawn using lines.

    Args:
        screen (pygame.Surface): The screen to draw the grid on.
    """
    for i in range(18):
        for j in range(14):
            rect = pygame.Rect(i * 50, j * 50, 50, 50)
            pygame.draw.rect(screen, GREEN1 if (i + j) % 2 == 0 else GREEN2, rect)

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
    clicked_cells = [[False for _ in range(14)] for _ in range(18)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = getCellFromMouse(pygame.mouse.get_pos())
                if cell:
                    i, j = cell
                    clicked_cells[i][j] = not clicked_cells[i][j]
                
        screen.fill("black")
        drawGrid(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()