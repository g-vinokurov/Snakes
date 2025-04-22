
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout

from Gui.Screen import Screen
from Gui.StartScreen import StartScreen
from Gui.MenuScreen import MenuScreen
from Gui.SetupGameScreen import SetupGameScreen
from Gui.ConnectingScreen import ConnectingScreen
from Gui.GameScreen import GameScreen


class ScreenManager(QWidget):
    __mapper = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__screens = {}
        self.initUI()

    def initUI(self):
        self.current_screen = Screen(self)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.current_screen)

        self.setLayout(self.layout)

    def currentScreen(self):
        return self.current_screen

    def loadScreen(self, tag: str, *args, **kwargs):
        self.__screens[tag] = self.__mapper.get(tag, Screen)(self, *args, **kwargs)

    def updateScreen(self, tag: str, *args, **kwargs):
        self.__screens.get(tag, Screen(self)).updateData(*args, **kwargs)

    def gotoScreen(self, tag: str, *args, **kwargs):
        if tag not in self.__screens:
            self.loadScreen(tag, *args, **kwargs)

        self.layout.removeWidget(self.current_screen)
        self.current_screen.hide()
        self.current_screen = self.__screens[tag]
        self.current_screen.show()
        self.layout.addWidget(self.current_screen)

    @classmethod
    def register(cls, tag: str, screen_cls: type[Screen]):
        if tag in cls.__mapper:
            return
        cls.__mapper[tag] = screen_cls


ScreenManager.register('start', StartScreen)
ScreenManager.register('menu', MenuScreen)
ScreenManager.register('setup-game', SetupGameScreen)
ScreenManager.register('connecting', ConnectingScreen)
ScreenManager.register('game', GameScreen)
