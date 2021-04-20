from cmath import phase
from itertools import starmap
from math import pi, e

PRECISION = 100


def get_center(points):
    # return sum(points) / len(points)

    min_x, max_x, min_y, max_y = (operation(map(part, points))
                                  for part in (lambda c: c.real, lambda c: c.imag)
                                  for operation in (min, max))

    return complex(min_x + (max_x - min_x) / 2, min_y + (max_y - min_y) / 2)


def get_convex_hull_points(points, center):
    min_point_indices = []
    max_point_indices = []

    for segment_index in range(PRECISION):
        # print('Segment index:', segment_index)

        new_points = []

        for point in points:
            # print('    Point:', point)

            moved_point = point - center
            # print('        Moved point:', moved_point)

            rotated_point = moved_point * e ** (2j * pi * segment_index / PRECISION)
            # print('        Rotated point:', rotated_point)

            new_point = rotated_point + center
            # print('        New point:', new_point)

            new_points.append(new_point)

        # print('New points:', new_points)

        min_point = min(new_points, key=abs)
        # print('Min point:', min_point)

        max_point = max(new_points, key=abs)
        # print('Max point:', max_point)

        min_point_index = new_points.index(min_point)
        # print('Min point index:', min_point_index)

        max_point_index = new_points.index(max_point)
        # print('Max point index:', max_point_index)

        min_point_indices.append(min_point_index)
        max_point_indices.append(max_point_index)

    filtered_points = [point for index, point in enumerate(points) if index in min_point_indices]

    # print()
    # print('Min point indices:', min_point_indices)
    # print('Max point indices:', max_point_indices)
    # print('Filtered points:', filtered_points)

    return filtered_points


def checkio(data):
    # data = [[1, 2], [2, 1], [2, 3], [3, 2]]
    # data = [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9], [4, 4]]
    # data = [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9], [1, 7]]

    print('Data:', data)

    complex_points = list(starmap(complex, data))
    print('Complex points:', complex_points)

    center = get_center(complex_points)
    print('Center:', center)

    convex_hull_points = get_convex_hull_points(complex_points, center)
    print('Convex hull points:', convex_hull_points)
    print()

    # for point_index, point in enumerate(convex_hull_points):
    #     print('Point: ', point, point_index)
    #
    #     vector = point - center
    #     print('Vector:', vector)
    #
    #     angle = phase(vector)
    #     print('Angle: ', angle)
    #
    #     print()
    #
    # quit()


    starting_point = min(convex_hull_points, key=lambda c: (c.real, c.imag))
    starting_index = complex_points.index(starting_point)
    print('Starting point:', starting_point)
    print('Starting index:', starting_index)
    print()

    angles = [(-phase(point - center), point, complex_points.index(point))
              for point in convex_hull_points if point != starting_point]
    print('Angles:', angles)

    sorted_angles = sorted(angles)

    print()
    print('Sorted angles:')
    [print(record) for record in sorted_angles]

    output_indices = [starting_index] + [record[2] for record in sorted_angles]
    print('Output indices:', output_indices)
    print()

    return output_indices


if __name__ == '__main__':

    assert checkio(
        [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9]]
    ) == [4, 5, 6, 0, 1, 2, 3], "First example"

    assert checkio(
        [[3, 8], [1, 6], [6, 2], [7, 6], [5, 5], [8, 4], [6, 8]]
    ) == [1, 0, 6, 3, 5, 2], "Second example"

    assert checkio([[2, 6], [5, 5], [4, 4], [2, 2]]) == [3, 0, 1, 2]
