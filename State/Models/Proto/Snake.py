
import Proto.snakes_pb2 as protocol

from State.Models.Proto.Coord import Coord
from State.Models.Proto.SnakeState import SnakeState
from State.Models.Proto.Direction import Direction

from Logger import log


class Snake:
    def __init__(self, player_id: int, points: list[Coord], head_direction: Direction, state: SnakeState):
        self.player_id = player_id
        self.points = points
        
        self.state = SnakeState.ALIVE
        self.head_direction = head_direction
        self.state = state

    @property
    def player_id(self):
        return self.__player_id

    @player_id.setter
    def player_id(self, player_id: int):
        self.__player_id = player_id

    @property
    def points(self):
        return self.__points[::]

    @property
    def coordinates(self):
        coordinates = [Coord(self.head.x, self.head.y)]

        prev_x = self.head.x
        prev_y = self.head.y
        for i in range(1, len(self.__points)):
            curr_dx = self.__points[i].x
            curr_dy = self.__points[i].y
            curr_x = prev_x + curr_dx
            curr_y = prev_y + curr_dy
            
            coordinates.append(Coord(curr_x, curr_y))
            
            prev_x = curr_x
            prev_y = curr_y
        return coordinates

    @points.setter
    def points(self, points: list[Coord]):
        if len(points) < 2:
            raise ValueError('Snake length must be no less than 2')
        for point in points[1:]:
            if abs(point.x) > 1 and abs(point.y) > 1:
                raise ValueError('Snake must contain head position and offsets between next point and current')
        self.__points = points[::]

    @property
    def head_direction(self):
        return self.__head_direction

    @head_direction.setter
    def head_direction(self, head_direction: Direction):
        if not self.is_alive:
            return
        
        if self.__direction_is_backward(head_direction):
            log.debug('Direction is backward')
            return
        
        self.__head_direction = head_direction

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: SnakeState):
        self.__state = state

    @property
    def head(self):
        return self.__points[0]

    @property
    def is_alive(self):
        return self.state == SnakeState.ALIVE

    @property
    def is_zombie(self):
        return self.state == SnakeState.ZOMBIE

    def zombify(self):
        self.state = SnakeState.ZOMBIE

    def up(self):
        self.head_direction = Direction.UP

    def down(self):
        self.head_direction = Direction.DOWN

    def left(self):
        self.head_direction = Direction.LEFT

    def right(self):
        self.head_direction = Direction.RIGHT

    def move(self, grow: bool = False):       
        curr_head_pos = self.head
        next_head_pos = self.__get_next_head_position(self.__head_direction)

        neck_dx = curr_head_pos.x - next_head_pos.x
        neck_dy = curr_head_pos.y - next_head_pos.y
        neck = Coord(neck_dx, neck_dy)
        
        self.__points.insert(0, next_head_pos)
        self.__points[1] = neck
        if not grow:
            self.__points.pop()

    def untail(self):
        self.__points.pop()

    def to_protobuf(self):
        msg = protocol.GameState.Snake()
        msg.player_id = self.__player_id
        msg.points.extend([point.to_protobuf() for point in self.__points])
        msg.state = self.__state.to_protobuf()
        msg.head_direction = self.__head_direction.to_protobuf()
        return msg

    @classmethod
    def from_protobuf(cls, msg: protocol.GameState.Snake):
        player_id = msg.player_id
        points = [Coord.from_protobuf(x) for x in msg.points]
        state = SnakeState.from_protobuf(msg.state)
        head_direction = Direction.from_protobuf(msg.head_direction)
        return cls(player_id, points, head_direction, state)

    def __get_neck_position(self):
        neck_x = self.head.x + self.__points[1].x
        neck_y = self.head.y + self.__points[1].y
        return Coord(neck_x, neck_y)

    def __get_next_head_position(self, direction: Direction):
        x, y = self.head.x, self.head.y
        if direction == Direction.UP:
            return Coord(x, y - 1)
        if direction == Direction.DOWN:
            return Coord(x, y + 1)
        if direction == Direction.LEFT:
            return Coord(x - 1, y)
        if direction == Direction.RIGHT:
            return Coord(x + 1, y)
        raise ValueError('Unexpected direction')

    def __direction_is_backward(self, direction: Direction):
        neck = self.__get_neck_position()
        head = self.__get_next_head_position(direction)
        return neck.x == head.x and neck.y == head.y
