import sys, os, shutil
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog


class Sure(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Are you sure?")
        
        self.main = uic.loadUi('sure.ui', self)
        self.Buttons.accepted.connect(self.accept)
        self.Buttons.rejected.connect(self.reject)
    
    def accept(self):
        if s.type == "sessions":
            s.type = ""
            s.sessions()
        elif s.type == "loadTable":
            s.type = ""
            s.loadTable()
        elif s.type == "createNewFile":
            s.type = ""
            s.createNewFile()
        self.hide()

    def reject(self):
        self.hide()


class NewFile(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New File...")
        
        self.main = uic.loadUi('new_file.ui', self)
        self.Buttons.accepted.connect(self.accept)
        self.Buttons.rejected.connect(self.reject)
    
    def accept(self):
        self.text = self.Text_Edit.toPlainText()
        if self.text == "":
            self.Error_Text.setText("Нельзя использовать пустое название")
        else:
            s.new_filename = self.text
            s.newFile()
            self.Error_Text.setText("")
        self.hide()

    def reject(self):
        self.Error_Text.setText("")
        self.hide()

class MyWidget(QMainWindow):
    def __init__(self):
        global s
        super().__init__()
        self.setWindowTitle("Sport Oracle")
        
        self.main = uic.loadUi('test.ui', self)
        self.Sessions_Table_Button.clicked.connect(self.sessionsBefore)
        self.Create_New_File_Button.clicked.connect(self.createNewFileAfter)
        self.Save_Table_Button.clicked.connect(self.saveTable)
        self.Load_Table_Button.clicked.connect(self.loadTableAfter)
        self.New_Row.clicked.connect(self.newRow)
        self.Remove_Row.clicked.connect(self.removeRow)
        s = self
        
        self.exaple_path = "Example"
        self.db_path = "db/"
    
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
            else:
                self.Error_Text.setText("Не правильное разрешение файла")
        else:
            self.Error_Text.setText("Не правильное разрешение файла")
    
    def saveTable(self):
        a = self.Main_Table.rowCount()
        self.Error_Text.setText("")
        dmd = self.date.split('.')
        x = self.cur.execute("DELETE FROM " + f"'{dmd[0]}'").fetchall()
        for i in range(1, a + 1):
            try:
                dmd = self.Main_Table.item(i - 1, 0).text().split('.')
                x = '''INSERT INTO''' + f"'{dmd[0]}'" + '''(id, Year, Mounth, Day, Score, Result) VALUES(?,?,?,?,?,?);'''
                self.result = self.cur.execute(x, (i, dmd[0],dmd[1],dmd[2], self.Main_Table.item(i - 1, 1).text(), self.Main_Table.item(i - 1, 2).text())).fetchall()
            except:
                self.Error_Text.setText("Ошибка в " + str(i) + " строке")
            self.con.commit()
    
    def createNewFileAfter(self):
        self.type = "createNewFile"
        ses = Sure()
        ses.show()

    def createNewFile(self):
        self.new_filename = ""
        file = NewFile()
        file.show()
    
    def newFile(self):
        self.Team_Name_Text.setText("Таблица: " + self.new_filename)
        self.Sessions_Table_Button.setEnabled(True)
        self.Save_Table_Button.setEnabled(True)
        a = self.Main_Table.rowCount()
        for i in range(a):
            self.Main_Table.removeRow(0)
        shutil.copy(self.exaple_path, self.db_path + self.new_filename)
    
    def loadTableAfter(self):
        self.type = "loadTable"
        ses = Sure()
        ses.show()
    
    def loadTable(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл')[0].split("/")[-1]
        if self.file.count(".") == 0:
            if self.file != "":
                a = self.Main_Table.rowCount()
                for i in range(a):
                    self.Main_Table.removeRow(0)
                
                self.con = sqlite3.connect(self.db_path + self.file)
                self.cur = self.con.cursor()
                
                self.yearsList = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                self.Combo_Box.clear()
                self.yearsList = list(self.yearsList)
                for i in range(0, len(self.yearsList) - 1):
                    self.Combo_Box.addItem(str(self.yearsList[i])[2:-3] + "/" + str(self.yearsList[i+1])[4:-3])

                self.Team_Name_Text.setText("Таблица: " + self.file)
                self.Error_Text.setText("")
                self.Save_Table_Button.setEnabled(True) # теперь можно сохранять таблицу
                self.Sessions_Table_Button.setEnabled(True)
                
                x = "SELECT name FROM sqlite_master WHERE type= 'table' "
                self.result = self.cur.execute(x).fetchall()
                self.result = self.cur.execute(''' SELECT *  FROM ''' + f"'{self.result[-1][0]}'").fetchall()
                self.result.sort(key=lambda x: (x[1], x[2], x[3]))
                self.Team_Name_Text.setText("Таблица: " + self.file)
                for i in range(len(self.result)):
                    self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
                for i in range(len(self.result)):
                    self.date = str(self.result[i][1]) + '.' + str(self.result[i][2])  + '.' + str(self.result[i][3])
                    self.Main_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.date))
                    self.Main_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.result[i][4])))
                    self.Main_Table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.result[i][5])))
        else:
            self.Error_Text.setText("Не правильное разрешение файла")
    
    def sessionsBefore(self):
        self.type = "sessions"
        ses = Sure()
        ses.show()
    
    def sessions(self):
        a = self.Main_Table.rowCount()
        for i in range(a):
            self.Main_Table.removeRow(0)
        self.Sessions_Table_Button.setEnabled(False)
        self.con = sqlite3.connect(self.db_path + "Sessions")
        self.cur = self.con.cursor()
        x = "SELECT name FROM sqlite_master WHERE type= 'table' "
        self.result = self.cur.execute(x).fetchall()
        self.result = self.cur.execute(''' SELECT *  FROM ''' + f"'{self.result[-1][0]}'").fetchall()
        self.result.sort(key=lambda x: (x[1], x[2], x[3]))
        self.Team_Name_Text.setText("Расписание сессий")
        for i in range(len(self.result)):
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