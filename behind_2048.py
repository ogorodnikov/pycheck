def move2048(state, move):
    print('State:')
    [print(row) for row in state]
    print()

    if move == 'left':
        lines = state
    elif move == 'up':
        lines = [line for line in zip(*state)]
    elif move == 'right':
        lines = [line[::-1] for line in state]
    elif move == 'down':
        lines = [line[::-1] for line in zip(*state)]

    print('Lines:')
    [print(line) for line in lines]

    return state


if __name__ == '__main__':

    assert move2048([[0, 2, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 2, 0, 0]], 'up') == [[0, 4, 0, 0],
                                              [0, 0, 0, 0],
                                              [0, 0, 0, 0],
                                              [0, 0, 0, 2]], "Start. Move Up!"

    # assert move2048([[4, 0, 0, 0],
    #                  [0, 4, 0, 0],
    #                  [0, 0, 0, 0],
    #                  [0, 0, 8, 8]], 'right') == [[0, 0, 0, 4],
    #                                              [0, 0, 0, 4],
    #                                              [0, 0, 0, 0],
    #                                              [0, 0, 2, 16]], "Simple right"
    # assert move2048([[2, 0, 2, 2],
    #                  [0, 4, 4, 4],
    #                  [8, 8, 8, 16],
    #                  [0, 0, 0, 0]], 'right') == [[0, 0, 2, 4],
    #                                              [0, 0, 4, 8],
    #                                              [0, 8, 16, 16],
    #                                              [0, 0, 0, 2]], "Three merging"
    # assert move2048([[256, 0, 256, 4],
    #                  [16, 8, 8, 0],
    #                  [32, 32, 32, 32],
    #                  [4, 4, 2, 2]], 'right') == [[0, 0, 512, 4],
    #                                              [0, 0, 16, 16],
    #                                              [0, 0, 64, 64],
    #                                              [0, 2, 8, 4]], "All right"
    # assert move2048([[4, 4, 0, 0],
    #                  [0, 4, 1024, 0],
    #                  [0, 256, 0, 256],
    #                  [0, 1024, 1024, 8]], 'down') == [['U', 'W', 'I', 'N'],
    #                                                   ['U', 'W', 'I', 'N'],
    #                                                   ['U', 'W', 'I', 'N'],
    #                                                   ['U', 'W', 'I', 'N']], "We are the champions!"
    # assert move2048([[2, 4, 8, 16],
    #                  [32, 64, 128, 256],
    #                  [512, 1024, 2, 4],
    #                  [8, 16, 32, 64]], 'left') == [['G', 'A', 'M', 'E'],
    #                                                ['O', 'V', 'E', 'R'],
    #                                                ['G', 'A', 'M', 'E'],
    #                                                ['O', 'V', 'E', 'R']], "Nobody moves!"