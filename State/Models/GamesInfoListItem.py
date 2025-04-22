
class GamesInfoListItem:
    def __init__(self, game_name: str, master_name: str, master_ip: str, master_port: int, field_width: int, field_height: int, food_static: int, alive_snakes_count: int, can_join: bool, state_delay_ms: int):
        self.__game_name = game_name
        self.__master_name = master_name
        self.__master_ip = master_ip
        self.__master_port = master_port
        self.__field_width = field_width
        self.__field_height = field_height
        self.__food_static = food_static
        self.__alive_snakes_count = alive_snakes_count
        self.__can_join = can_join
        self.__state_delay_ms = state_delay_ms

    @property
    def game_name(self):
        return self.__game_name

    @property
    def master_name(self):
        return self.__master_name

    @property
    def master_ip(self):
        return self.__master_ip

    @property
    def master_port(self):
        return self.__master_port

    @property
    def field_width(self):
        return self.__field_width

    @property
    def field_height(self):
        return self.__field_height

    @property
    def food_static(self):
        return self.__food_static

    @property
    def alive_snakes_count(self):
        return self.__alive_snakes_count

    @property
    def can_join(self):
        return self.__can_join

    @property
    def state_delay_ms(self):
        return self.__state_delay_ms
