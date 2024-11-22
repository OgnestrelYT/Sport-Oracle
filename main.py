import sys
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sport Oracle")
        
        self.main = uic.loadUi('test.ui', self)
        self.Save_Table_Button.clicked.connect(self.saveTable)
        self.Load_Table_Button.clicked.connect(self.loadTable)
        self.New_Row.clicked.connect(self.newRow)
        self.Remove_Row.clicked.connect(self.removeRow)
        self.load = False
    
    def newRow(self):
        self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
    
    def removeRow(self):
        if self.Main_Table.currentRow() == -1:
            self.Main_Table.removeRow(self.Main_Table.currentRow() + 1)
        else:
            self.Main_Table.removeRow(self.Main_Table.currentRow())
    
    def saveTable(self):
        pass
    
    def loadTable(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл')[0].split("/")[-1]
        if self.file.count(".") == 0:
            if self.file != "":
                self.Team_Name_Text.setText("Таблица: " + self.file)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())