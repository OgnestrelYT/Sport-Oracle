import sys
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

con = sqlite3.connect("Футбол")
cur = con.cursor()
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
        x = "SELECT name FROM sqlite_master WHERE type= 'table' "
        self.result = cur.execute(x).fetchall()
        print(self.result[-1][0])
        self.result = cur.execute(''' SELECT *  FROM ''' + f"'{self.result[-1][0]}'").fetchall()
        self.result.sort(key=lambda x: (x[1], x[2], x[3]))
        if self.file.count(".") == 0:
            if self.file != "":
                self.Team_Name_Text.setText("Таблица: " + self.file)
                for i in range(len(self.result) - 1):
                    self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
                for i in range(len(self.result)):
                    self.date = str(self.result[i][1]) + '.' + str(self.result[i][2])  + '.' + str(self.result[i][3])
                    self.Main_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.date))
                    self.Main_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.result[i][4])))
                    self.Main_Table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.result[i][5])))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())