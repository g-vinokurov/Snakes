
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt

from State.Models.CellType import CellType
from State.Models.Proto.Direction import Direction

from Gui.Screen import Screen

from Gui.Colors import COLOR_WHITE, COLOR_BLACK, COLOR_RED, COLOR_YELLOW, COLOR_DARK, COLOR_SUCCESS
from Gui.Fonts import FONT_USSR_STENCIL

from Logger import log

from App import app


class FreeCell(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 0px;
            padding-right: 0px;
            padding-top: 0px;
            padding-bottom: 0px;
            border: 1px solid {COLOR_WHITE};
            background-color: {COLOR_DARK};
        ''')


class FoodCell(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 0px;
            padding-right: 0px;
            padding-top: 0px;
            padding-bottom: 0px;
            border: 1px solid {COLOR_WHITE};
            background-color: {COLOR_YELLOW};
        ''')


class MeCell(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 0px;
            padding-right: 0px;
            padding-top: 0px;
            padding-bottom: 0px;
            border: 1px solid {COLOR_WHITE};
            background-color: {COLOR_WHITE};
        ''')


class EnemyCell(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 0px;
            padding-right: 0px;
            padding-top: 0px;
            padding-bottom: 0px;
            border: 1px solid {COLOR_WHITE};
            background-color: {COLOR_RED};
        ''')


class ZombieCell(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 0px;
            padding-right: 0px;
            padding-top: 0px;
            padding-bottom: 0px;
            border: 1px solid {COLOR_WHITE};
            background-color: {COLOR_SUCCESS};
        ''')


class HeaderLabel(QLabel):
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


class MessageLabel(QLabel):
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
        self.setAlignment(Qt.AlignLeft)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 16))


class ScoreboardLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 64px;
            padding-right: 64px;
            padding-top: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid {COLOR_WHITE};
            color: {COLOR_WHITE};
        ''')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 20))


class ScoreboardHeaderLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 16px;
            padding-right: 16px;
            padding-top: 4px;
            padding-bottom: 4px;
            color: {COLOR_YELLOW};
        ''')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 16))


class ScoreboardItemLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 16px;
            padding-right: 16px;
            padding-top: 4px;
            padding-bottom: 4px;
            color: {COLOR_WHITE};
        ''')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 15))


class LeaveGameButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f'''
            QPushButton {{
                background: none;
                padding-left: 32px;
                padding-right: 32px;
                padding-top: 4px;
                padding-bottom: 4px;
                border: none;
                outline: none;
                color: {COLOR_RED};
            }}

            QPushButton:hover {{
                color: {COLOR_RED};
            }}
        ''')
        self.setFont(QFont(str(FONT_USSR_STENCIL), 18))
    
    def enterEvent(self, event):
        super().enterEvent(event)
        font = QFont(str(FONT_USSR_STENCIL), 18)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        self.setFont(font)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        font = QFont(str(FONT_USSR_STENCIL), 18)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0)
        self.setFont(font)


class Scoreboard(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'''border-bottom: 1px solid {COLOR_WHITE}''')

        self.label_scoreboard = ScoreboardLabel(self)

        self.label_position = ScoreboardHeaderLabel(self)
        self.label_player = ScoreboardHeaderLabel(self)
        self.label_score = ScoreboardHeaderLabel(self)
        
        self.content_layout = QGridLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_layout.setAlignment(Qt.AlignTop)

        self.content_layout.addWidget(self.label_position, 0, 0)
        self.content_layout.addWidget(self.label_player, 0, 1)
        self.content_layout.addWidget(self.label_score, 0, 2)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.label_scoreboard)
        self.layout.addLayout(self.content_layout)

        self.layout.setStretch(1, 1)

        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.label_scoreboard.setText('Scoreboard')
        self.label_position.setText('#')
        self.label_player.setText('Player')
        self.label_score.setText('Score')

        print(self.content_layout.rowCount())
        print(self.content_layout.columnCount())
        
        for i in range(1, self.content_layout.rowCount()):
            for j in range(self.content_layout.columnCount()):
                item = self.content_layout.itemAtPosition(i, j)
                if item is None:
                    continue
                widget = item.widget()
                self.content_layout.removeWidget(widget)
                widget.setParent(None)
                widget.hide()

        players = sorted(app.state.game.state.players.players, key=lambda x: x.score, reverse=True)
        players = list(filter(lambda x: not x.is_viewer(), players))

        for i, item in enumerate(players, 1):
            item_0 = ScoreboardItemLabel(f'{i}', self)
            item_1 = ScoreboardItemLabel(f'{item.name}', self)
            item_2 = ScoreboardItemLabel(f'{item.score}', self)
            
            self.content_layout.addWidget(item_0, i, 0)
            self.content_layout.addWidget(item_1, i, 1)
            self.content_layout.addWidget(item_2, i, 2)


class FieldWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.__field = []
        self.__cell_size = 25
        self.initUI()

    def initUI(self):
        self.layout = None
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.__field = app.state.game.build_field()
        width = self.__cell_size * len(self.__field[0])
        height = self.__cell_size * len(self.__field)

        if self.layout is None:

            self.layout = QGridLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)
            self.layout.setAlignment(Qt.AlignCenter)

            self.setLayout(self.layout)
        else:
            for i in range(self.layout.rowCount()):
                for j in range(self.layout.columnCount()):
                    item = self.layout.itemAtPosition(i, j)
                    if item is None:
                        continue
                    widget = item.widget()
                    self.layout.removeWidget(widget)
                    widget.setParent(None)
                    widget.hide()

        for i, row in enumerate(self.__field):
            for j, cell in enumerate(self.__field[i]):
                if cell == CellType.FREE:
                    item = FreeCell(self)
                if cell == CellType.FOOD:
                    item = FoodCell(self)
                if cell == CellType.ME:
                    item = MeCell(self)
                if cell == CellType.ENEMY:
                    item = EnemyCell(self)
                if cell == CellType.ZOMBIE:
                    item = ZombieCell(self)
                item.setFixedSize(self.__cell_size, self.__cell_size)
                self.layout.addWidget(item, i, j)


class GameSection(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.field = FieldWidget(self)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.field)

        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.field.updateData(*args, **kwargs)


class ScoreboardSection(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'''border-left: 1px solid {COLOR_WHITE}''')

        self.scoreboard = Scoreboard(self)

        self.btn_leave_game = LeaveGameButton(self)
        self.btn_leave_game.clicked.connect(self.on_btn_leave_game_clicked)
        
        self.actions_layout = QHBoxLayout()
        self.actions_layout.setContentsMargins(16, 0, 16, 0)
        self.actions_layout.setSpacing(0)
        
        self.actions_layout.addWidget(self.btn_leave_game)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.scoreboard)
        self.layout.addLayout(self.actions_layout)

        self.layout.setStretch(0, 1)

        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.scoreboard.updateData(*args, **kwargs)
        self.btn_leave_game.setText('Leave Game')

    def on_btn_leave_game_clicked(self):
        app.node.leave_game()


class Header(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'''border-bottom: 1px solid {COLOR_WHITE}''')

        self.label_current_game = HeaderLabel(self)
        self.label_master = HeaderLabel(self)
        self.label_size = HeaderLabel(self)
        self.label_food = HeaderLabel(self)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(32, 0, 32, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(self.label_current_game)
        self.layout.addWidget(self.label_master)
        self.layout.addWidget(self.label_size)
        self.layout.addWidget(self.label_food)

        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        
        game_name = app.state.game.name
        master_name = app.state.game.state.players.master.name
        field_width = app.state.game.config.width
        field_height = app.state.game.config.height
        food_static = app.state.game.config.food_static
        alive_snakes_count = app.state.game.state.players.alive_count
        
        self.label_current_game.setText(f'Current Game: {game_name}')
        self.label_master.setText(f'Master: {master_name}')
        self.label_size.setText(f'Size: {field_width} x {field_height}')
        self.label_food.setText(f'Food: {food_static} + {alive_snakes_count}x')


class Body(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.game_section = GameSection(self)
        self.scoreboard_section = ScoreboardSection(self)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.game_section)
        self.layout.addWidget(self.scoreboard_section)

        self.layout.setStretch(0, 1)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.game_section.updateData(*args, **kwargs)
        self.scoreboard_section.updateData(*args, **kwargs)


class Footer(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'''border-top: 1px solid {COLOR_WHITE}''')

        self.message = MessageLabel(self)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(self.message)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        if app.state.game is None:
            return
        
        me = app.state.game.me
        if me is None:
            return

        if me.is_viewer():
            self.message.setText(f'MODE: VIEWER')
        if me.is_normal():
            self.message.setText(f'MODE: NORMAL')
        if me.is_deputy():
            self.message.setText(f'MODE: DEPUTY')
        if me.is_master():
            self.message.setText(f'MODE: MASTER')


class GameScreen(Screen):
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
        self.setFocus()
        
        self.header.updateData(*args, **kwargs)
        self.body.updateData(*args, **kwargs)
        self.footer.updateData(*args, **kwargs)

    def keyPressEvent(self, event):
        log.debug(str(event.key()))
        
        if app.state.game.me.is_master():
            if event.key() == Qt.Key_W or event.key() == Qt.Key_Up:
                app.state.game.my_snake.up()
            if event.key() == Qt.Key_S or event.key() == Qt.Key_Down:
                app.state.game.my_snake.down()
            if event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
                app.state.game.my_snake.left()
            if event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
                app.state.game.my_snake.right()
        elif app.state.game.me.is_viewer():
            print('I am VIEWER')
        else:
            if event.key() == Qt.Key_W or event.key() == Qt.Key_Up:
                app.node.steer(Direction.UP)
            if event.key() == Qt.Key_S or event.key() == Qt.Key_Down:
                app.node.steer(Direction.DOWN)
            if event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
                app.node.steer(Direction.LEFT)
            if event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
                app.node.steer(Direction.RIGHT)
        return
