
import secrets

from State.Models.Proto.GameConfig import GameConfig
from State.Models.Proto.PlayerType import PlayerType
from State.Models.Proto.NodeRole import NodeRole

from State.Models.User import User
from State.Models.GamesInfoList import GamesInfoList
from State.Models.Game import Game


class State:
    def __init__(self):
        self.user = User()
        self.games_info_list = GamesInfoList()
        self.game_config = GameConfig()
        
        self.__game = None

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user: User):
        self.__user = user

    @property
    def games_info_list(self):
        return self.__games_info_list

    @games_info_list.setter
    def games_info_list(self, games_info_list: GamesInfoList):
        self.__games_info_list = games_info_list

    @property
    def game_config(self):
        return self.__game_config

    @game_config.setter
    def game_config(self, game_config: GameConfig):
        self.__game_config = game_config

    @property
    def game(self):
        return self.__game

    def start_game(self):
        if self.__game is not None:
            raise RuntimeError('Impossible to start game: you have active game!')
        
        name = secrets.token_hex(4)
        while name in self.games_info_list.names:
            name = secrets.token_hex(4)
        
        self.__game = Game(name, self.game_config, can_join=True)
        self.__game.start(self.user.name)
        
    def join_game(self, game_name: str, player_ip: str, player_port: int, type: PlayerType, name: str, role: NodeRole):
        if self.__game is None:
            return
        if self.__game.name != game_name:
            return
        if role != NodeRole.VIEWER and role != NodeRole.NORMAL:
            return
        if role == NodeRole.VIEWER:
            return self.__game.join(player_ip, player_port, type, name, only_view=True)
        return self.__game.join(player_ip, player_port, type, name, only_view=False)

    def setup_game(self, game_name: str, id: int, name: str, type: PlayerType, role: NodeRole):
        if self.__game is not None:
            raise RuntimeError('Impossible to start game: you have active game!')
        
        if role != NodeRole.VIEWER and role != NodeRole.NORMAL:
            return

        try:
            game = self.__games_info_list[game_name]
        except Exception:
            return

        width = game.field_width
        height = game.field_height
        food_static = game.food_static
        state_delay_ms = game.state_delay_ms

        game_config = GameConfig(width, height, food_static, state_delay_ms)
        
        self.__game = Game(game.game_name, game_config, can_join=game.can_join)
        self.__game.setup(id, name, type, role)

    def quit_game(self):
        self.__game = None
