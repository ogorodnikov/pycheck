CORNER_KEYS = "north-west north-east south-west south-east"


class Building:
    def __init__(self, south, west, width_WE, width_NS, height=10):

        init_code = type(self).__init__.__code__

        parameters = init_code.co_varnames[1:init_code.co_argcount]

        filtered_locals = {key: value for key, value in locals().items() if key in parameters}

        self.values = filtered_locals.values()

        vars(self).update(filtered_locals)


    def corners(self):
        corners_coordinates = (self.south + self.width_NS, self.west), \
                              (self.south + self.width_NS, self.west + self.width_WE), \
                              (self.south, self.west), \
                              (self.south, self.west + self.width_WE)

        corners_dict = {key: value for key, value in zip(CORNER_KEYS.split(), corners_coordinates)}
        return corners_dict

    def area(self):
        return self.width_WE * self.width_NS

    def volume(self):
        return self.area() * self.height

    def __repr__(self):
        return f'Building({", ".join(map(str, self.values))})'


if __name__ == '__main__':
    def json_dict(d):
        return dict((k, list(v)) for k, v in d.items())


    b = Building(1, 2, 2, 3)
    b2 = Building(1, 2, 2, 3, 5)
    assert json_dict(b.corners()) == {'north-east': [4, 4], 'south-east': [1, 4],
                                      'south-west': [1, 2], 'north-west': [4, 2]}, "Corners"
    assert b.area() == 6, "Area"
    assert b.volume() == 60, "Volume"
    assert b2.volume() == 30, "Volume2"
    assert str(b) == "Building(1, 2, 2, 3, 10)", "String"
