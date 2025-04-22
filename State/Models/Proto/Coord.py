
import Proto.snakes_pb2 as protocol


class Coord:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x: int):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y: int):
        self.__y = y

    def to_protobuf(self):
        msg = protocol.GameState.Coord()
        msg.x = self.__x
        msg.y = self.__y
        return msg

    @classmethod
    def from_protobuf(cls, msg: protocol.GameState.Coord):
        x = msg.x
        y = msg.y
        return cls(x, y)
