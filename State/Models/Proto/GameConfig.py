
import Proto.snakes_pb2 as protocol


class GameConfig:
    def __init__(self, width: int = 40, height: int = 30, food_static: int = 1, state_delay_ms: int = 1000):
        
        if width < 10 or width > 100:
            raise ValueError('Field width must be between 10 and 100')
        if height < 10 or height > 100:
            raise ValueError('Field height must be between 10 and 100')
        if food_static < 0 or food_static > 100:
            raise ValueError('Food static count must be between 0 and 100')
        if state_delay_ms < 100 or state_delay_ms > 3000:
            raise ValueError('State delay must be between 100 and 3000 ms')
        
        self.__width = width
        self.__height = height
        self.__food_static = food_static
        self.__state_delay_ms = state_delay_ms

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
    
    @property
    def food_static(self):
        return self.__food_static

    @property
    def state_delay_ms(self):
        return self.__state_delay_ms

    def to_protobuf(self):
        msg = protocol.GameConfig()
        msg.width = self.__width
        msg.height = self.__height
        msg.food_static = self.__food_static
        msg.state_delay_ms = self.__state_delay_ms
        return msg

    @classmethod
    def from_protobuf(cls, msg: protocol.GameConfig):
        width = msg.width
        height = msg.height
        food_static = msg.food_static
        state_delay_ms = msg.state_delay_ms
        return cls(width, height, food_static, state_delay_ms)
