
from State.Models.GamesInfoListItem import GamesInfoListItem


class GamesInfoList:
    def __init__(self):
        self.__items = {}

    def __getitem__(self, key: str):
        return self.__items[key]

    def __setitem__(self, key: str, item: GamesInfoListItem):
        self.__items[key] = item

    @property
    def items(self):
        return list(self.__items.values())

    @property
    def names(self):
        return set(self.__items.keys())
