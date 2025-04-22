
import enum

import Proto.snakes_pb2 as protocol


class NodeRole(enum.Enum):
    NORMAL = 0
    MASTER = 1
    DEPUTY = 2
    VIEWER = 3

    def to_protobuf(self):
        if self == NodeRole.NORMAL:
            return protocol.NodeRole.NORMAL
        if self == NodeRole.MASTER:
            return protocol.NodeRole.MASTER
        if self == NodeRole.DEPUTY:
            return protocol.NodeRole.DEPUTY
        if self == NodeRole.VIEWER:
            return protocol.NodeRole.VIEWER
        return protocol.NodeRole.VIEWER

    @classmethod
    def from_protobuf(cls, msg: protocol.NodeRole):
        if msg == protocol.NodeRole.NORMAL:
            return NodeRole.NORMAL
        if msg == protocol.NodeRole.MASTER:
            return NodeRole.MASTER
        if msg == protocol.NodeRole.DEPUTY:
            return NodeRole.DEPUTY
        if msg == protocol.NodeRole.VIEWER:
            return NodeRole.VIEWER
        return NodeRole.VIEWER
