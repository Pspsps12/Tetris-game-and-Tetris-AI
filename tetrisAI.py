from copy import deepcopy
from node import Node


class TetrisAI:
    aggregateHeightMultiplier = -20
    completeLinesMultiplier = 13
    holesMultiplier = -17
    bumpinessMultiplier = -7
    blocksAboveHolesMultiplier = -4

    def gridValue(self, grid):
        completeLines = 0

        for row in grid:
            if "" not in row:
                completeLines += 1

        highestPoints = [0] * len(grid[0])

        for column in range(len(grid[0])):
            for row in range(len(grid)):
                if grid[row][column] != "":
                    highestPoints[column] = len(grid) - row
                    break

        aggregateHeight = sum(highestPoints)

        blocksAboveHoles = 0
        holes = 0
        for column in range(len(grid[0])):
            holeFound = False
            for row in range(len(grid) - 1, len(grid) - highestPoints[column] - 1, -1):
                if grid[row][column] == "":
                    holeFound = True
                    holes += 1
                else:
                    if holeFound:
                        blocksAboveHoles += 1

        bumpiness = 0
        for i in range(len(highestPoints) - 1):
            bumpiness += abs(highestPoints[i] - highestPoints[i + 1])

        return (
            aggregateHeight * self.aggregateHeightMultiplier
            + completeLines * self.completeLinesMultiplier
            + holes * self.holesMultiplier
            + bumpiness * self.bumpinessMultiplier
            + blocksAboveHoles * self.blocksAboveHolesMultiplier
        )

    def findPossibleMoves(self, previousMove, tetromino, grid, previousMoves):
        # gets the current y value of tetromino
        maxY = self.maxY(tetromino.location)

        if previousMove != "Counterclockwise":
            # -------------------------move Clockwise---------------------------------------------------
            # creates a copy of the tetromino
            newTetromino = deepcopy(tetromino)

            # tries to rotate the tetromino
            if newTetromino.rotateClockwise(grid):

                # if tetromino was able to rotate
                # check if this position was explored already
                if newTetromino.location not in self.visitedPositions:
                    # if not
                    # add this position to visited positions
                    self.visitedPositions.append(newTetromino.location)

                    # creates a copy of previous moves, and appends this move
                    newPreviousMoves = deepcopy(previousMoves)
                    newPreviousMoves.append(("Clockwise", maxY))

                    # adds this position to moves to execute
                    self.movesToExecute.append(
                        Node("Clockwise", newTetromino, newPreviousMoves)
                    )

        if previousMove != "Clockwise":
            # -------------------------move Counterclockwise--------------------------------------------
            # creates a copy of the tetromino
            newTetromino = deepcopy(tetromino)

            # tries to rotate the tetromino
            if newTetromino.rotateCounterclockwise(grid):

                # if tetromino was able to rotate
                # check if this position was explored already
                if newTetromino.location not in self.visitedPositions:
                    # if not
                    # add this position to visited positions
                    self.visitedPositions.append(newTetromino.location)

                    # creates a copy of previous moves, and appends this move
                    newPreviousMoves = deepcopy(previousMoves)
                    newPreviousMoves.append(("Counterclockwise", maxY))

                    # adds this position to moves to execute
                    self.movesToExecute.append(
                        Node("Counterclockwise", newTetromino, newPreviousMoves)
                    )

        if previousMove != "Right":
            # -------------------------moveLeft--------------------------------------------------------
            # creates a copy of the tetromino
            newTetromino = deepcopy(tetromino)

            # tries to move the tetromino
            if newTetromino.moveLeft(grid):

                # if tetromino was able to move
                # check if this position was explored already
                if newTetromino.location not in self.visitedPositions:
                    # if not
                    # add this position to visited positions
                    self.visitedPositions.append(newTetromino.location)

                    # creates a copy of previous moves, and appends this move
                    newPreviousMoves = deepcopy(previousMoves)
                    newPreviousMoves.append(("Left", maxY))
                    # adds this position to moves to execute
                    self.movesToExecute.append(
                        Node("Left", newTetromino, newPreviousMoves)
                    )

        if previousMove != "Left":
            # -------------------------moveRight-------------------------------------------------------
            # creates a copy of the tetromino
            newTetromino = deepcopy(tetromino)

            # tries to move the tetromino
            if newTetromino.moveRight(grid):

                # if tetromino was able to move
                # check if this position was explored already
                if newTetromino.location not in self.visitedPositions:
                    # if not
                    # add this position to visited positions
                    self.visitedPositions.append(newTetromino.location)

                    # creates a copy of previous moves, and appends this move
                    newPreviousMoves = deepcopy(previousMoves)
                    newPreviousMoves.append(("Right", maxY))
                    # adds this position to moves to execute
                    self.movesToExecute.append(
                        Node("Right", newTetromino, newPreviousMoves)
                    )

        # -------------------------move Down-----------------------------------------------------------
        newTetromino = deepcopy(tetromino)
        # tries to move down the tetromino
        if newTetromino.moveDown(grid):
            # if tetromino was able to move
            # check if this position was explored already
            if newTetromino.location not in self.visitedPositions:
                # if not
                # add this position to visited positions
                self.visitedPositions.append(newTetromino.location)

                # adds this position to moves to execute
                self.movesToExecute.append(Node(None, newTetromino, previousMoves))
        else:
            # if tetromino was not able to move
            # saves the tetromino final location
            self.possibleFinalPositions.append(newTetromino.location)
            # saves the moves it took to get to this destination
            self.possibleFinalPositionsMoves.append(deepcopy(previousMoves))

    def maxY(self, l: tuple[list[int, int]]):
        return max(l, key=lambda pair: pair[1])[1]

    def calculateBestMove(self, tetromino, grid: list):
        """returns a list of functions that would lead to the best move"""
        self.movesToExecute = []
        self.visitedPositions = []
        self.possibleFinalPositions = []
        self.possibleFinalPositionsMoves = []

        grid = deepcopy(grid)
        activeTetrominoLocation = deepcopy(tetromino.location)

        space = 0
        for i in range(self.maxY(activeTetrominoLocation) + 1, len(grid)):
            if all(elem == "" for elem in grid[i]):
                space += 1

        for location in activeTetrominoLocation:
            location[1] += space - 1

        # ---------------------------------------------------------------------------------------------------
        # creates the first move
        self.movesToExecute.append(Node(None, tetromino, []))

        # while there are more moves left to execute,
        while self.movesToExecute:
            self.findPossibleMoves(
                self.movesToExecute[0].lastMove,
                self.movesToExecute[0].tetromino,
                grid,
                self.movesToExecute[0].previousMoves,
            )
            self.movesToExecute.pop(0)

        bestGridMoves = []
        bestMoveValue = -1000000

        # calculates which move is the best
        for tetrominoLocation, moves in zip(
            self.possibleFinalPositions, self.possibleFinalPositionsMoves
        ):
            # creates a copy of the grid
            newGrid = deepcopy(grid)
            # places tetromino on the grid
            for location in tetrominoLocation:
                newGrid[location[1]][location[0]] = tetromino.color
            # gets the value of grid
            moveValue = self.gridValue(newGrid)
            # if this grid value is the highest,
            if moveValue > bestMoveValue:
                # update highest move value
                # and add the move to the best moves
                bestMoveValue = moveValue
                bestGridMoves = [moves]

            elif (
                moveValue == bestMoveValue
            ):  # if this move has equal value as best move
                # add this move to best moves array
                bestGridMoves.append(moves)

        # return the shortest list of moves
        return min(bestGridMoves, key=len)
