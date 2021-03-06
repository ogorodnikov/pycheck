class Grid:
    def __init__(self, rows):
        height = len(rows)
        width = len(rows[0])

        self.all_cells = {complex(y, x): rows[y][x] for x in range(width) for y in range(height)}
        self.empty_cells = {cell for cell in self.all_cells
                            if self.all_cells[cell] == 0}

        self.used_cells = set()
        initial_cell = self.get_unused_number_cell
        self.number = self.all_cells[initial_cell]
        self.rectangle = {initial_cell}
        self.used_cells = {initial_cell}
        self.expansion_directions = {1j, 1, -1j, -1}
        self.checked = set()
        self.complete_rectangles = []

    def __repr__(self):
        stats = f'    All cells:    {self.all_cells}    \n' + \
                f'    Empty cells:  {self.empty_cells}  \n'
        values = '\n'.join((f'    Complete:     {self.complete_rectangles}',
                            f'    Used cells:   {self.used_cells}',
                            f'    Number:       {self.number}',
                            f'    Rectangle:    {self.rectangle}'))
        return values

    def copy(self):
        new_grid = Grid.__new__(Grid)

        new_grid.all_cells = self.all_cells.copy()
        new_grid.empty_cells = self.empty_cells.copy()

        new_grid.number = self.number
        new_grid.rectangle = self.rectangle.copy()
        new_grid.used_cells = self.used_cells.copy()
        new_grid.expansion_directions = self.expansion_directions.copy()
        new_grid.checked = self.checked
        new_grid.complete_rectangles = self.complete_rectangles.copy()

        return new_grid

    @property
    def get_unused_number_cell(self):
        number_cells = {cell for cell in self.all_cells
                        if self.all_cells[cell] != 0}
        unused_number_cells = number_cells - self.used_cells
        max_number = max(self.all_cells[cell] for cell in unused_number_cells)
        max_unused_number_cell = next(cell for cell in unused_number_cells if self.all_cells[cell] == max_number)
        return max_unused_number_cell

    # @property
    # def get_unused_number_cell(self):
    #     number_cells = {cell for cell in self.all_cells
    #                     if self.all_cells[cell] != 0}
    #     unused_number_cells = number_cells - self.used_cells
    #     best_cell = min(unused_number_cells, key=lambda cell: abs(cell) / self.all_cells[cell])
    #     return best_cell

    @property
    def is_all_parsed(self):
        return self.used_cells == set(self.all_cells.keys())

    @property
    def rectangles_coordinates(self):
        coordinates = set()
        for rectangle in self.complete_rectangles:
            minimum = min(rectangle, key=abs)
            maximum = max(rectangle, key=abs)
            rectangle_coordinates = tuple(map(int, (minimum.real, minimum.imag, maximum.real, maximum.imag)))
            coordinates.add(rectangle_coordinates)
        return coordinates

    def print_rectangles(self, grid):
        print('Grid:')
        [print(row) for row in grid]
        print()

        height = len(grid)
        width = len(grid[0])

        rectangle_dict = {i: rectangle for i, rectangle in enumerate(self.complete_rectangles)}

        for y in range(height):
            row = ''
            for x in range(width):
                cell = complex(y, x)
                letter = ''
                for i, rectangle in rectangle_dict.items():
                    if cell in rectangle:
                        letter = str(i)[-1]
                row += letter or '.'
            print(row)
        print()
        # print('Rectangle dict:', rectangle_dict, len(rectangle_dict), height * width)


def rectangles(grid):
    print('Grid:')
    [print(row) for row in grid]

    tick = 0
    q = [(0, Grid(grid))]

    while q:
        level, g = q.pop()

        if not tick % 10000:
            print('Tick:', tick, len(g.complete_rectangles))

        for delta in g.expansion_directions.copy():
            tick += 1

            new_cells = {cell + delta for cell in g.rectangle} - g.rectangle

            if any(cell not in g.empty_cells - g.used_cells
                   for cell in new_cells):
                g.expansion_directions -= {delta}
                continue

            new_g = g.copy()
            new_g.rectangle = g.rectangle | new_cells

            if len(new_g.rectangle) > new_g.number:
                continue

            rectangle_hash = hash(tuple(new_g.rectangle))
            if rectangle_hash in new_g.checked:
                # print('---- Rectangle already checked')
                # print('     Rectangle:', new_g.rectangle)
                # print('     Rectangle hash:', rectangle_hash)
                # print('     Checked:  ', new_g.checked)
                # new_g.print_rectangles(grid)
                # input()
                continue
            new_g.checked.add(rectangle_hash)

            new_g.used_cells = g.used_cells | new_cells



            if len(new_g.rectangle) == new_g.number:

                new_g.complete_rectangles.append(new_g.rectangle)

                # print('Complete rectangles count:', len(new_g.complete_rectangles))

                # complete_rectangles_len = sum(map(len, new_g.complete_rectangles))
                # total_len = len(new_g.all_cells)
                #
                # print('    +++ Adding new rectangle:', new_g.rectangle)
                # print('        Level:               ', level)
                # print('        Complete rectangles: ', new_g.complete_rectangles)
                # print(f'        {complete_rectangles_len} of {total_len}')

                if new_g.is_all_parsed:
                    new_g.print_rectangles(grid)
                    coordinates = new_g.rectangles_coordinates
                    print('Coordinates:', coordinates)
                    return coordinates

                new_initial_cell = new_g.get_unused_number_cell

                new_g.number = new_g.all_cells[new_initial_cell]
                new_g.rectangle = {new_initial_cell}
                new_g.used_cells |= {new_initial_cell}
                new_g.expansion_directions = {1j, 1, -1j, -1}
                new_g.checked = set()

            q.append((level + 1, new_g))

    return []


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
        [[0, 0, 2, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0], [4, 9, 0, 3, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0],
         [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
         [0, 0, 0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [6, 0, 0, 0, 0, 0, 0, 6, 0, 10, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0],
         [0, 0, 0, 20, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0], [2, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 2, 3, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 2, 0, 0], [6, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 2, 4, 0, 0],
         [0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 3]],
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
