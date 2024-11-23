import sys, os, shutil
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog


class NewTabel(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Table...")
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
        if self.text != "":
            if len(self.text) != 9 or self.text[4] != '-' or count != 8 or (int(self.text[:4]) + 1 != int(self.text[5:])):
                self.Error_Text.setText("Название указано неверно")
            else:
                self.Error_Text.setText("")
                s.table = '''CREATE TABLE IF NOT EXISTS''' + f"'{self.text}'" +'''(
                id INTEGER ,
                Year INTEGER ,
                Mount INTEGER,
                Day INTEGER,
                Score INTEGER,
                Result TEXT
                )
                '''
                s.newTable()
                self.hide()
        else:
            self.Error_Text.setText("Название указано неверно")

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
        
        self.main = uic.loadUi('main.ui', self)
        self.Sessions_Table_Button.clicked.connect(self.sessionsBefore)
        self.Create_New_File_Button.clicked.connect(self.createNewFileAfter)
        self.Save_Table_Button.clicked.connect(self.saveTable)
        self.Load_Table_Button.clicked.connect(self.loadTableAfter)
        self.New_Row_Button.clicked.connect(self.newRow)
        self.Remove_Row_Button.clicked.connect(self.removeRow)
        self.Combo_Box.currentTextChanged.connect(self.boxChange)
        self.Update_Table_Button.clicked.connect(self.newTableWindow)
        self.Result_Button.clicked.connect(self.results)
        self.Main_Table.itemChanged.connect(self.change)
        s = self
        
        self.showButtons(False)
        
        self.exaple_path = "db/Example"
        self.db_path = "db/"
    
    def newRow(self):
        self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
        self.Save_Table_Button.setEnabled(True)
        self.Error_Text.setText("")
    
    def removeRow(self):
        self.Error_Text.setText("")
        if self.Main_Table.currentRow() == -1:
            self.Main_Table.removeRow(self.Main_Table.currentRow() + 1)
        else:
            self.Main_Table.removeRow(self.Main_Table.currentRow())
        if self.Main_Table.rowCount() == 0:
            self.Save_Table_Button.setEnabled(False)
    
    def saveTable(self):
        a = self.Main_Table.rowCount()
        try:
            self.Error_Text.setText("Сохранено!")
            if self.Combo_Box.count() > 0:
                try:
                    x = self.cur.execute("DELETE FROM " + f"'{self.Combo_Box.currentText()}'").fetchall()
                except:
                    x = self.cur.execute("DELETE FROM " + f"'{self.Combo_Box.itemText(0)}'").fetchall()
                for i in range(0, a):
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
            else:
                self.Error_Text.setText("Сначала создайте таблицу")
        except:
            self.Error_Text.setText("Ошибка сохранения")
    
    def createNewFileAfter(self):
        self.type = "createNewFile"
        ses = Sure()
        ses.show()

    def createNewFile(self):
        self.new_filename = ""
        file = NewFile()
        file.show()
    
    def newFile(self):
        self.showButtons(True)
        self.Save_Table_Button.setEnabled(False)
        self.Team_Name_Text.setText("Таблица: " + self.new_filename)
        self.Sessions_Table_Button.setEnabled(True)
        self.Save_Table_Button.setEnabled(True)
        self.Combo_Box.clear()
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
        self.showButtons(True)
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл')[0].split("/")[-1]
        if self.file.count(".") == 0:
            if self.file != "":
                self.con = sqlite3.connect(self.db_path + self.file)
                self.cur = self.con.cursor()
                
                self.yearsList = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                self.Combo_Box.clear()
                
                try:
                    for i in range(len(self.yearsList)):
                        if len(self.yearsList[i][0].split('-')) > 1:
                            self.Combo_Box.addItem(str(self.yearsList[i][0]))
                        else:
                            self.Combo_Box.addItem(str(self.yearsList[i][0][0:5]) + "-20" + str(int(self.yearsList[i][0][7:9]) + 1))
                    g = self.Main_Table.columnCount()
                    for i in range(g):
                        self.Main_Table.removeColumn(0)
                    for i in range(3):
                        self.Main_Table.insertColumn(0)
                    self.Main_Table.setHorizontalHeaderLabels(["Дата", "Счёт", "Результат"])
                    x = "SELECT name FROM sqlite_master WHERE type= 'table' "
                    self.result = self.cur.execute(x).fetchall()
                    if self.Combo_Box.count() > 0:
                        self.result = self.cur.execute(''' SELECT *  FROM ''' + f"'{self.Combo_Box.itemText(0)}'").fetchall()
                    self.result.sort(key=lambda x: (x[1], x[2], x[3]))
                    for i in range(len(self.result)):
                        self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
                    for i in range(len(self.result)):
                        self.date = str(self.result[i][1]) + '.' + str(self.result[i][2])  + '.' + str(self.result[i][3])
                        self.Main_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.date))
                        self.Main_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.result[i][4])))
                        self.Main_Table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.result[i][5])))
                except:
                    pass
                    
                a = self.Main_Table.rowCount()
                for i in range(a):
                    self.Main_Table.removeRow(0)

                self.Team_Name_Text.setText("Таблица: " + self.file)
                self.Error_Text.setText("")
                self.Save_Table_Button.setEnabled(True) # теперь можно сохранять таблицу
                self.Sessions_Table_Button.setEnabled(True)
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
        self.showButtons(True)
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
        self.Main_Table.setHorizontalHeaderLabels(["Начало", "Конец"])
        for i in range(len(self.result)):
            self.Main_Table.insertRow(self.Main_Table.currentRow() + 1)
        for i in range(len(self.result)):

            self.date = str(self.result[i][1]) + '.' + str(self.result[i][2])  + '.' + str(self.result[i][3])
            self.dateEnd = str(self.result[i][4]) + '.' + str(self.result[i][5])  + '.' + str(self.result[i][6])

            self.Main_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.date))
            self.Main_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.dateEnd))

    def newTableWindow(self):
        f = NewTabel()
        f.show()

    def newTable(self):
        Flag = True
        self.Error_Text.setText("")
        try:
            for i in self.yearsList:
                if s.tablename == i[0]:
                    Flag = False
        except:
            pass
        if Flag:
            x = self.cur.execute(s.table)
            self.yearsList = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            self.Combo_Box.addItem(str(self.yearsList[-1][0]))

    def results(self):
        msg = QtWidgets.QMessageBox()
        days = [1] * 365
        self.con = sqlite3.connect(self.db_path + "Sessions")
        self.cur = self.con.cursor()
        self.result = self.cur.execute(''' SELECT *  FROM ''' + f"'{self.Combo_Box.currentText()}'").fetchall()

        for i in self.result:
            l = [1,i[2],i[3]]
            if l[1] == 9:
                l[2] = int(l[2])
            if l[1] == 10:
                l[2] = int(l[2]) + 31
            if l[1] == 11:
                l[2] = int(l[2]) + 61
            if l[1] == 12:
                l[2] = int(l[2]) + 92
            if l[1] == 1:
                l[2] = int(l[2]) + 122
            if l[1] == 2:
                l[2] = int(l[2]) + 153
            if l[1] == 3:
                l[2] = int(l[2]) + 183
            if l[1] == 4:
                l[2] = int(l[2]) + 214
            if l[1] == 5:
                l[2] = int(l[2]) + 244
            if l[1] == 6:
                l[2] = int(l[2]) + 275
            if l[1] == 7:
                l[2] = int(l[2]) + 305
            if l[1] == 8:
                l[2] = int(l[2]) + 336
            le = l[2]
            l = [1,i[5],i[6]]
            if l[1] == 9:
                l[2] = int(l[2])
            if l[1] == 10:
                l[2] = int(l[2]) + 31
            if l[1] == 11:
                l[2] = int(l[2]) + 61
            if l[1] == 12:
                l[2] = int(l[2]) + 92
            if l[1] == 1:
                l[2] = int(l[2]) + 122
            if l[1] == 2:
                l[2] = int(l[2]) + 153
            if l[1] == 3:
                l[2] = int(l[2]) + 183
            if l[1] == 4:
                l[2] = int(l[2]) + 214
            if l[1] == 5:
                l[2] = int(l[2]) + 244
            if l[1] == 6:
                l[2] = int(l[2]) + 275
            if l[1] == 7:
                l[2] = int(l[2]) + 305
            if l[1] == 8:
                l[2] = int(l[2]) + 336
            re = l[2]

            for i in range(le - 14, re + 14):
                days[i] = 0
        print(days)

        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Информация\n1\n2')
        msg.setWindowTitle('Результат')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
    
    def showButtons(self, flag):
        self.Save_Table_Button.setEnabled(flag)
        self.Combo_Box.setEnabled(flag)
        self.Update_Table_Button.setEnabled(flag)
        self.Result_Button.setEnabled(flag)
        self.New_Row_Button.setEnabled(flag)
        self.Remove_Row_Button.setEnabled(flag)
    
    def change(self):
        self.Error_Text.setText("")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())