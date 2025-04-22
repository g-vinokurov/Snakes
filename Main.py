
import sys

from PyQt5.QtWidgets import QApplication

from Gui.Window import Window
from State.State import State

from Node import Node

from App import app


if __name__ == '__main__':
    application = QApplication([])
    
    app.state = State()
    app.state.user.name = sys.argv[1]
    
    app.gui = Window()
    app.gui.screen_manager.gotoScreen('start')
    app.gui.show()
    
    app.node = Node()
    app.node.start()
    
    sys.exit(application.exec())
