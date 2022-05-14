import sqlite3
from sqlite3 import Error
from PyQt5 import QtWidgets
import trainee_gui
import time


class ExampleApp(QtWidgets.QMainWindow, trainee_gui.Ui_Test_trainee):
    def __init__(self):
        super(ExampleApp, self).__init__()
        self.setupUi(self)
        self.findButton.pressed.connect(self.execute_read_query)
        self.deleteButton_2.pressed.connect(self.delete_bd)

    def create_connection(self):
        path = 'bd.sqlite'
        connection = None
        try:
            connection = sqlite3.connect(path)
        except Error as e:
            self.textBrowser.append(f'Error {e}!')
            self.textBrowser.append('')
        return connection

    def execute_read_query(self):
        self.textBrowser.clear()
        start_time = time.time()
        connecte = self.create_connection()
        cur = connecte.cursor()
        count = 0
        search = self.lineEdit.text()
        try:

            for id, rubrics, text, created_date in cur.execute("SELECT * FROM data WHERE text LIKE ? "
                                                               "ORDER BY created_date", [f"%{search}%"]):
                if count == 21:
                    break
                else:
                    self.textBrowser.append(f"\nСовпадение №{count}:"
                                            f"\nid - {id}"
                                            f"\nРубрики - {rubrics},"
                                            f"\nДата публикации - {created_date}"
                                            f" \nТекст: \n{text}")
                    self.textBrowser.append('')
                    count += 1
        except Error as e:
            self.textBrowser.append(f'Error {e}!')
            self.textBrowser.append('')
        connecte.close()
        self.textBrowser.append("--- %s seconds ---" % (time.time() - start_time))
        self.textBrowser.append('')

    def delete_bd(self):
        connecte = self.create_connection()
        cur = connecte.cursor()
        id = self.lineEdit_2.text()
        try:
            cur.execute(f"DELETE FROM data WHERE id = {id}")
            self.textBrowser.append(f'ID {id} is delete!')
            self.textBrowser.append('')
            connecte.commit()
            connecte.close()
        except Error as e:
            self.textBrowser.append(f'Error {e}!')
            self.textBrowser.append('')


app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()




