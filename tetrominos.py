class Tetrominos:
    def rotateClockwise(self, grid: list[list]) -> bool:
        """Rotates the tetromino 90 degrees clockwise and returns true
        returns false if cant be rotated"""
        # Tests that the new orientation doesn't interfere with anything,
        # then if it doesn't, it assigns the new orientation to the tetromino
        # else, it tries it in one of the other possible locations

        # creates a temp copy of tetromino in its new location for testing
        testingLocations = tuple(
            (self.location[i][0] + location[0], self.location[i][1] + location[1])
            for i, location in enumerate(
                self.clockwiseRotationTests[self.orientation // 90][1]
            )
        )

        # checks if the piece can be rotated based on tests
        for test in self.clockwiseRotationTests[self.orientation // 90][0]:
            # tests new location
            for location in testingLocations:
                if (
                    not (0 <= location[0] + test[0] < len(grid[0]))
                    or not (0 <= location[1] + test[1] < len(grid))
                    or grid[location[1] + test[1]][location[0] + test[0]] != ""
                ):

                    break  # if interference is found
            else:
                break
        else:
            return False  # cant rotate

        # updates the active tetromino location to new location
        for i in range(len(self.location)):
            self.location[i][0] = testingLocations[i][0] + test[0]
            self.location[i][1] = testingLocations[i][1] + test[1]
        # updates rotation
        self.orientation = (self.orientation + 90) % 360
        return True

    def rotateCounterclockwise(self, grid: list[list]) -> bool:
        """Rotates the tetromino 90 degrees counter clockwise and returns true
        returns false if cant be rotated"""
        # Tests that the new orientation doesn't interfere with anything,
        # then if it doesn't, it assigns the new orientation to the tetromino
        # else, it tries it in one of the other possible locations

        # creates a temp copy of tetromino in its new location for testing
        testingLocations = tuple(
            (self.location[i][0] + location[0], self.location[i][1] + location[1])
            for i, location in enumerate(
                self.counterClockwiseRotationTests[self.orientation // 90][1]
            )
        )

        # checks if the piece can be rotated based on tests
        for test in self.counterClockwiseRotationTests[self.orientation // 90][0]:
            # tests new location
            for location in testingLocations:
                if (
                    not (0 <= location[0] + test[0] < len(grid[0]))
                    or not (0 <= location[1] + test[1] < len(grid))
                    or grid[location[1] + test[1]][location[0] + test[0]] != ""
                ):

                    break  # if interference is found
            else:
                break
        else:
            return False  # cant rotate

        # updates the active tetromino location to new location
        for i in range(len(self.location)):
            self.location[i][0] = testingLocations[i][0] + test[0]
            self.location[i][1] = testingLocations[i][1] + test[1]
        # updates rotation
        self.orientation = abs((self.orientation - 90) + 360) % 360
        return True

    def moveDown(self, grid: list[list]) -> bool:
        """Moves the active pieces in the list down one block,
        returns false if the piece can not be moved down (either
        because there is already a piece there or end of array/grid)
        true otherwise"""

        # Checks for interference
        for location in self.location:
            # if interference is found return False
            if location[1] + 1 >= len(grid) or grid[location[1] + 1][location[0]] != "":
                return False

        # if no interference, update location
        for location in self.location:
            location[1] += 1
        return True

    def moveLeft(self, grid: list[list]) -> bool:
        """Moves the active pieces one block to the left"""

        # checks for interference in new location
        for location in self.location:
            if grid[location[1]][location[0] - 1] != "" or location[0] - 1 < 0:
                # if interference found
                return False

        # if no collision, update location and return
        for location in self.location:
            location[0] -= 1
        return True

    def moveRight(self, grid: list[list]) -> bool:
        """Moves the active pieces one block to the right"""

        for location in self.location:
            # checks for interference in new location
            if (
                location[0] + 1 >= len(grid[0])
                or grid[location[1]][location[0] + 1] != ""
            ):
                # if interference is found
                return False

        # if no interference, update location and return true
        for location in self.location:
            location[0] += 1
        return True

    def prediction(self, grid: list[list]) -> tuple[tuple[int, int]]:
        """Returns a tuple containing the location of predicted tetromino location"""
        for i in range(len(grid)):
            # checks for interference
            for location in self.location:
                # if interference is found
                if location[1] + i >= len(grid) or grid[location[1] + i][location[0]] != "":
                    break
            else:
                # if no interference is found
                continue
            # when interference is found return predicted location
            return ((location[0], location[1] + i - 1) for location in self.location)

    def hardDrop(self, grid: list[list]) -> None:
        """moves tetromino ot its predicted location and places it on the grid"""
        for index, location in enumerate(self.prediction(grid)):
            self.location[index][0] = location[0]
            self.location[index][1] = location[1]


class I(Tetrominos):
    color = (10, 205, 205)
    clockwiseRotationTests = (
        (  # 0 -> 90
            ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),  # Wall Kick positions
            ((2, -1), (1, 0), (0, 1), (-1, 2)),  # rotation direction
        ),
        (  # 90 -> 180
            ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),
            ((1, 2), (0, 1), (-1, 0), (-2, -1)),
        ),
        (  # 180 -> 270
            ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
            ((-2, 1), (-1, 0), (0, -1), (1, -2)),
        ),
        (  # 270 -> 0
            ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
            ((-1, -2), (0, -1), (1, 0), (2, 1)),
        ),
    )
    counterClockwiseRotationTests = (
        (  # 0 -> 270
            ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),  # Wall Kick positions
            ((1, 2), (0, 1), (-1, 0), (-2, -1)),  # rotation direction
        ),
        (  # 90 -> 0
            ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
            ((-2, 1), (-1, 0), (0, -1), (1, -2)),
        ),
        (  # 180 -> 90
            ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
            ((-1, -2), (0, -1), (1, 0), (2, 1)),
        ),
        (  # 270 -> 180
            ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
            ((2, -1), (1, 0), (0, 1), (-1, 2)),
        ),
    )

    def __init__(self):
        self.orientation = 0
        self.location = ([3, 1], [4, 1], [5, 1], [6, 1])  # starting orientation


class L(Tetrominos):
    color = (240, 120, 20)
    clockwiseRotationTests = (
        (  # 0 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),  # Wall Kick positions
            ((1, -1), (0, 0), (-1, 1), (0, 2)),  # rotation direction
        ),
        (  # 90 -> 180
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((1, 1), (0, 0), (-1, -1), (-2, 0)),
        ),
        (  # 180 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
            ((-1, 1), (0, 0), (1, -1), (0, -2)),
        ),
        (  # 270 -> 0
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((-1, -1), (0, 0), (1, 1), (2, 0)),
        ),
    )

    counterClockwiseRotationTests = (
        (  # 0 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),  # Wall Kick positions
            ((1, 1), (0, 0), (-1, -1), (-2, 0)),  # rotation direction
        ),
        (  # 90 -> 0
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((-1, 1), (0, 0), (1, -1), (0, -2)),
        ),
        (  # 180 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
            ((-1, -1), (0, 0), (1, 1), (2, 0)),
        ),
        (  # 270 -> 180
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((1, -1), (0, 0), (-1, 1), (0, 2)),
        ),
    )

    def __init__(self):
        self.orientation = 0
        self.location = ([3, 1], [4, 1], [5, 1], [5, 0])  # starting orientation


class J(Tetrominos):
    color = (10, 10, 240)
    clockwiseRotationTests = (
        (  # 0 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),  # Wall Kick positions
            ((1, -1), (0, 0), (-1, 1), (2, 0)),  # rotation direction
        ),
        (  # 90 -> 180
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((1, 1), (0, 0), (-1, -1), (0, 2)),
        ),
        (  # 180 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
            ((-1, 1), (0, 0), (1, -1), (-2, 0)),
        ),
        (  # 270 -> 0
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((-1, -1), (0, 0), (1, 1), (0, -2)),
        ),
    )

    counterClockwiseRotationTests = (
        (  # 0 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),  # Wall Kick positions
            ((1, 1), (0, 0), (-1, -1), (0, 2)),  # rotation direction
        ),
        (  # 90 -> 0
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((-1, 1), (0, 0), (1, -1), (-2, 0)),
        ),
        (  # 180 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
            ((-1, -1), (0, 0), (1, 1), (0, -2)),
        ),
        (  # 270 -> 180
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((1, -1), (0, 0), (-1, 1), (2, 0)),
        ),
    )

    def __init__(self):
        self.orientation = 0
        self.location = ([3, 1], [4, 1], [5, 1], [3, 0])  # starting orientation


class O(Tetrominos):
    color = (240, 240, 10)

    def __init__(self):
        self.orientation = 0
        self.location = ([4, 0], [5, 0], [4, 1], [5, 1])  # starting orientation

    def rotateClockwise(self, grid: list[list]) -> bool:
        return True

    def rotateCounterclockwise(self, grid: list[list]) -> bool:
        return True


class S(Tetrominos):
    color = (10, 240, 10)
    clockwiseRotationTests = (
        (  # 0 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),  # Wall Kick positions
            ((1, -1), (0, 0), (1, 1), (0, 2)),  # rotation direction
        ),
        (  # 90 -> 180
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((1, 1), (0, 0), (-1, 1), (-2, 0)),
        ),
        (  # 180 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
            ((-1, 1), (0, 0), (-1, -1), (0, -2)),
        ),
        (  # 270 -> 0
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((-1, -1), (0, 0), (1, -1), (2, 0)),
        ),
    )

    counterClockwiseRotationTests = (
        (  # 0 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),  # Wall Kick positions
            ((1, 1), (0, 0), (-1, 1), (-2, 0)),  # rotation direction
        ),
        (  # 90 -> 0
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((-1, 1), (0, 0), (-1, -1), (0, -2)),
        ),
        (  # 180 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
            ((-1, -1), (0, 0), (1, -1), (2, 0)),
        ),
        (  # 270 -> 180
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((1, -1), (0, 0), (1, 1), (0, 2)),
        ),
    )

    def __init__(self):
        self.orientation = 0
        self.location = ([3, 1], [4, 1], [4, 0], [5, 0])  # starting orientation


class T(Tetrominos):
    color = (205, 30, 220)
    clockwiseRotationTests = (
        (  # 0 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),  # Wall Kick positions
            ((1, -1), (0, 0), (-1, 1), (1, 1)),  # rotation direction
        ),
        (  # 90 -> 180
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((1, 1), (0, 0), (-1, -1), (-1, 1)),
        ),
        (  # 180 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
            ((-1, 1), (0, 0), (1, -1), (-1, -1)),
        ),
        (  # 270 -> 0
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((-1, -1), (0, 0), (1, 1), (1, -1)),
        ),
    )

    counterClockwiseRotationTests = (
        (  # 0 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),  # Wall Kick positions
            ((1, 1), (0, 0), (-1, -1), (-1, 1)),  # rotation direction
        ),
        (  # 90 -> 0
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((-1, 1), (0, 0), (1, -1), (-1, -1)),
        ),
        (  # 180 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
            ((-1, -1), (0, 0), (1, 1), (1, -1)),
        ),
        (  # 270 -> 180
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((1, -1), (0, 0), (-1, 1), (1, 1)),
        ),
    )

    def __init__(self):
        self.orientation = 0
        self.location = ([3, 1], [4, 1], [5, 1], [4, 0])  # starting orientation


class Z(Tetrominos):
    color = (240, 10, 10)
    clockwiseRotationTests = (
        (  # 0 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),  # Wall Kick positions
            ((0, 0), (-1, 1), (2, 0), (1, 1)),  # rotation direction
        ),
        (  # 90 -> 180
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((0, 0), (-1, -1), (0, 2), (-1, 1)),
        ),
        (  # 180 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
            ((0, 0), (1, -1), (-2, 0), (-1, -1)),
        ),
        (  # 270 -> 0
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((0, 0), (1, 1), (0, -2), (1, -1)),
        ),
    )

    counterClockwiseRotationTests = (
        (  # 0 -> 270
            ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),  # Wall Kick positions
            ((0, 0), (-1, -1), (0, 2), (-1, 1)),  # rotation direction
        ),
        (  # 90 -> 0
            ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
            ((0, 0), (1, -1), (-2, 0), (-1, -1)),
        ),
        (  # 180 -> 90
            ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
            ((0, 0), (1, 1), (0, -2), (1, -1)),
        ),
        (  # 270 -> 180
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
            ((0, 0), (-1, 1), (2, 0), (1, 1)),
        ),
    )

    def __init__(self):
        self.orientation = 0
        self.location = ([4, 1], [5, 1], [3, 0], [4, 0])  # starting orientation


"""
Rotation s
        0 = spawn state
        R = state resulting from a clockwise rotation ("right") from spawn
        L = state resulting from a counter-clockwise ("left") rotation from spawn
        2 = state resulting from 2 successive rotations in either direction from spawn.
        
                J, L, S, T, Z Tetromino Wall Kick Data
                Test 1	Test 2	Test 3	Test 4	Test 5
        clockwise
        0->R	(0, 0)	(-1, 0)	(-1,+1)	( 0,-2)	(-1,-2)
        R->2	(0, 0)	(+1, 0)	(+1,-1)	( 0,+2)	(+1,+2)
        2->L	(0, 0)	(+1, 0)	(+1,+1)	( 0,-2)	(+1,-2)
        L->0	(0, 0)	(-1, 0)	(-1,-1)	( 0,+2)	(-1,+2)
        
        counterclockwise
        0->L	(0, 0)	(+1, 0)	(+1,+1)	( 0,-2)	(+1,-2)
        L->2	(0, 0)	(-1, 0)	(-1,-1)	( 0,+2)	(-1,+2)
        2->R	(0, 0)	(-1, 0)	(-1,+1)	( 0,-2)	(-1,-2)
        R->0	(0, 0)	(+1, 0)	(+1,-1)	( 0,+2)	(+1,+2)
        
        
                I Tetromino Wall Kick Data
                Test 1	Test 2	Test 3	Test 4	Test 5
        clockwise
        0->R	(0, 0)	(-2, 0)	(+1, 0)	(-2,-1)	(+1,+2)
        R->2	(0, 0)	(-1, 0)	(+2, 0)	(-1,+2)	(+2,-1)
        2->L	(0, 0)	(+2, 0)	(-1, 0)	(+2,+1)	(-1,-2)
        L->0	(0, 0)	(+1, 0)	(-2, 0)	(+1,-2)	(-2,+1)
        
        counterclockwise
        0->L	(0, 0)	(-1, 0)	(+2, 0)	(-1,+2)	(+2,-1)
        L->2	(0, 0)	(-2, 0)	(+1, 0)	(-2,-1)	(+1,+2)
        2->R	(0, 0)	(+1, 0)	(-2, 0)	(+1,-2)	(-2,+1)
        R->0	(0, 0)	(+2, 0)	(-1, 0)	(+2,+1)	(-1,-2)
        """
