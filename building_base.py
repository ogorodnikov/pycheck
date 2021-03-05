CORNER_KEYS = "north-west north-east south-west south-east"


class Building:
    def __init__(self, south, west, width_WE, width_NS, height=10):
        self.south = south
        self.west = west
        self.width_WE = width_WE
        self.width_NS = width_NS
        self.height = height


    def corners(self):
        raise NotImplementedError

    def area(self):
        raise NotImplementedError

    def volume(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError
#     "Building({south}, {west}, {width_we}, {width_ns}, {height})"


if __name__ == '__main__':

    def json_dict(d):
        return dict((k, list(v)) for k, v in d.items())

    b = Building(1, 2, 2, 3)
    # b2 = Building(1, 2, 2, 3, 5)
    # assert json_dict(b.corners()) == {'north-east': [4, 4], 'south-east': [1, 4],
    #                                   'south-west': [1, 2], 'north-west': [4, 2]}, "Corners"
    # assert b.area() == 6, "Area"
    # assert b.volume() == 60, "Volume"
    # assert b2.volume() == 30, "Volume2"
    # assert str(b) == "Building(1, 2, 2, 3, 10)", "String"