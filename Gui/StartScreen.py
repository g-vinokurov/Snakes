
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt

from Gui.Screen import Screen

from Gui.Colors import COLOR_WHITE, COLOR_BLACK
from Gui.Fonts import FONT_USSR_STENCIL

from Logger import log

from App import app


class SnakesLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            background: none;
            border: none;
            outline: none;
            color: {COLOR_WHITE};
        ''')
        self.setFont(QFont(str(FONT_USSR_STENCIL), 80))
        self.setAlignment(Qt.AlignCenter)


class ClickToStartLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f'''
            background: none;
            border: none;
            outline: none;
            color: {COLOR_WHITE};
        ''')
        self.setFont(QFont(str(FONT_USSR_STENCIL), 24))
        self.setAlignment(Qt.AlignCenter)


class StartScreen(Screen):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'''background-color: {COLOR_BLACK};''')
        
        self.label_snakes = SnakesLabel(self)
        self.label_click_to_start = ClickToStartLabel(self)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label_snakes)
        self.layout.addWidget(self.label_click_to_start)

        self.setLayout(self.layout)
        self.updateData()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            app.gui.screen_manager.gotoScreen('menu')

    def updateData(self, *args, **kwargs):
        app.gui.setWindowTitle('Snakes')
        self.label_snakes.setText('SNAKES')
        self.label_click_to_start.setText('Click To Start')
