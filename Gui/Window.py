
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QGridLayout

from Gui.ScreenManager import ScreenManager

from App import app


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Preferred)
        size_policy.setVerticalPolicy(QSizePolicy.Preferred)

        self.central_widget = QWidget(self)
        self.central_widget.setSizePolicy(size_policy)

        self.screen_manager = ScreenManager(self.central_widget)

        self.central_layout = QGridLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.addWidget(self.screen_manager)

        self.central_widget.setLayout(self.central_layout)

        self.setCentralWidget(self.central_widget)
        self.setSizePolicy(size_policy)

        display_geometry = QDesktopWidget().availableGeometry()
        display_w = display_geometry.width()
        display_h = display_geometry.height()

        window_w = display_w * 3 // 4
        window_h = display_h * 3 // 4
        self.resize(window_w, window_h)
        

    def closeEvent(self, event):
        if app.node is not None:
            app.node.stop()
        event.accept()
