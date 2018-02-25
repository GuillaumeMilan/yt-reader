from PyQt5.QtWidgets import QLabel
def void():
    pass 

class Signal:
    def __init__(self):
        self.callback_function = void

    def connect(self,function):
        self.callback_function = function

    def execute(self):
        self.callback_function()

class TranslucidButton(QLabel):
    def __init__(self, parent = None):
        self.__parent = parent
        self.clicked = Signal()
        self.hover = Signal()
        super(TranslucidButton, self).__init__(parent)

    def mouseMoveEvent(self, event):
        self.hover

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.clicked.execute()
