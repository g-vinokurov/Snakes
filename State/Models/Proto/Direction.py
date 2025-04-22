
import enum

import Proto.snakes_pb2 as protocol


class Direction(enum.Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def to_protobuf(self):
        if self == Direction.UP:
            return protocol.Direction.UP
        if self == Direction.DOWN:
            return protocol.Direction.DOWN
        if self == Direction.LEFT:
            return protocol.Direction.LEFT
        if self == Direction.RIGHT:
            return protocol.Direction.RIGHT

    @classmethod
    def from_protobuf(cls, msg: protocol.Direction):
        if msg == protocol.Direction.UP:
            return Direction.UP
        if msg == protocol.Direction.DOWN:
            return Direction.DOWN
        if msg == protocol.Direction.LEFT:
            return Direction.LEFT
        if msg == protocol.Direction.RIGHT:
            return Direction.RIGHT
