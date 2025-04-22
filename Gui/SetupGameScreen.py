
import json
import traceback

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

from State.Models.Proto.GameConfig import GameConfig

from Gui.Screen import Screen

from Gui.Colors import COLOR_WHITE, COLOR_BLACK, COLOR_RED
from Gui.Fonts import FONT_USSR_STENCIL

from Config import GAME_CONFIG_FILE

from Logger import log

from App import app


class GameConfigLabel(QLabel):
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


class ConfigParameterLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            padding-left: 0px;
            padding-right: 0px;
            padding-top: 0px;
            padding-bottom: 0px;
            color: {COLOR_WHITE};
        ''')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont(str(FONT_USSR_STENCIL), 20))


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


class StartGameButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f'''
            QPushButton {{
                background: none;
                padding-left: 4px;
                padding-right: 4px;
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


class BackToMenuButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f'''
            QPushButton {{
                background: none;
                padding-left: 4px;
                padding-right: 4px;
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


class GameConfigSection(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.label_game_config = GameConfigLabel(self)

        self.label_filename = ConfigParameterLabel(self)
        self.label_your_name = ConfigParameterLabel(self)
        self.label_config_field_size = ConfigParameterLabel(self)
        self.label_config_food_static = ConfigParameterLabel(self)
        self.label_config_state_delay = ConfigParameterLabel(self)

        self.label_filename.setAlignment(Qt.AlignRight)
        self.label_your_name.setAlignment(Qt.AlignRight)
        self.label_config_field_size.setAlignment(Qt.AlignRight)
        self.label_config_food_static.setAlignment(Qt.AlignRight)
        self.label_config_state_delay.setAlignment(Qt.AlignRight)

        self.label_filename_value = ConfigParameterLabel(self)
        self.label_your_name_value = ConfigParameterLabel(self)
        self.label_config_field_size_value = ConfigParameterLabel(self)
        self.label_config_food_static_value = ConfigParameterLabel(self)
        self.label_config_state_delay_value = ConfigParameterLabel(self)

        self.label_filename_value.setAlignment(Qt.AlignLeft)
        self.label_your_name_value.setAlignment(Qt.AlignLeft)
        self.label_config_field_size_value.setAlignment(Qt.AlignLeft)
        self.label_config_food_static_value.setAlignment(Qt.AlignLeft)
        self.label_config_state_delay_value.setAlignment(Qt.AlignLeft)

        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(8, 8, 8, 8)
        self.left_layout.setSpacing(16)
        self.left_layout.setAlignment(Qt.AlignVCenter)

        self.left_layout.addWidget(self.label_filename)
        self.left_layout.addWidget(self.label_your_name)
        self.left_layout.addWidget(self.label_config_field_size)
        self.left_layout.addWidget(self.label_config_food_static)
        self.left_layout.addWidget(self.label_config_state_delay)

        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(8, 8, 8, 8)
        self.right_layout.setSpacing(16)
        self.right_layout.setAlignment(Qt.AlignVCenter)

        self.right_layout.addWidget(self.label_filename_value)
        self.right_layout.addWidget(self.label_your_name_value)
        self.right_layout.addWidget(self.label_config_field_size_value)
        self.right_layout.addWidget(self.label_config_food_static_value)
        self.right_layout.addWidget(self.label_config_state_delay_value)

        self.config_layout = QHBoxLayout()
        self.config_layout.setContentsMargins(0, 0, 0, 0)
        self.config_layout.setSpacing(0)

        self.config_layout.addLayout(self.left_layout)
        self.config_layout.addLayout(self.right_layout)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.label_game_config)
        self.layout.addLayout(self.config_layout)
        
        self.layout.setStretch(1, 1)

        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.label_game_config.setText('Game Config')

        try:
            with open(GAME_CONFIG_FILE, encoding='utf-8') as file:
                json_obj = json.load(file)

            filename = GAME_CONFIG_FILE
            field_width = int(json_obj.get('width', 40))
            field_height = int(json_obj.get('height', 30))
            food_static = int(json_obj.get('food_static', 1))
            state_delay = int(json_obj.get('state_delay_ms', 1000))

            game_config = GameConfig(field_width, field_height, food_static, state_delay)
        except Exception as err:
            log.debug(f'{traceback.format_exc()}')
            log.error(f'Impossible to load game config from file {GAME_CONFIG_FILE} due to error. Default values used')
            
            filename = '(default values)'
            field_width = app.state.game_config.width
            field_height = app.state.game_config.height
            food_static = app.state.game_config.food_static
            state_delay = app.state.game_config.state_delay_ms
        else:
            app.state.game_config = game_config

        self.label_filename.setText('Config File:')
        self.label_your_name.setText('Your Name:')
        self.label_config_field_size.setText('Field Size:')
        self.label_config_food_static.setText('Food Static:')
        self.label_config_state_delay.setText('State Delay:')

        self.label_filename_value.setText(f'{filename}')
        self.label_your_name_value.setText(f'{app.state.user.name}')
        self.label_config_field_size_value.setText(f'{field_width} x {field_height}')
        self.label_config_food_static_value.setText(f'{food_static}')
        self.label_config_state_delay_value.setText(f'{state_delay} ms')


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

        self.game_config_section = GameConfigSection(self)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.game_config_section)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.game_config_section.updateData(*args, **kwargs)


class Footer(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.btn_start_game = StartGameButton(self)
        self.btn_start_game.clicked.connect(self.on_btn_start_game_clicked)

        self.btn_back_to_menu = BackToMenuButton(self)
        self.btn_back_to_menu.clicked.connect(self.on_btn_back_to_menu_clicked)

        self.left_layout = QHBoxLayout()
        self.left_layout.setContentsMargins(0, 32, 0, 32)
        self.left_layout.setSpacing(0)
        self.left_layout.setAlignment(Qt.AlignCenter)

        self.left_layout.addWidget(self.btn_back_to_menu)

        self.right_layout = QHBoxLayout()
        self.right_layout.setContentsMargins(0, 32, 0, 32)
        self.right_layout.setSpacing(0)
        self.right_layout.setAlignment(Qt.AlignCenter)

        self.right_layout.addWidget(self.btn_start_game)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.btn_start_game.setText('Start Game!')
        self.btn_back_to_menu.setText('Back To Menu')

    def on_btn_start_game_clicked(self):
        if app.state.game is not None:
            log.error('Impossible to start new game because current game exists')
            return
        
        try:
            app.state.start_game()
            app.node.start_game()
        except Exception as err:
            log.debug(f'{traceback.format_exc()}')
            log.error(f'Impossible to start game due to error: {err}')
            return
        
        app.gui.screen_manager.gotoScreen('game')
        
        log.info('Start Game')

    def on_btn_back_to_menu_clicked(self):
        app.gui.screen_manager.gotoScreen('menu')


class SetupGameScreen(Screen):
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
