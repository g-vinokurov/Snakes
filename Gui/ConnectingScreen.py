
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

from Gui.Screen import Screen

from Gui.Colors import COLOR_WHITE, COLOR_BLACK
from Gui.Fonts import FONT_USSR_STENCIL

from Logger import log

from App import app


class ConnectingLabel(QLabel):
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
        self.setFont(QFont(str(FONT_USSR_STENCIL), 32))


class Body(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.label_connecting = ConnectingLabel(self)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label_connecting)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.label_connecting.setText('Connecting...')


class ConnectingScreen(Screen):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'''background-color: {COLOR_BLACK};''')

        self.body = Body(self)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.body)
        
        self.setLayout(self.layout)
        self.updateData()

    def updateData(self, *args, **kwargs):
        self.body.updateData(*args, **kwargs)
