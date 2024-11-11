import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.first import Ui_FirstTimeWindow


# Наследуемся от виджета из PyQt6.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_FirstTimeWindow):
    def __init__(self):
        super().__init__()
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.setupUi(self)
        # .show()
        # self.pushButton.clicked.connect(self.run)

    # def run(self):
    #     self.label.setText("OK")


def main():
    app = QApplication(sys.argv)

    ex = MyWidget()
    ex.show()
    if ex.close(): sys.exit()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
