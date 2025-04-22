
import Proto.snakes_pb2 as protocol

from State.Models.Proto.GameConfig import GameConfig
from State.Models.Proto.GamePlayers import GamePlayers


class GameAnnouncement:
    def __init__(self, game_name: str, config: GameConfig, players: GamePlayers, can_join: bool = True):
        self.game_name = game_name
        self.config = config
        self.players = players
        self.can_join = can_join

    @property
    def game_name(self):
        return self.__game_name

    @game_name.setter
    def game_name(self, game_name: str):
        self.__game_name = game_name

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config: GameConfig):
        self.__config = config

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, players: GamePlayers):
        self.__players = players

    @property
    def can_join(self):
        return self.__can_join

    @can_join.setter
    def can_join(self, can_join: bool):
        self.__can_join = can_join

    def to_protobuf(self):
        msg = protocol.GameAnnouncement()
        msg.players.CopyFrom(self.__players.to_protobuf())
        msg.config.CopyFrom(self.__config.to_protobuf())
        msg.can_join = self.__can_join
        msg.game_name = self.__game_name
        return msg

    @classmethod
    def from_protobuf(cls, msg: protocol.GameMessage.AnnouncementMsg):
        if not msg.games:
            raise ValueError('There is no games')
        msg = msg.games[0]
        game_name = msg.game_name
        can_join = msg.can_join
        config = GameConfig.from_protobuf(msg.config)
        players = GamePlayers.from_protobuf(msg.players)
        return cls(game_name, config, players, can_join)
