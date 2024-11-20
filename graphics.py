import sys
import pygame
import time

# Constants
CELLSIZE = 50
WIDTH, HEIGHT = 900, 750
ROWS, COLS = 18, 14

# global variables
colors = {
    "green1": (185, 221, 119),
    "green2": (191, 225, 125),
    "green3": (74, 117, 44),
    "vividGreen": (0, 128, 0),
    "brown1": (215, 184, 153),
    "brown2": (229, 194, 159),
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "transparentGray": (192,192,192, 20),
    "1": (0, 0, 255),
    "2": (0, 128, 0),
    "3": (255, 0, 0),
    "4": (0, 0, 128),
    "5": (128, 0, 0),
    "6": (0, 128, 128),
    "7": (1, 3, 1),
    "8": (128, 128, 128)
}
flagImage = pygame.image.load("./assets/flag.png")
flagImage = pygame.transform.scale(flagImage, (CELLSIZE // 1.5, CELLSIZE // 1.5))
bombImage = pygame.image.load("./assets/mine.png")
bombImage = pygame.transform.scale(bombImage, (CELLSIZE // 2, CELLSIZE // 2))
clockImage = pygame.image.load("./assets/clock.png")
clockImage = pygame.transform.scale(clockImage, (CELLSIZE // 2, CELLSIZE // 2))
startTime = time.time()

def finalScreen(screen: pygame.Surface, message: str, buttonColor: tuple) -> bool:
    """
    Shows a message on the screen and asks the player if they want to play again.

    Args:
        screen (pygame.Surface): The screen to show the message.
        message (str): The message to show on the screen.
        color (tuple): The color of the button.
    
    Returns:
        bool: True if the player wants to play again.
    """
    font = pygame.font.Font(None, 50)  
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill(colors["transparentGray"])

    while True:
        screen.blit(overlay, (0, 0))

        button_rect = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 50, 200, 100)
        pygame.draw.rect(screen, buttonColor, button_rect)
        
        lines = message.split("\n")
        line_height = font.get_linesize()
        for i, line in enumerate(lines):
            text = font.render(line, True, colors["white"])
            text_rect = text.get_rect(center=(button_rect.centerx, button_rect.centery - (len(lines) - 1) * line_height // 2 + i * line_height))
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # check if the player wants to play again. keys ENTER, SPACE and mouse click are accepted
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_rect.collidepoint(event.pos)) or (event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)):
                    return True
            
def checkWin(screen: pygame.Surface, clicked_cells: list[list[bool]], cells: list[list[int]], flags: list[list[bool]]) -> bool:
    """
    Checks if the player has won the game.
    The player wins the game if all cells with mines are flagged and all other cells are clicked.
    The player can choose to play again after winning the game.

    Args:
        screen (pygame.Surface): The screen to show the win message.
        clicked_cells (list[list[bool]]): The cells that have been clicked.
        cells (list[list[int]]): The cells with mines and numbers.
        flags (list[list[bool]]): The cells that have been flagged.

    Returns:
        bool: True if the player has won the game, False otherwise
    """
    for i in range(ROWS):
        for j in range(COLS):
            if (cells[i][j] == -1 and not flags[i][j]) or (cells[i][j] != -1 and not clicked_cells[i][j]):
                return False
    return finalScreen(screen, "You Win!\nPlay Again?", colors["vividGreen"])

def gameOver(screen: pygame.Surface, cells: list[list[int]], flags: list[list[bool]]) -> bool:
    """
    Shows all mines and ends the game.
    At the end of the game, the player can choose to play again.

    Args:
        screen (pygame.Surface): The screen to show the mines.
        cells (list[list[int]]): The cells with mines and numbers.
        flags (list[list[bool]]): The cells that have been flagged.

    Returns:
        bool: True if the player wants to play again, False otherwise.
    """
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(i * 50, j * 50, 50, 50)
            if cells[i][j] == -1 and not flags[i][j]:
                screen.blit(bombImage, rect.move((CELLSIZE - bombImage.get_width()) // 2, (CELLSIZE - bombImage.get_height()) // 2))
            elif flags[i][j] and cells[i][j] != -1:
                pygame.draw.line(screen, colors["red"], rect.topleft, rect.bottomright, 5)
                pygame.draw.line(screen, colors["red"], rect.bottomleft, rect.topright, 5)
    pygame.display.flip()
    pygame.time.wait(1000)
    return finalScreen(screen, "Game Over!\nPlay Again?", colors["red"])

def drawBottomBar(screen: pygame.Surface, flagsCount: int) -> None:
    """
    Draws the bottom bar of the screen.
    The bottom bar shows the number of flags left and the time elapsed.

    Args:
        screen (pygame.Surface): The screen to draw the bottom bar on.
        flagsCount (int): The number of flags left.
    """
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, colors["green3"], pygame.Rect(0, HEIGHT - CELLSIZE, WIDTH, CELLSIZE))
    screen.blit(flagImage, (10, HEIGHT - CELLSIZE // 2 - flagImage.get_height() // 2))
    text = font.render(str(flagsCount), True, colors["white"])
    screen.blit(text, (10 + flagImage.get_width() + 10, HEIGHT - CELLSIZE // 2 - text.get_height() // 2))
    timeElapsed = int(time.time() - startTime)
    text = font.render(str(timeElapsed), True, colors["white"])
    screen.blit(text, (WIDTH - 10 - text.get_width(), HEIGHT - CELLSIZE // 2 - text.get_height() // 2))
    screen.blit(clockImage, (WIDTH - 10 - text.get_width() - 10 - clockImage.get_width(), HEIGHT - CELLSIZE // 2 - clockImage.get_height() // 2))

def drawGrid(screen: pygame.Surface, clicked_cells: list[list[bool]], cells: list[list[int]], flags: list[list[bool]]) -> None:
    """
    Draws a grid on the screen, with the following rules:
    - If a cell has a number, the number is shown.
    - If a flag has been placed on a cell, the flag is shown.
    - If a mine is clicked, all mines are shown.

    Args:
        screen (pygame.Surface): The screen to draw the grid on.
        clicked_cells (list[list[bool]]): The cells that have been clicked.
        cells (list[list[int]]): The cells with mines and numbers.
        flags (list[list[bool]]): The cells that have been flagged.
    """
    font = pygame.font.Font(None, 36)

    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(i * CELLSIZE, j * CELLSIZE, CELLSIZE, CELLSIZE)
            color1 = colors["brown1"] if clicked_cells[i][j] else colors["green1"]
            color2 = colors["brown2"] if clicked_cells[i][j] else colors["green2"]
            pygame.draw.rect(screen, color1 if (i + j) % 2 == 0 else color2, rect)

            if clicked_cells[i][j] and cells[i][j] >= 1:
                text = font.render(str(cells[i][j]), True, colors[str(cells[i][j])])
                screen.blit(text, rect.move((CELLSIZE - text.get_width()) // 2, (CELLSIZE - text.get_height()) // 2))
            elif flags[i][j] and not clicked_cells[i][j]:
                screen.blit(flagImage, rect.move((CELLSIZE - flagImage.get_width()) // 2, (CELLSIZE - flagImage.get_height()) // 2))
