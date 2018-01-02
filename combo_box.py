from PyQt5.QtWidgets import QComboBox, QWidget, QHBoxLayout

class ComboDemo(QWidget):
   def __init__(self, parent = None, interface = None):
      super(ComboDemo, self).__init__(parent)
      self.__interface = interface
      layout = QHBoxLayout()
      self.cb = QComboBox()
      self.cb.addItems(['Audio', 'Video'])
      self.cb.currentIndexChanged.connect(self.selectionchange)

      layout.addWidget(self.cb)
      self.setLayout(layout)
   def selectionchange(self, i):
       if self.__interface != None:
           self.__interface.set_player_mode(self.cb.currentText())
    
   def init_combo_box(self, value):
      index = self.cb.findText(value)
      print("Hallo:"+str(index))
      self.cb.setCurrentIndex(index)
