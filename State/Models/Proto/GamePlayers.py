
import secrets
import struct

import Proto.snakes_pb2 as protocol

from State.Models.Proto.GamePlayer import GamePlayer
from State.Models.Proto.NodeRole import NodeRole
from State.Models.Proto.PlayerType import PlayerType


class GamePlayers:
    def __init__(self, players: list[GamePlayer] = []):
        self.players = players

    def __getitem__(self, key: int, default = None):
        return self.__players.get(key, default)
    
    @property
    def players(self):
        return list(self.__players.values())

    @players.setter
    def players(self, players: list[GamePlayer]):
        self.__players = {}
        for player in players:
            self.__players[player.id] = player

    @property
    def master(self):
        for player in self.__players.values():
            if player.role == NodeRole.MASTER:
                return player
        return None

    @property
    def deputy(self):
        for player in self.__players.values():
            if player.role == NodeRole.DEPUTY:
                return player
        return None

    def get_normal(self, my_id: int):
        for player in self.__players.values():
            if player.role == NodeRole.NORMAL and player.id != my_id:
                return player
        return None

    def add(self, name: str, role: NodeRole, type: PlayerType = PlayerType.HUMAN):
        if role == NodeRole.MASTER and self.master is not None:
            raise ValueError('Master exists!')
        
        id = struct.unpack('!i', secrets.token_bytes(4))[0]
        while id in self.__players:
            id = struct.unpack('!i', secrets.token_bytes(4))[0]
        score = 0
        
        player = GamePlayer(name, id, score, role)
        player.type = type
        self.__players[player.id] = player
        return player.id

    def remove(self, player_id: int):
        if player_id not in self.__players:
            return
        self.__players.pop(player_id)

    def get_player_by_address(self, ip: str, port: int):
        for player in self.__players.values():
            if player.ip_address == ip and player.port == port:
                return player
        return None

    @property
    def alive_count(self):
        counter = 0
        for player in self.__players.values():
            if player.role != NodeRole.VIEWER:
                counter += 1
        return counter

    def to_protobuf(self):
        msg = protocol.GamePlayers()
        msg.players.extend([player.to_protobuf() for player in self.players])
        return msg

    @classmethod
    def from_protobuf(cls, msg: protocol.GamePlayers):
        players = [GamePlayer.from_protobuf(x) for x in msg.players]
        return cls(players)
