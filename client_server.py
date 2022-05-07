from PyQt5 import QtWidgets, QtCore
import clientui

import requests
import json


def sender(method, params=None):
    url = "http://localhost:4000/jsonrpc"

    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(url, json=payload).json()
    return response


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super(ExampleApp, self).__init__()
        self.setupUi(self)
        self.pushButton_2.pressed.connect(self.send_request_EnumirateBoard)
        self.pushButton_3.pressed.connect(self.send_request_EnumirateBoardPorts)
        self.pushButton_4.pressed.connect(self.send_request_GetBoardOfType)
        self.pushButton_5.pressed.connect(self.send_request_GetBoardPortsOfType)
        self.pushButton_6.pressed.connect(self.send_request_EnumiratePortCapabilities)
        self.pushButton_7.pressed.connect(self.send_request_CallPortMethod)

    def send_request_EnumirateBoard(self):
        get_response = sender('enumirateBoard')
        try:
            result = get_response.get('result')
            for name in result:
                self.textBrowser.append(name)
            self.textBrowser.append('')
        except:
            pass

    def send_request_EnumirateBoardPorts(self):
        name_serial = self.lineEdit.text()
        try:
            get_response = sender('enumirateBoardPorts', [name_serial])
            result = get_response.get('result')
            ports = f'{result[0]}'
            for i in result[1:]:
                ports += f',  {i}'
            self.textBrowser.append(f'{name_serial} - {ports}')
            self.textBrowser.append('')
            self.lineEdit.clear()
        except:
            pass

    def send_request_GetBoardOfType(self):
        name = self.lineEdit_4.text()
        try:
            get_response = sender('getBoardOfType', [name])
            result = get_response.get('result')
            for name_sereal in result:
                self.textBrowser.append(name_sereal)
            self.textBrowser.append('')
            self.lineEdit_4.clear()
        except:
            pass

    def send_request_GetBoardPortsOfType(self):
        name_serial = self.lineEdit_6.text()
        port = self.lineEdit_5.text()
        try:
            get_response = sender('getBoardPortsOfType', [name_serial, port])
            result = get_response.get('result')
            self.textBrowser.append(f'{name_serial},  {port} - {result}')
            self.textBrowser.append('')
            self.lineEdit_6.clear()
            self.lineEdit_5.clear()
        except:
            pass

    def send_request_EnumiratePortCapabilities(self):
        name_serial = self.lineEdit_8.text()
        port = self.lineEdit_7.text()
        try:
            get_response = sender('enumiratePortCapabilities', [name_serial, port])
            result = get_response.get('result')
            methods = f'{result[0]}  '
            for method in result[1:]:
                methods += f', {method}'
            self.textBrowser.append(f'{name_serial},  {port} - {methods}')
            self.textBrowser.append('')
            self.lineEdit_8.clear()
            self.lineEdit_7.clear()
        except:
            pass

    def send_request_CallPortMethod(self):
        name_serial = self.lineEdit_9.text()
        port = self.lineEdit_10.text()
        method = self.lineEdit_3.text()
        try:
            get_response = sender('callPortMethod', [name_serial, port, method])
            result = get_response.get('result')
            self.textBrowser.append(f'{name_serial},  {port} - {result}')
            self.textBrowser.append('')
            self.lineEdit_9.clear()
            self.lineEdit_10.clear()
            self.lineEdit_3.clear()
        except:
            pass

app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()