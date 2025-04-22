
import enum

import Proto.snakes_pb2 as protocol


class PlayerType(enum.Enum):
    HUMAN = 0
    ROBOT = 1

    def to_protobuf(self):
        if self == PlayerType.HUMAN:
            return protocol.PlayerType.HUMAN
        if self == PlayerType.ROBOT:
            return protocol.PlayerType.ROBOT
        return protocol.PlayerType.HUMAN

    @classmethod
    def from_protobuf(cls, msg: protocol.PlayerType):
        if msg == protocol.PlayerType.HUMAN:
            return PlayerType.HUMAN
        if msg == protocol.PlayerType.ROBOT:
            return PlayerType.ROBOT
        return PlayerType.HUMAN
