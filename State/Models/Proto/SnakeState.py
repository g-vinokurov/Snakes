
import enum

import Proto.snakes_pb2 as protocol


class SnakeState(enum.Enum):
    ALIVE = 0
    ZOMBIE = 1

    def to_protobuf(self):
        if self == SnakeState.ALIVE:
            return protocol.GameState.Snake.SnakeState.ALIVE
        if self == SnakeState.ZOMBIE:
            return protocol.GameState.Snake.SnakeState.ZOMBIE

    @classmethod
    def from_protobuf(cls, msg: protocol.GameState.Snake.SnakeState):
        if msg == protocol.GameState.Snake.SnakeState.ALIVE:
            return SnakeState.ALIVE
        if msg == protocol.GameState.Snake.SnakeState.ZOMBIE:
            return SnakeState.ZOMBIE
