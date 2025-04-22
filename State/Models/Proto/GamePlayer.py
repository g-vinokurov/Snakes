
import Proto.snakes_pb2 as protocol

from State.Models.Proto.NodeRole import NodeRole
from State.Models.Proto.PlayerType import PlayerType


class GamePlayer:
    def __init__(self, name: str, id: int, score: int, role: NodeRole):
        self.__id = id
        
        self.name = name
        self.role = role
        self.score = score
        
        self.ip_address = None
        self.port = None
        self.type = PlayerType.HUMAN

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role: NodeRole):
        self.__role = role

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score: int):
        self.__score = score

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, ip_address: str | None):
        self.__ip_address = ip_address

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port: int | None):
        self.__port = port

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type: PlayerType):
        self.__type = type

    def is_master(self):
        return self.__role == NodeRole.MASTER

    def is_deputy(self):
        return self.__role == NodeRole.DEPUTY

    def is_viewer(self):
        return self.__role == NodeRole.VIEWER

    def is_normal(self):
        return self.__role == NodeRole.NORMAL

    def is_human(self):
        return self.__type == PlayerType.HUMAN

    def is_robot(self):
        return self.__type == PlayerType.ROBOT

    def to_protobuf(self):
        msg = protocol.GamePlayer()
        msg.name = self.name
        msg.id = self.id
        if self.ip_address is not None:
            msg.ip_address = self.ip_address
        if self.port is not None:
            msg.port = self.port
        msg.role = self.role.to_protobuf()
        msg.type = self.type.to_protobuf()
        msg.score = self.score
        return msg

    @classmethod
    def from_protobuf(cls, msg: protocol.GamePlayer):
        name = msg.name
        id = msg.id
        score = msg.score
        role = NodeRole.from_protobuf(msg.role)
        
        player = cls(name, id, score, role)
        player.type = PlayerType.from_protobuf(msg.type)
        if msg.HasField('ip_address'):
            player.ip_address = msg.ip_address
        if msg.HasField('port'):
            player.port = msg.port
        return player
