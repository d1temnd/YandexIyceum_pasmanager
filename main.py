import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.first import Ui_FirstTimeWindow
from ui.interf import Ui_MainWindow
from ui.next import Ui_SubsequentWindow
from backend.qwery import check_table_exists, create_table

testBool = False


# Наследуемся от виджета из PyQt6.QtWidgets и от класса с интерфейсом
class RegUser(QMainWindow, Ui_FirstTimeWindow):
    def __init__(self):
        super().__init__()
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.setupUi(self)
        # .show()
        # self.pushButton.clicked.connect(self.run)

    # def run(self):
    #     self.label.setText("OK")


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class LoginWin(QMainWindow, Ui_SubsequentWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    # print(check_table_exists('users.db', 'passMGR'))
    if check_table_exists('users.db', 'passMGR'):
        auth = LoginWin()
        auth.show()
    else:
        create_table('users.db')
        reg_user = RegUser()
        reg_user.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
