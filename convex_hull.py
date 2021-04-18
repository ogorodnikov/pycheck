from operator import itemgetter


def checkio(data):

    print('Data:', data)

    initial_a = min(data)
    print('Initial a:', initial_a)

    checked = []

    min_x = min(map(itemgetter(0), data))
    min_y = min(map(itemgetter(1), data))

    min_x, min_y, max_x, max_y = (operation(map(itemgetter(coordinate), data))
                                  for operation in (min, max)
                                  for coordinate in (0, 1))

    print('Min x:', min_x)
    print('Min y:', min_y)
    print('Max x:', max_x)
    print('Max y:', max_y)



    quit()

    return [0, 1, 2]


if __name__ == '__main__':

    assert checkio(
        [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9]]
    ) == [4, 5, 6, 0, 1, 2, 3], "First example"

    # assert checkio(
    #     [[3, 8], [1, 6], [6, 2], [7, 6], [5, 5], [8, 4], [6, 8]]
    # ) == [1, 0, 6, 3, 5, 2], "Second example"
