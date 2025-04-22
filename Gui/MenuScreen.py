
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt

from State.Models.Proto.NodeRole import NodeRole

from Gui.Screen import Screen

from Gui.Colors import COLOR_WHITE, COLOR_BLACK, COLOR_RED
from Gui.Fonts import FONT_USSR_STENCIL

from Logger import log

from App import app


class GamesListHeaderLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 32px;
            padding-right: 32px;
            padding-top: 8px;
            padding-bottom: 8px;
            color: {COLOR_WHITE};
        ''')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 17))


class GamesListItemLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 32px;
            padding-right: 32px;
            padding-top: 8px;
            padding-bottom: 8px;
            color: {COLOR_WHITE};
        ''')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 16))


class GamesListItemPlayButton(QPushButton):
    def __init__(self, game_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__game_name = game_name
        self.initUI()

    def initUI(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f'''
            QPushButton {{
                background: none;
                padding-left: 0px;
                padding-right: 0px;
                padding-top: 0px;
                padding-bottom: 0px;
                border: none;
                outline: none;
                color: {COLOR_RED};
            }}

            QPushButton:hover {{
                color: {COLOR_RED};
            }}
        ''')
        self.setFont(QFont(str(FONT_USSR_STENCIL), 16))
        self.clicked.connect(self.on_clicked)

    def enterEvent(self, event):
        super().enterEvent(event)
        font = QFont(str(FONT_USSR_STENCIL), 16)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        self.setFont(font)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        font = QFont(str(FONT_USSR_STENCIL), 16)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0)
        self.setFont(font)

    def on_clicked(self):
        log.info(f'Play: {self.__game_name}')
        game_info = app.state.games_info_list[self.__game_name]
        master_ip = game_info.master_ip
        master_port = game_info.master_port
        game_name = self.__game_name
        role = NodeRole.NORMAL
        app.node.join_game(master_ip, master_port, game_name, role)


class GamesListItemViewButton(QPushButton):
    def __init__(self, game_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__game_name = game_name
        self.initUI()

    def initUI(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f'''
            QPushButton {{
                background: none;
                padding-left: 0px;
                padding-right: 0px;
                padding-top: 0px;
                padding-bottom: 0px;
                border: none;
                outline: none;
                color: {COLOR_WHITE};
            }}

            QPushButton:hover {{
                color: {COLOR_WHITE};
            }}
        ''')
        self.setFont(QFont(str(FONT_USSR_STENCIL), 16))
        self.clicked.connect(self.on_clicked)

    def enterEvent(self, event):
        super().enterEvent(event)
        font = QFont(str(FONT_USSR_STENCIL), 16)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        self.setFont(font)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        font = QFont(str(FONT_USSR_STENCIL), 16)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0)
        self.setFont(font)

    def on_clicked(self):
        log.info(f'View: {self.__game_name}')
        game_info = app.state.games_info_list[self.__game_name]
        master_ip = game_info.master_ip
        master_port = game_info.master_port
        game_name = self.__game_name
        role = NodeRole.VIEWER
        app.node.join_game(master_ip, master_port, game_name, role)


class NoGamesLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 64px;
            padding-right: 64px;
            padding-top: 16px;
            padding-bottom: 16px;
            color: {COLOR_WHITE};
        ''')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 24))


class UserNameLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 64px;
            padding-right: 64px;
            padding-top: 16px;
            padding-bottom: 16px;
            color: {COLOR_WHITE};
        ''')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 18))


class StartNewGameButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f'''
            QPushButton {{
                background: none;
                padding-left: 16px;
                padding-right: 16px;
                padding-top: 4px;
                padding-bottom: 4px;
                border: none;
                outline: none;
                color: {COLOR_WHITE};
            }}

            QPushButton:hover {{
                color: {COLOR_WHITE};
            }}
        ''')
        self.setFont(QFont(str(FONT_USSR_STENCIL), 24))

    def enterEvent(self, event):
        super().enterEvent(event)
        font = QFont(str(FONT_USSR_STENCIL), 24)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        self.setFont(font)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        font = QFont(str(FONT_USSR_STENCIL), 24)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0)
        self.setFont(font)


class Games(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.label_list_header_game = GamesListHeaderLabel(self)
        self.label_list_header_master = GamesListHeaderLabel(self)
        self.label_list_header_field = GamesListHeaderLabel(self)
        self.label_list_header_food = GamesListHeaderLabel(self)
        self.label_list_header_play_or_view = GamesListHeaderLabel(self)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.label_list_header_game, 0, 0)
        self.layout.addWidget(self.label_list_header_master, 0, 1)
        self.layout.addWidget(self.label_list_header_field, 0, 2)
        self.layout.addWidget(self.label_list_header_food, 0, 3)
        self.layout.addWidget(self.label_list_header_play_or_view, 0, 4)

        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):           
        self.label_list_header_game.setText('Game')
        self.label_list_header_master.setText('Master [IP]')
        self.label_list_header_field.setText('Field')
        self.label_list_header_food.setText('Food')
        self.label_list_header_play_or_view.setText('Play Or View')

        for i in range(1, self.layout.rowCount()):
            for j in range(self.layout.columnCount()):
                widget = self.layout.itemAtPosition(i, j).widget()
                self.layout.removeWidget(widget)
                widget.setParent(None)
                widget.hide()
        
        for i, item in enumerate(app.state.games_info_list.items, 1):
            item_0 = GamesListItemLabel(f'{item.game_name}', self)
            item_1 = GamesListItemLabel(f'{item.master_name} [{item.master_ip}]', self)
            item_2 = GamesListItemLabel(f'{item.field_width} x {item.field_height}', self)
            item_3 = GamesListItemLabel(f'{item.food_static} + {item.alive_snakes_count}x', self)

            btn_play = GamesListItemPlayButton(item.game_name, self)
            btn_play.setText('Play!')

            btn_view = GamesListItemViewButton(item.game_name, self)
            btn_view.setText('View')

            layout = QHBoxLayout()
            layout.setContentsMargins(16, 4, 16, 4)
            layout.setSpacing(16)

            layout.addWidget(btn_view)
            layout.addWidget(btn_play)

            item_4 = QWidget(self)
            item_4.setLayout(layout)
            
            self.layout.addWidget(item_0, i, 0)
            self.layout.addWidget(item_1, i, 1)
            self.layout.addWidget(item_2, i, 2)
            self.layout.addWidget(item_3, i, 3)
            self.layout.addWidget(item_4, i, 4)


class NoGames(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.label_no_games = NoGamesLabel(self)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label_no_games)

        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.label_no_games.setText('No Active Games')


class Header(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.label_user_name = UserNameLabel(self)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(self.label_user_name)

        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.label_user_name.setText(f'You: {app.state.user.name}')


class Body(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.games = Games(self)
        self.no_games = NoGames(self)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.games)
        self.layout.addWidget(self.no_games)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        if not app.state.games_info_list.items:
            self.games.hide()
            self.no_games.show()
        else:
            self.games.show()
            self.no_games.hide()
        self.games.updateData(*args, **kwargs)
        self.no_games.updateData(*args, **kwargs)


class Footer(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.btn_start_new_game = StartNewGameButton(self)
        self.btn_start_new_game.clicked.connect(self.on_btn_start_new_game_clicked)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(128, 32, 128, 32)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.btn_start_new_game)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.btn_start_new_game.setText('Start New Game')

    def on_btn_start_new_game_clicked(self):
        app.gui.screen_manager.gotoScreen('setup-game')


class MenuScreen(Screen):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'''background-color: {COLOR_BLACK};''')

        self.header = Header(self)
        self.body = Body(self)
        self.footer = Footer(self)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.body)
        self.layout.addWidget(self.footer)

        self.layout.setStretch(1, 1)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.header.updateData(*args, **kwargs)
        self.body.updateData(*args, **kwargs)
        self.footer.updateData(*args, **kwargs)
