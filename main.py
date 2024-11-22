import sys
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow


con = sqlite3.connect("MainData.db")
cur = con.cursor()
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Sport Oracle'
        
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
        team_name = self.Team_Search.toPlainText()
        if team_name != "":
            self.Team_Name_Text.setText("Таблица: " + team_name)
            print(team_name)
        # обращаемся к поиску по названию

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())