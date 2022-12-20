import pygame
import sys
from copy import deepcopy
from tetrisAI import TetrisAI
import tetrominos
from random import shuffle


# create window
size = windowWidth, windowHeight = 210, 400
boardHeight, boardWidth = 20, 10
GRIDCELLSIZE = int(
    min((windowHeight - 10) / boardHeight, (windowWidth - 10) / boardWidth)
)  # 25px by 25px
gridOrigin = (10, 10)

AI = True
FPS = 10
dropTime = 2

frameDelayAfterLineClear = 1
timer = -10  # the negative gives the user time before first block moves

# create grid
grid = []
for row in range(boardHeight):
    grid.append([])
    for column in range(boardWidth):
        grid[row].append("")


# initiates pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

# initiate AI
tetrisAI = TetrisAI()


def main():
    AIMoves = []
    points = 0
    global timer

    # creates first tetromino
    tetromino = newTetrominos(grid)
    # create first ai move sequence 
    AIMoves = tetrisAI.calculateBestMove(tetromino, grid)
    

    # starts game
    while True:
        clock.tick(FPS)

        # executes user input
        executeUserInput(tetromino)

        timer += 1
        if timer >= dropTime:
            timer = 0

            if not tetromino.moveDown(grid):
                timer = -frameDelayAfterLineClear

                # place tetromino on grid
                for location in tetromino.location:
                    grid[location[1]][location[0]] = tetromino.color

                # update points and print if they changed 
                if points != (points := points + lineClear(grid)):
                    print(points)

                # creates new tetromino
                tetromino = newTetrominos(grid)

                # if piece cant be placed
                if not tetromino:
                    # end game
                    break
                drawWindow(tetromino, grid)
                if AI:
                    # find best move
                    AIMoves = tetrisAI.calculateBestMove(tetromino, grid)

        
        if AI:
            executeAIInput(AIMoves, tetromino, grid)

        drawWindow(tetromino, grid)
    pygame.quit()  # quit pygame after closing window


def executeAIInput(AIMoves, tetromino, grid):
    if len(AIMoves) != 0:
        while AIMoves[0][1] == max(
            location[1] for location in tetromino.location
        ):

            match AIMoves[0][0]:
                case "Left":
                    tetromino.moveLeft(grid)
                case "Right":
                    tetromino.moveRight(grid)
                case "Clockwise":
                    tetromino.rotateClockwise(grid)
                case "Counterclockwise":
                    tetromino.rotateCounterclockwise(grid)

            
            AIMoves.pop(0)
            if len(AIMoves) == 0:
                break


def updateGrid(tetromino: grid) -> None:
    for location in tetromino.location:
        grid[location[1]][location[0]] = tetromino.color


def lineClear(grid) -> int:
    """checks for a line clear
    if line clear is not found return 0
    else clear lines and return the number of cleared lines"""
    # inserts
    for row in grid:
        if "" not in row:
            grid.remove(row)
            grid.insert(0, [""] * len(grid[0]))
            return 1 + lineClear(grid)
    return 0


def executeUserInput(tetromino):
    for event in pygame.event.get():
        # Check if game quit
        if event.type == pygame.QUIT:
            sys.exit()

        # check for other user input
        if event.type == pygame.KEYDOWN:
            # if k is pressed, turn on AI
            if event.key == pygame.K_a:
                global AI
                AI = not AI
                print("AI is now:", AI)

            # if left arrow is pressed, move tetromino left
            if event.key == pygame.K_LEFT:
                tetromino.moveLeft(grid)

            # if right arrow is pressed, move tetromino right
            if event.key == pygame.K_RIGHT:
                tetromino.moveRight(grid)

            # if up arrow is pressed, spin tetromino clockwise
            if event.key == pygame.K_UP:
                tetromino.rotateClockwise(grid)

            # if down arrow is pressed, spin tetromino counterclockwise
            if event.key == pygame.K_DOWN:
                tetromino.rotateCounterclockwise(grid)

            # if space is pressed, hard drop tetromino
            if event.key == pygame.K_SPACE:
                tetromino.hardDrop(grid)
                global timer
                timer = dropTime


def drawWindow(tetromino, grid):
    # draw background
    screen.fill((0, 0, 0))
    # draws the grid with the corresponding colors
    for row in range(boardHeight):
        for column in range(boardWidth):
            rect = pygame.Rect(
                gridOrigin[0] + column * GRIDCELLSIZE,
                gridOrigin[1] + row * GRIDCELLSIZE,
                GRIDCELLSIZE,
                GRIDCELLSIZE,
            )
            pygame.draw.rect(
                screen,
                (127, 127, 127) if grid[row][column] == "" else grid[row][column],
                rect,
            )
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    # draws the tetromino
    for location in tetromino.location:
        rect = pygame.Rect(
            gridOrigin[0] + location[0] * GRIDCELLSIZE,
            gridOrigin[1] + location[1] * GRIDCELLSIZE,
            GRIDCELLSIZE,
            GRIDCELLSIZE,
        )
        pygame.draw.rect(screen, tetromino.color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    # draws the predicted location
    for predicted in tetromino.prediction(grid):
        rect = pygame.Rect(
            gridOrigin[0] + predicted[0] * GRIDCELLSIZE,
            gridOrigin[1] + predicted[1] * GRIDCELLSIZE,
            GRIDCELLSIZE,
            GRIDCELLSIZE,
        )
        pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    # updates the screen
    pygame.display.update()


sevenSystem = []
possibleTetrominos = [
    tetrominos.I,
    tetrominos.J,
    tetrominos.L,
    tetrominos.O,
    tetrominos.Z,
    tetrominos.S,
    tetrominos.T,
]


def newTetrominos(grid) -> str:
    """generates the next tetrominos
    Returns None if the new piece will overlap with any other piece
    returns the tetrominos otherwise"""
    global sevenSystem
    if sevenSystem == []:
        sevenSystem = deepcopy(possibleTetrominos)
        shuffle(sevenSystem)

    tetromino = sevenSystem.pop()()
    # checks if the new piece will not interfere with any other existing ones
    for location in tetromino.location:
        if grid[location[1]][location[0]] != "":
            return None

    return tetromino


if __name__ == "__main__":
    main()
