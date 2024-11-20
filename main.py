import sys
import os

from PyQt6 import QtWidgets
from dotenv import load_dotenv
import re

from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from ui.first import Ui_FirstTimeWindow
from ui.interf import Ui_MainWindow
from ui.next import Ui_SubsequentWindow

from backend.qwery import check_table_exists, create_table, check_user
from backend.qwery import create_user, pars_pass, save_data
from backend.qwery import remove_data
from backend.bot import sand_code, gev_auth_cod

testBool = False
pattern_password = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
pattern_url = r'^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?$'

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
                if create_user('users.db', str(self.lineEdit.text()), int(self.tgIdEdit.text())):
                    # print('успешно в бд')
                    # else:
                    # print('такой юзер уже есть')
                    create_user('users.db', str(self.lineEdit.text()), int(self.tgIdEdit.text()))
                    self.close()
                    self.auth_user = LoginWin()
                    self.auth_user.show()

                else:
                    self.statusbar.showMessage('пользователь с таким ником уже есть')

        else:
            self.statusbar.showMessage('uncorrect auth cod')


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, nic_user):
        super().__init__()
        self.setupUi(self)
        # self.tableWidget.setEnabled(False)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.nic_user = nic_user
        self.tableWidget.cellClicked.connect(self.copy)
        self.data_table()
        self.saveBtn.clicked.connect(self.get_data)
        self.DelBtn.clicked.connect(self.del_data)

    def data_table(self):
        print(self.nic_user)
        print(check_user('users.db', self.nic_user)[1])

        data = pars_pass('users.db', self.nic_user)
        print(data)

        self.tableWidget.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def get_data(self):
        name_ser = self.nameEdit.text()
        URL = self.siteUrlEdit.text()
        login = self.loginEdit.text()
        paswd = self.passwordEdit.text()

        if not bool(re.match(pattern_url, URL)):
            self.statusbar.showMessage(r'Не содержит URL. Должен начинатся с https://', 3000)
            return

        if not bool(re.match(pattern_password, paswd)):
            self.statusbar.showMessage(
                'Пароль ненадежный: должен быть не менее 8 символов, содержать заглавные и строчные буквы, '
                'цифры и специальные символы.', 3000
            )

        save_data('users.db', tuple([self.nic_user, name_ser, URL, login, paswd]))
        self.nameEdit.clear()
        self.siteUrlEdit.clear()
        self.loginEdit.clear()
        self.passwordEdit.clear()

        self.data_table()

    def del_data(self):
        name_ser = self.nameEdit.text()
        URL = self.siteUrlEdit.text()
        login = self.loginEdit.text()
        paswd = self.passwordEdit.text()

        if not bool(re.match(pattern_url, URL)):
            self.statusbar.showMessage(r'Не содержит URL. Должен начинатся с https://', 3000)
            return

        if not remove_data('users.db', tuple([self.nic_user, name_ser, URL, login, paswd])):
            self.nameEdit.clear()
            self.siteUrlEdit.clear()
            self.loginEdit.clear()
            self.passwordEdit.clear()

            self.data_table()
            self.statusbar.showMessage('Данные удалены', 3000)
        else:
            self.statusbar.showMessage('Данные не найдены', 3000)

    def copy(self, row, column):
        item = self.tableWidget.item(row, column)
        if item:
            clipboard = QApplication.clipboard()
            clipboard.setText(item.text())
            self.statusbar.showMessage(f"Скопировано: {item.text()}", 2000)


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
            self.close()
            nic_user = self.NicEdit.text()
            self.main_windows = MainWin(nic_user)
            self.main_windows.show()
            self.main_windows.statusbar.showMessage(nic_user)
        else:
            print(2)
            self.statusbar.showMessage('не верный код авторизации')


def main():
    app = QApplication(sys.argv)
    check_user = LoginWin()
    check_user.show()
    sys.exit(app.exec())
    create_table('users.db')


if __name__ == '__main__':
    main()
