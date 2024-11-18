import sys
import os
from dotenv import load_dotenv

from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.first import Ui_FirstTimeWindow
from ui.interf import Ui_MainWindow
from ui.next import Ui_SubsequentWindow

from backend.qwery import check_table_exists, create_table, check_user
from backend.qwery import create_user
from backend.bot import sand_code, gev_auth_cod

testBool = False
load_dotenv('backend/.env')


class RegUser(QMainWindow, Ui_FirstTimeWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.last_code = None
        self.status_cod = None

        self.CheckTg.clicked.connect(self.check_tg)
        self.submitBtn.clicked.connect(self.reg_user_db)

    def check_tg(self):
        if self.tgIdEdit.text() == '':
            self.statusbar.showMessage('не указан tg id')
        else:
            self.last_code = gev_auth_cod()

            self.status_cod = sand_code(int(self.tgIdEdit.text()), str(self.last_code))
            if self.status_cod == 400:
                self.statusbar.showMessage('не верный tg id')
            print(self.last_code)

    def reg_user_db(self):
        if self.last_code == self.codeEdit.text():
            print(1)
            if self.lineEdit.text() == '':
                self.statusbar.showMessage('не указдан nicname')
            else:
                self.statusbar.clearMessage()
                # print('auth')
                if not create_user('users.db', str(self.lineEdit.text()), int(self.tgIdEdit.text())):
                    # print('успешно в бд')
                # else:
                    # print('такой юзер уже есть')
                    self.close()
                    self.auth_user = LoginWin()
                    self.auth_user.show()
                    self.auth_user.statusbar.showMessage("у вас уже есть аккаунт")


        else:
            self.statusbar.showMessage('uncorrect auth cod')


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LoginWin(QMainWindow, Ui_SubsequentWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.last_cod = None

        self.sendCodeBtn.clicked.connect(self.check_user)
        self.submitBtn.clicked.connect(self.check_cod_auth)

    def check_user(self):
        user_status = check_user('users.db', self.NicEdit.text())
        if user_status[0]:
            self.last_cod = gev_auth_cod()
            print(self.last_cod)
            sand_code(int(user_status[1]), str(self.last_cod))

        else:
            self.close()
            self.reg_window = RegUser()
            self.reg_window.show()
            self.reg_window.statusbar.showMessage("you don't have an account")

    def check_cod_auth(self):
        if self.last_cod == self.codeEdit.text():
            print(1)  # TODO: заход в интерфе основной интерфейс
            self.close()
            self.main_windows = MainWin()
            self.main_windows.show()
            self.main_windows.statusbar.showMessage(self.NicEdit.text())

        else:
            print(2)
            self.statusbar.showMessage('не верный код авторизыции')


def main():
    app = QApplication(sys.argv)
    check_user = LoginWin()
    check_user.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
