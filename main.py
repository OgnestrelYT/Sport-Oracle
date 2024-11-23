import sys, os, shutil
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog


class NewTabel(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New File...")
        self.main = uic.loadUi('new_Tabel.ui', self)
        self.Buttons.accepted.connect(self.accept)
        self.Buttons.rejected.connect(self.reject)

    def accept(self):
        self.text = self.Text_Edit.toPlainText()
        s.tablename = self.text
        count = 0
        for i in self.text:
            if i in '1234567890':
                count += 1
        if self.text == "" or len(self.text) != 9 or self.text[4] != '-' or count != 8:
            self.Error_Text.setText("Название указано неверно")
        else:
            s.table = '''CREATE TABLE IF NOT EXISTS''' + f"'{self.text}'" +'''(
             id INTEGER ,
            Year INTEGER ,
            Mount INTEGER,
            Day INTEGER,
            Score INTEGER,
            Result TEXT
            )
            '''
            s.NewTable()
            self.hide()

    def reject(self):
        self.Error_Text.setText("")
        self.hide()

class Sure(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вы уверены?")
        
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
        self.Combo_Box.currentTextChanged.connect(self.boxChange)
        self.Update_Table.clicked.connect(self.New_Table)
        self.Result_button.clicked.connect(self.results)
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
        x = self.cur.execute("DELETE FROM " + f"'{self.Combo_Box.currentText()}'").fetchall()
        for i in range(1, a + 1):
            try:
                if self.s != True:
                    dmd = self.Main_Table.item(i - 1, 0).text().split('.')
                    x = '''INSERT INTO''' + f"'{self.Combo_Box.currentText()}'" + '''(id, Year, Mounth, Day, Score, Result) VALUES(?,?,?,?,?,?);'''
                    self.result = self.cur.execute(x, (i, dmd[0],dmd[1],dmd[2], self.Main_Table.item(i - 1, 1).text(), self.Main_Table.item(i - 1, 2).text())).fetchall()
                else:
                    dmd = self.Main_Table.item(i - 1, 0).text().split('.')
                    dmd2 = self.Main_Table.item(i - 1, 1).text().split('.')
                    print(dmd, dmd2)
                    x = '''INSERT INTO''' + f"'{self.Combo_Box.currentText()}'" + '''(id, Year, Mounth, Day, YearEnd, MounthEnd, DayEnd) VALUES(?,?,?,?,?,?,?);'''
                    self.result = self.cur.execute(x, (i, dmd[0], dmd[1], dmd[2], dmd2[0], dmd2[1], dmd2[2])).fetchall()
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
        self.s = False
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл')[0].split("/")[-1]
        if self.file.count(".") == 0:
            if self.file != "":
                self.con = sqlite3.connect(self.db_path + self.file)
                self.cur = self.con.cursor()
                
                self.yearsList = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                self.Combo_Box.clear()

                for i in range(len(self.yearsList)):

                    if len(self.yearsList[i][0].split('-')) > 1:
                        self.Combo_Box.addItem(str(self.yearsList[i][0]))
                    else:
                        self.Combo_Box.addItem(str(self.yearsList[i][0][0:5]) + "-20" + str(int(self.yearsList[i][0][7:9]) + 1))
                    
                a = self.Main_Table.rowCount()
                for i in range(a):
                    self.Main_Table.removeRow(0)

                self.Team_Name_Text.setText("Таблица: " + self.file)
                self.Error_Text.setText("")
                self.Save_Table_Button.setEnabled(True) # теперь можно сохранять таблицу
                self.Sessions_Table_Button.setEnabled(True)
                
                x = "SELECT name FROM sqlite_master WHERE type= 'table' "
                self.result = self.cur.execute(x).fetchall()
                self.result = self.cur.execute(''' SELECT *  FROM ''' + f"'{self.Combo_Box.currentText()}'").fetchall()
                self.result.sort(key=lambda x: (x[1], x[2], x[3]))
                for i in range(len(self.result)):
                    self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
                for i in range(len(self.result)):
                    self.date = str(self.result[i][1]) + '.' + str(self.result[i][2])  + '.' + str(self.result[i][3])
                    self.Main_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.date))
                    self.Main_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.result[i][4])))
                    self.Main_Table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.result[i][5])))
        else:
            self.Error_Text.setText("Не правильное разрешение файла")
    
    def boxChange(self):
        a = self.Main_Table.rowCount()
        for i in range(a):
            self.Main_Table.removeRow(0)
        if self.s != True:
            x = "SELECT name FROM sqlite_master WHERE type= 'table' "
            self.result = self.cur.execute(x).fetchall()
            self.result = self.cur.execute(''' SELECT *  FROM ''' + f"'{self.Combo_Box.currentText()}'").fetchall()
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
            self.con = sqlite3.connect(self.db_path + 'Sessions')
            a = self.Main_Table.rowCount()
            for i in range(a):
                self.Main_Table.removeRow(0)
            self.result = self.cur.execute(''' SELECT *  FROM ''' + f"'{self.Combo_Box.currentText()}'").fetchall()
            self.result.sort(key=lambda x: (x[1], x[2], x[3]))
            for i in range(len(self.result)):
                self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
            for i in range(len(self.result)):
                self.date = str(self.result[i][1]) + '.' + str(self.result[i][2])  + '.' + str(self.result[i][3])
                self.dateEnd = str(self.result[i][4]) + '.' + str(self.result[i][5]) + '.' + str(self.result[i][6])
                self.Main_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.date))
                self.Main_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.dateEnd))
    def sessionsBefore(self):
        self.type = "sessions"
        ses = Sure()
        ses.show()
    
    def sessions(self):
        self.s = True
        self.Sessions_Table_Button.setEnabled(False)
        self.con = sqlite3.connect(self.db_path + "Sessions")
        self.cur = self.con.cursor()
        
        self.yearsList = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        self.Combo_Box.clear()
        for i in range(len(self.yearsList)):

            if len(self.yearsList[i][0].split('-')) > 1:
                self.Combo_Box.addItem(str(self.yearsList[i][0]))
            else:
                self.Combo_Box.addItem(str(self.yearsList[i][0][0:5]) + "-20" + str(int(self.yearsList[i][0][5:9]) + 1))

        a = self.Main_Table.rowCount()
        for i in range(a):
            self.Main_Table.removeRow(0)
        
        x = "SELECT name FROM sqlite_master WHERE type= 'table' "
        self.result = self.cur.execute(x).fetchall()
        print(self.result[0][0])
        self.result = self.cur.execute(''' SELECT *  FROM ''' + f"'{self.result[0][0]}'").fetchall()
        self.result.sort(key=lambda x: (x[1], x[2], x[3]))
        self.Team_Name_Text.setText("Расписание сессий")
        g = self.Main_Table.columnCount()
        for i in range(g):
            self.Main_Table.removeColumn(0)
        for i in range(2):
            self.Main_Table.insertColumn(0)
        #()
        self.Main_Table.setHorizontalHeaderLabels(["Начало", "Конец"])
        for i in range(len(self.result)):
            self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
        for i in range(len(self.result)):

            self.date = str(self.result[i][1]) + '.' + str(self.result[i][2])  + '.' + str(self.result[i][3])
            self.dateEnd = str(self.result[i][4]) + '.' + str(self.result[i][5])  + '.' + str(self.result[i][6])

            self.Main_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.date))
            self.Main_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.dateEnd))

    def New_Table(self):
        f = NewTabel()
        f.show()
        pass

    def NewTable(self):
        Flag = True
        for i in self.yearsList:
            if s.tablename == i[0]:
                Flag = False
        if Flag:
            x = self.cur.execute(s.table)
            self.yearsList = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            self.Combo_Box.addItem(str(self.yearsList[-1][0]))

    def results(self):
        msg = QtWidgets.QMessageBox()
        days = [1] * 365

        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Информация\n1\n2')
        msg.setWindowTitle('Результат')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())