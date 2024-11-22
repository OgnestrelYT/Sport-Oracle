import sys
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import random
import string
import shutil
import os


con = sqlite3.connect("MainData.db")
cur = con.cursor()
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.main = uic.loadUi('test.ui', self)
        self.Add_Tab_Button.clicked.connect(self.addTab)

    def addTab(self):
        new_but = QtWidgets.QPushButton(self.centralwidget)
        new_but.setFixedSize(QtCore.QSize(100, 100))
        new_but.setStyleSheet('background-color:red')
        self.gridLayout.addWidget(new_but, 1, 1)

    def logIn(self):
        self.login = self.Login_Text.toPlainText()
        self.password = self.Password_Text.toPlainText()
        x = 'SELECT login, password FROM users WHERE login = ?'
        self.result = cur.execute(x, (self.login,)).fetchall()
        if len(self.result) != 0 and self.result[0][0] == self.login and self.result[0][1] == self.password:
            x = 'SELECT mail FROM users WHERE login = ?'
            self.result = cur.execute(x,(self.login, )).fetchall()
            self.mail = self.result[0][0]
            self.loadMainscr()
        else:
            self.Error_Text.setText('Неверные данные')
            self.Login_Text.setText('')
            self.Password_Text.setText('')

    def registr(self):
        self.loginscr = uic.loadUi('Registr screen.ui', self)

        self.Registr_Button.clicked.connect(self.confirm)
        self.Back_Button.clicked.connect(self.backLog)

    def confirm(self):
        self.mail = self.Mail_Text.toPlainText()
        self.login = self.Login_Text.toPlainText()
        self.confr = self.Confirm_Text.toPlainText()
        self.password = self.Password_Text.toPlainText()
        flag = self.check(self.login, self.password, self.mail, self.confr)
        if flag == 'ok':
            x = """INSERT INTO users (login, password, mail) VALUES (?, ?, ?);"""
            self.result = cur.execute(x, (self.login, self.password, self.mail)).fetchall()
            con.commit()
            self.loadMainscr()
        else:
            self.Login_Text.setText('')
            self.Password_Text.setText('')
            self.Mail_Text.setText('')
            self.Confirm_Text.setText('')
            if flag == 'mail':
                self.Error_Text.setText('Почта уже занята или указана неверно')
            elif flag == 'login':
                self.Error_Text.setText('Логин уже занят')
            elif flag == 'password':
                self.Error_Text.setText('Пароли не совпадают или слишком короткие')


    def loadMainscr(self):
        self.mainscr = uic.loadUi('Main screen.ui', self)

        x = 'SELECT ids FROM users WHERE login = ?'
        self.result = cur.execute(x, (self.login,)).fetchall()
        if self.result[0][0] != None:
            self.ids = self.result[0][0].split('/')
            self.Files_Tabel.setRowCount(len(self.result[0][0].split('/')) - 1)
            for i in range(1, len(self.ids)):
                self.Files_Tabel.setItem(i - 1, 1, QtWidgets.QTableWidgetItem(self.ids[i]))
                x = 'SELECT name FROM files WHERE id = ?'
                self.result = cur.execute(x, (self.ids[i],)).fetchall()
                self.Files_Tabel.setItem(i - 1, 0, QtWidgets.QTableWidgetItem(self.result[0][0]))

        self.Upload_Button.clicked.connect(self.upload)
        self.Open_Button.clicked.connect(self.open)
        self.Account_Button.setText(self.login)
        self.Account_Button.clicked.connect(self.settings)
        self.Delete_Button.clicked.connect(self.delete)

    def settings(self):
        self.settingsscr = uic.loadUi('Settings screen.ui', self)

        self.Login_Text.setText(self.login)
        self.Password_Text.setText(self.password)
        self.Mail_Text.setText(self.mail)
        self.LogOut_Button.clicked.connect(self.backLog)
        self.Back_Button.clicked.connect(self.backMain)
        self.Save_Button.clicked.connect(self.saveSettings)


    def saveSettings(self):
        self.NewLogin = self.Login_Text.toPlainText()
        self.NewPassword = self.Password_Text.toPlainText()
        self.NewMail = self.Mail_Text.toPlainText()
        self.MailError_Text.setText('')
        self.PasswordError_Text.setText('')
        self.LoginError_Text.setText('')
        if self.NewMail != self.mail:
            x = 'SELECT mail FROM users WHERE mail = ?'
            result = cur.execute(x, (self.NewMail,)).fetchall()
            if '@' in self.NewMail and self.NewMail[0] != '@' and ('.ru' in self.NewMail or '.com' in self.NewMail) and len(result) == 0:
                x = 'UPDATE users SET mail = ? WHERE mail = ?'
                cur.execute(x, (self.NewMail, self.mail))
                con.commit()
                self.mail = self.NewMail
            else:
                self.Mail_Text.setText(self.mail)
                self.MailError_Text.setText('Почта не подходит')

        elif self.NewLogin != self.login:
            x = 'SELECT login FROM users WHERE login = ?'
            result = cur.execute(x, (self.NewLogin,)).fetchall()
            if len(result) == 0 and self.NewLogin != '':
                x = 'UPDATE users SET login = ? WHERE login = ?'
                cur.execute(x, (self.NewLogin, self.login))
                con.commit()
                self.login = self.NewLogin
            else:
                self.Login_Text.setText(self.login)
                self.LoginError_Text.setText('Логин занят')

        if self.NewPassword != self.password:
            if len(self.NewPassword) > 3:
                x = 'UPDATE users SET password = ? WHERE login = ?'
                cur.execute(x, (self.NewPassword, self.login))
                con.commit()
                self.password = self.NewPassword
            else:
                self.Password_Text.setText(self.password)
                self.PasswordError_Text.setText('Пароль слишком простой')
        con.commit()

    def backLog(self):
        self.login = ''
        self.loginscr = uic.loadUi('Login screen.ui', self)
        self.Log_Button.clicked.connect(self.logIn)
        self.Reg_Button.clicked.connect(self.registr)

    def backMain(self):
        self.loadMainscr()

    def open(self):
        self.ID = self.ID_Text.toPlainText()
        x = 'SELECT name FROM files WHERE id = ?'
        self.result = cur.execute(x, (self.ID, )).fetchall()
        if len(self.result) != 0:
            if '.txt' in self.result[0][0]:
                os.system("start " + 'Uploads/' + ('').join(self.result[0][0]))
        else:
            self.Error_Label.setText('Неверный id')
            self.ID_Text.setText('')
    def upload(self):
        self.filenames = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл')
        if self.filenames[0] != '':
            self.name = self.filenames[0].split('/')[-1]
            self.id = self.create_id(20)
            x = """INSERT INTO files (id, name) VALUES (?, ?)"""
            self.result = cur.execute(x, (self.id, self.name)).fetchall()
            x = 'SELECT ids FROM users WHERE login = ?'
            self.result = cur.execute(x, (self.login, )).fetchall()
            x = """UPDATE users SET ids = ? WHERE login = ?"""
            if self.result[0][0] != None:
                self.result = cur.execute(x, (self.result[0][0] + '/' + self.id, self.login)).fetchall()
            else:
                self.result = cur.execute(x, ('/' + self.id, self.login)).fetchall()
            con.commit()
            shutil.copyfile(self.filenames[0], 'Uploads/'+ self.name)
            x = 'SELECT ids FROM users WHERE login = ?'
            self.result = cur.execute(x, (self.login,)).fetchall()
            if len(self.result) != 0:
                self.ids = self.result[0][0].split('/')
                self.Files_Tabel.setRowCount(len(self.ids) - 1)
                for i in range(1, len(self.ids)):
                    self.Files_Tabel.setItem(i - 1, 1, QtWidgets.QTableWidgetItem(self.ids[i]))
                    x = 'SELECT name FROM files WHERE id = ?'
                    self.result = cur.execute(x, (self.ids[i],)).fetchall()
                    self.Files_Tabel.setItem(i - 1, 0, QtWidgets.QTableWidgetItem(self.result[0][0]))

    def delete(self):
        self.id = self.ID_Text.toPlainText()
        x = 'select id from files where id = ?'
        self.result = cur.execute(x, (self.id, )).fetchall()
        if len(self.result) != 0:
            x = 'select name from files where id = ?'
            self.result = cur.execute(x, (self.id,)).fetchall()
            os.remove('uploads/' + self.result[0][0])
            x = 'delete from files where id = ?'
            self.result = cur.execute(x, (self.id,)).fetchall()
            con.commit()
            x = 'select ids, login from users where ids like "%' + self.id + '%"'
            self.result = cur.execute(x).fetchall()
            self.ids = ''
            for i in self.result[0][0].split('/'):
                if i != self.id and i != '':
                   self.ids = '/' + i + self.ids
            x = 'update users set ids = ? where login = ?'
            self.result = cur.execute(x, (self.ids, self.result[0][1])).fetchall()
            con.commit()
        else:
            self.Error_Label.setText('Неверный id')
            self.ID_Text.setText('')
    def check(self, login, password, mail, confr):
        x = 'SELECT mail FROM users WHERE mail = ?'
        result = cur.execute(x, (mail,)).fetchall()
        if '@' in mail and mail[0] != '@' and ('.ru' in mail or '.com' in mail) and len(result) == 0:
                x = 'SELECT login, password FROM users WHERE login = ?'
                result = cur.execute(x, (login,)).fetchall()
                if len(result) == 0:
                    if password == confr and len(password) > 2:
                        return 'ok'
                    else:
                        return 'password'
                else:
                    return 'login'
        else:
            return 'mail'

    def create_id(self, length):
        return ''.join(random.choices(string.ascii_lowercase + string.digits,k=length))

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())