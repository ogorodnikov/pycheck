from functools import reduce
from itertools import cycle


class Board:
    def __init__(self, rows):
        self.rows = rows
        height = len(rows)
        width = len(rows[0])

        self.all_cells = {complex(y, x): rows[y][x] for x in range(width) for y in range(height)}
        self.number_cells = {cell for cell in self.all_cells
                             if self.all_cells[cell] != 0}

        self.rectangles = [Rectangle(cell, self)
                           for cell in self.number_cells]
        self.free_cells = self.all_cells.keys() - self.number_cells

        self.rectangle_cycle = cycle(sorted(self.rectangles, key=lambda rectangle: -rectangle.number))

    @property
    def rectangles_coordinates(self):
        coordinates = set()
        for rectangle in self.rectangles:
            minimum = min(rectangle.used_cells, key=abs)
            maximum = max(rectangle.used_cells, key=abs)
            rectangle_coordinates = tuple(map(int, (minimum.real, minimum.imag, maximum.real, maximum.imag)))
            coordinates.add(rectangle_coordinates)
        return coordinates


class Rectangle:
    def __init__(self, cell, board):
        self.cell = cell
        self.board = board
        self.used_cells = {self.cell}
        self.number = board.all_cells[cell]
        self.expansion_directions = {1j, 1, -1j, -1}

    def recalculate_used_cells(self):

        # for x in range(30):
        #     for y in range(40):
        #         if x * y == 42:
        #             print(x, y, x*y)
        # quit()

        possible_used_cells = []
        q = [(self.used_cells, self.expansion_directions.copy())]

        while q:
            cells, expansion_directions = q.pop()

            new_expansion_directions = expansion_directions.copy()
            level_entry = []

            # print('A:')
            # self.print_cells(cells, self.board.rows)
            # print()

            for delta in expansion_directions.copy():

                new_cells = {cell + delta for cell in cells} | cells

                # print('New cells:')
                # self.print_cells(new_cells, self.board.rows)

                if not all(cell in self.board.free_cells | self.used_cells
                           for cell in new_cells):
                    # print('---- Obstacle')
                    # print()

                    new_expansion_directions -= {delta}
                    # print('---- Expansion directions:', new_expansion_directions)
                    continue

                if len(new_cells) > self.number:
                    continue

                if len(new_cells) == self.number:
                    possible_used_cells.append(new_cells)

                level_entry = [(old_cells, new_expansion_directions)
                               for old_cells, old_expansion_directions in level_entry]

                level_entry.append((new_cells, new_expansion_directions))

                # q.append((new_cells, new_expansion_directions))

            q.extend(level_entry)

        all_possible_cells = reduce(set.union, possible_used_cells, set())

        common_cells = {cell for cell in all_possible_cells
                        if all(cell in used_cells
                               for used_cells in possible_used_cells)}

        self.used_cells = common_cells
        self.board.free_cells -= common_cells

        print('==== Rectangle recalculated:', self.number, self.cell)
        print('Possible used cells:        ', possible_used_cells)
        print('All possible cells:         ', all_possible_cells)
        print('Common cells:               ', common_cells)
        self.print_cells(common_cells, self.board.rows)

    @property
    def is_complete(self):
        return len(self.used_cells) == self.number

    def print_cells(self, cells, grid):
        height = len(grid)
        width = len(grid[0])

        for y in range(height):
            row = ''
            for x in range(width):
                cell = complex(y, x)
                if cell in cells:
                    row += 'X'
                elif cell in self.board.number_cells:
                    row += str(self.board.all_cells[cell])[-1]
                else:
                    row += '.'
            print(row)


def rectangles(grid):
    board = Board(grid)

    while True:

        next_rectangle = next(board.rectangle_cycle)

        print('>>>> Next rectangle:', next_rectangle.number, next_rectangle.cell)

        if next_rectangle.is_complete:
            continue

        next_rectangle.recalculate_used_cells()

        # if next_rectangle.number == 7:
        #     input()

        if all(rectangle.is_complete for rectangle in board.rectangles):
            print('==== All complete')
            break

    print('Rectangles')
    for rectangle in board.rectangles:
        print(rectangle.number, len(rectangle.used_cells))

    coordinates = board.rectangles_coordinates
    print('Coordinates:', coordinates)

    return coordinates


if __name__ == '__main__':
    GRIDS = (
        [[3, 0, 0, 0, 0, 2],
         [2, 0, 0, 4, 0, 0],
         [0, 5, 0, 0, 0, 0],
         [3, 0, 3, 2, 0, 0],
         [0, 0, 2, 0, 0, 6],
         [0, 0, 0, 4, 0, 0]],
        [[6, 0, 0, 0, 0, 0, 0, 2, 0],
         [0, 2, 0, 2, 0, 0, 4, 0, 0],
         [0, 0, 0, 0, 0, 0, 5, 0, 0],
         [0, 12, 2, 0, 5, 0, 0, 0, 0],
         [0, 0, 2, 0, 3, 0, 2, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 2, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 7],
         [0, 0, 3, 0, 0, 12, 0, 0, 0],
         [0, 2, 0, 0, 0, 4, 0, 0, 4]],
        [[2, 6, 0, 0, 0, 0, 0, 3],
         [0, 2, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 8, 0, 0],
         [4, 0, 0, 2, 0, 0, 0, 0],
         [0, 0, 6, 0, 0, 0, 2, 2],
         [0, 2, 0, 0, 0, 0, 0, 6],
         [2, 0, 0, 0, 0, 0, 0, 0],
         [0, 2, 0, 0, 0, 0, 0, 0],
         [0, 0, 8, 0, 0, 0, 0, 0],
         [3, 0, 0, 3, 14, 0, 0, 4],
         [0, 0, 0, 0, 4, 0, 3, 0]],
        [[0, 0, 0, 2, 0, 3, 4, 0, 4, 0, 0, 0, 3, 0, 0, 2],
         [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 6, 0, 0, 2, 0, 3, 0, 0, 6, 6, 0, 0, 4],
         [0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 16, 0, 4, 0, 0],
         [21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
         [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
         [0, 0, 0, 0, 0, 3, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0]],
        # [[0, 0, 2, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0], [4, 9, 0, 3, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0],
        #  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        #  [0, 0, 0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #  [6, 0, 0, 0, 0, 0, 0, 6, 0, 10, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0],
        #  [0, 0, 0, 20, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        #  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0], [2, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 2, 3, 0, 0],
        #  [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 2, 0, 0], [6, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 2, 4, 0, 0],
        #  [0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 3]],
        [[3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [0, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0],
         [0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 8, 0, 4],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
         [3, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0],
         [3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 2, 0, 0, 4, 0],
         [0, 2, 4, 0, 0, 0, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 5, 0, 0, 0, 0, 12, 0, 0],
         [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
         [2, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 4]],
    )


    def checker(grid, result):
        from itertools import product
        try:
            result = list(result)
        except TypeError:
            raise AssertionError('Your result must be iterable.')
        nb_rects = sum(cell != 0 for row in grid for cell in row)
        if len(result) != nb_rects:
            print(f'There are {nb_rects} rectangles to detect, '
                  f'but you gave {len(result)} rectangle(s).')
        nb_rows, nb_cols = len(grid), len(grid[0])
        colored_grid = [[0 for _ in range(nb_cols)] for _ in range(nb_rows)]
        prev_rects = set()
        for color, rect in enumerate(result, 1):
            assert (isinstance(rect, (tuple, list)) and len(rect) == 4
                    and all(isinstance(coord, int) for coord in rect)), \
                (f'{rect} does not represent a rectangle, '
                 'it should be a tuple/list of four integers.')
            assert tuple(rect) not in prev_rects, \
                f'You gave the same rectangle {rect} twice.'
            prev_rects.add(tuple(rect))
            x1, y1, x2, y2 = rect
            assert x1 <= x2 and y1 <= y2, \
                (f'The rectangle {rect} must be '
                 '(top left coords, bottom right coords).')
            for x, y in ((x1, y1), (x2, y2)):
                assert 0 <= x < nb_rows and 0 <= y < nb_cols, \
                    (f'The rectangle {rect} contains {x, y} '
                     'which is not in the grid.')
            area = (x2 + 1 - x1) * (y2 + 1 - y1)
            grid_area = None
            for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
                assert not colored_grid[x][y], \
                    (f'Rectangle #{color} intersects '
                     f'rectangle #{colored_grid[x][y]} at {x, y}.')
                colored_grid[x][y] = color
                if grid[x][y]:
                    assert grid_area is None, \
                        (f'The rectangle {rect} contains two area values: '
                         f'{grid_area} and {grid[x][y]}.')
                    grid_area = grid[x][y]
                    assert grid[x][y] == area, \
                        (f'The rectangle {rect} have area={area} '
                         f'and contains another area value: {grid[x][y]}.')
            assert grid_area is not None, f'{rect} contains no area value.'
        nb_uncovered = sum(not cell for row in colored_grid for cell in row)
        assert not nb_uncovered, f'{nb_uncovered} cells are still not covered.'


    for test_nb, grid in enumerate(GRIDS, 1):
        result = rectangles([row[:] for row in grid])
        try:
            checker(grid, result)
        except AssertionError as error:
            print(f'You failed the test #{test_nb}:')
            print(error.args[0])
            break
    else:
        print('Well done! Click on "Check" for bigger tests.')
