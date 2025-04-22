
import random

from State.Models.Proto.GameConfig import GameConfig
from State.Models.Proto.GameState import GameState
from State.Models.Proto.GamePlayers import GamePlayers
from State.Models.Proto.GamePlayer import GamePlayer
from State.Models.Proto.Coord import Coord
from State.Models.Proto.Snake import Snake
from State.Models.Proto.NodeRole import NodeRole
from State.Models.Proto.PlayerType import PlayerType
from State.Models.Proto.Direction import Direction
from State.Models.Proto.SnakeState import SnakeState

from State.Models.CellType import CellType

from Logger import log


class Game:
    def __init__(self, name: str, config: GameConfig, can_join: bool = True):
        self.__name = name
        self.__config = config
        self.__can_join = can_join
        self.__state = None
        self.__my_id = None
        self.__me = None

    @property
    def config(self):
        return self.__config

    @property
    def name(self):
        return self.__name

    @property
    def can_join(self):
        return self.__can_join

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: GameState | None):
        if self.state is not None:
            if state is None:
                return
            if state.state_order <= self.state.state_order:
                return
        self.__state = state

    @property
    def my_id(self):
        return self.__my_id

    @property
    def me(self):
        if self.__state is None:
            return self.__me
        if self.__my_id is None:
            return None
        print([x.id for x in self.__state.players.players])
        return self.__state.players[self.__my_id]

    @property
    def my_snake(self):
        if self.__my_id is None:
            return None
        if self.__state is None:
            return None
        return self.__state.get_snake(self.__my_id)

    @property
    def enemies(self):
        if self.__my_id is None:
            return None
        if self.__state is None:
            return None
        return self.__state.get_enemies(self.__my_id)

    def start(self, master_name: str):
        if self.state is not None:
            return
        
        players = GamePlayers()
        id = players.add(master_name, NodeRole.MASTER, PlayerType.HUMAN)

        head_x = self.config.width // 2
        head_y = self.config.height // 2
        tail_dx = -1  # offset: tail.x - head.x
        tail_dy = 0
        snake = Snake(id, [Coord(head_x, head_y), Coord(tail_dx, tail_dy)], Direction.RIGHT, SnakeState.ALIVE)
        
        self.__state = GameState(0, [snake], [], players)
        self.__my_id = id

        self.__place_food(self.build_field())

    def next(self):
        if self.me is None:
            return
        if not self.me.is_master():
            return
        if self.state is None:
            return

        field = self.build_field()
        for snake in self.state.snakes:
            snake.move(grow=True)
        self.__eat_food(field)
        self.__check_collisions(field)
        self.__place_food(field)

        self.state.state_order = self.state.state_order + 1
        log.debug(f'Next State: {self.state.state_order}')

    def join(self, player_ip: str, player_port: int, type: PlayerType, name: str, only_view: bool = False):
        if not self.can_join:
            return
        if only_view:
            role = NodeRole.VIEWER
        else:
            role = NodeRole.NORMAL
                
        if role != NodeRole.VIEWER:
            head, direction = self.__data_for_join()
            if head is None or direction is None:
                return
            head = Coord(*head)

        player_id = self.state.players.add(name, role, type)
        self.state.players[player_id].ip_address = player_ip
        self.state.players[player_id].port = player_port
        
        if role != NodeRole.VIEWER:
            if direction == Direction.UP:
                tail_dx = 0
                tail_dy = 1
            if direction == Direction.DOWN:
                tail_dx = 0
                tail_dy = -1
            if direction == Direction.LEFT:
                tail_dx = 1
                tail_dy = 0
            if direction == Direction.RIGHT:
                tail_dx = -1
                tail_dy = 0
            snake = Snake(player_id, [head, Coord(tail_dx, tail_dy)], direction, SnakeState.ALIVE)
            self.state.add_snake(snake)
        
        log.debug(f'Game.join: player_id: {player_id}')
        return player_id

    def setup(self, id: int, name: str, type: PlayerType, role: NodeRole):
        log.debug(f'Game.setup: id: {id}')
        self.__my_id = id
        self.__me = GamePlayer(name, id, 0, role)

    def build_field(self):
        rows = self.config.height
        cols = self.config.width

        cells = [[CellType.FREE for i in range(cols)] for j in range(rows)]

        for food_pos in self.state.foods:
            coord_x = food_pos.x % cols
            coord_y = food_pos.y % rows
            cells[coord_y][coord_x] = CellType.FOOD

        if self.my_snake is not None:
            for coord in self.my_snake.coordinates:
                coord_x = coord.x % cols
                coord_y = coord.y % rows
                cells[coord_y][coord_x] = CellType.ME

        for enemy in self.enemies:
            for coord in enemy.coordinates:
                coord_x = coord.x % cols
                coord_y = coord.y % rows
                if enemy.is_alive:
                    cells[coord_y][coord_x] = CellType.ENEMY
                else:
                    cells[coord_y][coord_x] = CellType.ZOMBIE
        return cells

    def get_cell(self, field: list[list[CellType]], x: int, y: int):
        x = x % len(field[0])
        y = y % len(field)
        return x, y

    def cell_is_free(self, field: list[list[CellType]], x: int, y: int):
        x = x % len(field[0])
        y = y % len(field)
        return field[y][x] == CellType.FREE

    def cell_is_food(self, field: list[list[CellType]], x: int, y: int):
        x = x % len(field[0])
        y = y % len(field)
        return field[y][x] == CellType.FOOD

    def set_cell(self, field: list[list[CellType]], x: int, y: int, value: CellType):
        x = x % len(field[0])
        y = y % len(field)
        field[y][x] = value
        return field

    def get_free_cells(self, field: list[list[CellType]]):
        free_cells = []
        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j] != CellType.FREE:
                    continue
                free_cells.append(Coord(j, i))
        return free_cells

    def __eat_food(self, field: list[list[CellType]]):
        for snake in self.state.snakes:
            x, y = self.get_cell(field, snake.head.x, snake.head.y)
            
            if not self.cell_is_food(field, x, y):
                snake.untail()
                continue
            if snake.is_zombie:
                continue
            player = self.state.players[snake.player_id]
            player.score = player.score + 1
            self.state.eat_food(x, y)

    def __check_collisions(self, field: list[list[CellType]]):
        killed_snakes = []
        
        for s1 in self.state.snakes:
            s1_head = self.get_cell(field, s1.head.x, s1.head.y)
            for s2 in self.state.snakes:
                coords = [self.get_cell(field, c.x, c.y) for c in s2.coordinates]
                if s1 == s2:
                    if len(coords) != len(set(coords)):
                        killed_snakes.append(s1)
                    else:
                        continue
                else:
                    if s1_head in coords:
                        killed_snakes.append(s1)
                        if s2.is_zombie:
                            continue
                        player = self.state.players[s2.player_id]
                        player.score = player.score + 1
                    else:
                        continue
        for snake in killed_snakes:
            self.__destroy_snake(field, snake)

    def __destroy_snake(self, field: list[list[CellType]], snake: Snake):
        self.state.remove_snake(snake)
        
        coords = [self.get_cell(field, c.x, c.y) for c in snake.coordinates]
        foods = set(self.get_cell(field, f.x, f.y) for f in self.state.foods)
        
        for coord in coords:
            if random.randint(0, 1):
                foods.add(coord)
            else:
                continue
        self.state.foods = list(Coord(*f) for f in foods)

    def __place_food(self, field: list[list[CellType]]):
        free_cells = self.get_free_cells(field)
        
        foods = self.state.foods
        food_static = self.config.food_static
        alive_count = self.state.players.alive_count
        
        target_food_count = food_static + alive_count
        if len(free_cells) < target_food_count - len(foods):
            new_food_count = len(free_cells)
        else:
            new_food_count = target_food_count - len(foods)

        if new_food_count <= 0:
            return

        new_food_cells = random.sample(free_cells, k=new_food_count)
        
        self.state.foods = foods + new_food_cells
        return

    def __data_for_join(self):
        head = None
        direction = None

        field = self.build_field()

        for i in range(len(field)):
            for j in range(len(field[0])):
                if not self.__available_square_5x5(field, i, j):
                    continue
                return self.__place_snake_in_square_5x5(field, i, j)
        return head, direction

    def __available_square_5x5(self, field: list[list[CellType]], i: int, j: int):
        for ik in range(i, i + 5):
            for jk in range(j, j + 5):
                if self.cell_is_free(field, jk, ik) or self.cell_is_food(field, jk, ik):
                    continue
                return False
        return True

    def __place_snake_in_square_5x5(self, field: list[list[CellType]], i: int, j: int):
        head = random.randint(i + 1, i + 3), random.randint(j + 1, j + 3)
        direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
        return head, direction
