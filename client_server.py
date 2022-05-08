from PyQt5 import QtWidgets, QtCore
import clientgui_2

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


class ExampleApp(QtWidgets.QMainWindow, clientgui_2.Ui_MainWindow):

    def __init__(self):
        super(ExampleApp, self).__init__()
        self.setupUi(self)
        self.EnumirateBoard.pressed.connect(self.send_request_EnumirateBoard)
        self.CallPortMethod.pressed.connect(self.send_request_CallPortMethod)
        self.name_sereals = []
        self.description = sender('descriptions').get('result')

        description = self.description
        Name_sereal = self.Name_sereal
        Port_type = self.Port_type
        Port = self.Port

        def port_type_change():
            name_sereal = Name_sereal.currentText()
            for x in description:
                if x.get('name_sereal') == name_sereal:
                    Port_type.clear()
                    Port_type.addItems(x.get('type port'))
        self.Name_sereal.currentTextChanged.connect(port_type_change)

        def port_change():
            try:
                port_type = Port_type.currentText()
                name_sereal = Name_sereal.currentText()
                for x in description:
                    if x.get('name_sereal') == name_sereal:
                        count_port = x.get('count port type')
                        Port.clear()
                        Port.addItems(count_port.get(port_type))
            except:
                pass
        self.Port_type.currentTextChanged.connect(port_change)
        self.Method.addItems(['Send signal', 'Stop signal'])
    
    def send_request_EnumirateBoard(self):
        get_response = sender('enumirateBoard')
        try:
            result = get_response.get('result')
            for board in result:
                self.name_sereals.append(board.get('name_sereal'))
                description = f"Name: {board.get('name')}" \
                              f"\nSereal: {board.get('sereal')}" \
                              f"\nType port: {board.get('type port')}" \
                              f"\nCount port type: {board.get('count port type')}"
                self.textBrowser.append(description)
                self.textBrowser.append('')
            self.Name_sereal.addItems(self.name_sereals)
        except:
            pass

    def send_request_CallPortMethod(self):
        name_serial = self.Name_sereal.currentText()
        port = self.Port.currentText()
        method = self.Method.currentText()
        try:
            get_response = sender('callPortMethod', [name_serial, port, method])
            result = get_response.get('result')
            self.textBrowser.append(f'{name_serial},  {port} - {result}')
            self.textBrowser.append('')
        except:
            pass


app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()