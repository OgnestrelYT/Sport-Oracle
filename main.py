import sys
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog


class SaveAs(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save As...")
        
        self.main = uic.loadUi('saveAs.ui', self)
        self.Buttons.accepted.connect(self.accept)
        self.Buttons.rejected.connect(self.reject)
    
    def accept(self):
        self.text = self.Text_Edit.toPlainText()
        if self.text == "":
            self.Error_Text.setText("Нельзя использовать пустое название")
        else:
            MyWidget.new_text = self.text
            self.Error_Text.setText("")
        self.hide()

    def reject(self):
        self.Error_Text.setText("")
        self.hide()

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sport Oracle")
        
        self.main = uic.loadUi('test.ui', self)
        self.Export_Table_Button.clicked.connect(self.exportTable)
        self.Save_As_Table_Button.clicked.connect(self.saveAsTable)
        self.Save_Table_Button.clicked.connect(self.saveTable)
        self.Load_Table_Button.clicked.connect(self.loadTable)
        self.New_Row.clicked.connect(self.newRow)
        self.Remove_Row.clicked.connect(self.removeRow)
    
    def newRow(self):
        self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
    
    def removeRow(self):
        if self.Main_Table.currentRow() == -1:
            self.Main_Table.removeRow(self.Main_Table.currentRow() + 1)
        else:
            self.Main_Table.removeRow(self.Main_Table.currentRow())
    
    def exportTable(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл')[0].split("/")[-1]
        if self.file.count(".") != 0:
            self.file = self.file.split(".")
            if self.file[-1] == "xls":
                self.Team_Name_Text.setText("Таблица: " + self.file[0])
                self.Error_Text.setText("")
                self.Save_Table_Button.setEnabled(True) # теперь можно сохранять таблицу
                self.Save_As_Table_Button.setEnabled(True) # теперь можно сохранять таблицу как
            else:
                self.Error_Text.setText("Не правильное разрешение файла")
        else:
            self.Error_Text.setText("Не правильное разрешение файла")
    
    def saveTable(self):
        pass

    def saveAsTable(self):
        self.new_filename = ""
        file = SaveAs()
        file.show()
    
    def loadTable(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл')[0].split("/")[-1]
        if self.file.count(".") == 0:
            if self.file != "":
                self.Team_Name_Text.setText("Таблица: " + self.file)
                self.Error_Text.setText("")
                self.Save_Table_Button.setEnabled(True) # теперь можно сохранять таблицу
                self.Save_As_Table_Button.setEnabled(True) # теперь можно сохранять таблицу как
                
                con = sqlite3.connect(self.file)
                cur = con.cursor()
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
        else:
            self.Error_Text.setText("Не правильное разрешение файла")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())