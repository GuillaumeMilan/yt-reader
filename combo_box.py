from PyQt5.QtWidgets import QComboBox, QWidget, QHBoxLayout

class ComboDemo(QWidget):
   def __init__(self, parent = None, video_player = None):
      super(ComboDemo, self).__init__(parent)
      self.__video_player = video_player
      layout = QHBoxLayout()
      self.cb = QComboBox()
      self.cb.addItems(['Audio', 'Video'])
      self.cb.currentIndexChanged.connect(self.selectionchange)
		
      layout.addWidget(self.cb)
      self.setLayout(layout)
   def selectionchange(self,i):
       if self.__video_player != None:
           self.__video_player.set_mode(self.cb.currentText())
#
#      for count in range(self.cb.count()):
#         print(self.cb.itemText(count))
#      print("Current index",i,"selection changed ",self.cb.currentText())
