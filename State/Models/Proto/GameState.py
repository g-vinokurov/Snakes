
import Proto.snakes_pb2 as protocol

from State.Models.Proto.Coord import Coord
from State.Models.Proto.Snake import Snake
from State.Models.Proto.GamePlayers import GamePlayers


class GameState:
    def __init__(self, state_order: int, snakes: list[Snake], foods: list[Coord], players: GamePlayers):
        self.state_order = state_order
        self.snakes = snakes
        self.foods = foods
        self.players = players

    @property
    def state_order(self):
        return self.__state_order

    @state_order.setter
    def state_order(self, state_order: int):
        self.__state_order = state_order

    @property
    def snakes(self):
        return self.__snakes[::]

    @snakes.setter
    def snakes(self, snakes: list[Snake]):
        self.__snakes = snakes[::]

    @property
    def foods(self):
        return self.__foods[::]

    @foods.setter
    def foods(self, foods: list[Coord]):
        self.__foods = foods[::]

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, players: GamePlayers):
        self.__players = players

    def eat_food(self, x: int, y: int):
        foods = []
        for food in self.__foods:
            if food.x != x or food.y != y:
                foods.append(food)
        self.foods = foods
    
    def get_snake(self, player_id: int):
        for snake in self.__snakes:
            if snake.player_id == player_id:
                return snake
        return None

    def add_snake(self, snake: Snake):
        self.__snakes.append(snake)

    def remove_snake(self, snake: Snake):
        if snake not in self.__snakes:
            return
        self.__snakes.remove(snake)

    def get_enemies(self, player_id: int):
        enemies = []
        for snake in self.__snakes:
            if snake.player_id == player_id:
                continue
            enemies.append(snake)
        return enemies

    def to_protobuf(self):
        msg = protocol.GameState()
        msg.state_order = self.__state_order
        msg.snakes.extend([snake.to_protobuf() for snake in self.__snakes])
        msg.foods.extend([food.to_protobuf() for food in self.__foods])
        msg.players.CopyFrom(self.__players.to_protobuf())
        return msg

    @classmethod
    def from_protobuf(cls, msg: protocol.GameState):
        state_order = msg.state_order
        snakes = [Snake.from_protobuf(x) for x in msg.snakes]
        foods = [Coord.from_protobuf(x) for x in msg.foods]
        players = GamePlayers.from_protobuf(msg.players)
        return cls(state_order, snakes, foods, players)
        
