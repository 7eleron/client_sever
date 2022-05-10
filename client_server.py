from PyQt5 import QtWidgets, QtCore
import clientgui_2
import requests
import xml.etree.ElementTree as ET
import json


class ExampleApp(QtWidgets.QMainWindow, clientgui_2.Ui_MainWindow):
    def __init__(self):
        super(ExampleApp, self).__init__()
        self.setupUi(self)
        self.EnumirateBoard.pressed.connect(self.send_request_EnumirateBoard)
        self.CallPortMethod.pressed.connect(self.send_request_CallPortMethod)
        self.Save_xml.pressed.connect(self.save_xml)
        self.name_sereals = []

        self.Name_sereal.currentTextChanged.connect(self.port_type_change)
        self.Port_type.currentTextChanged.connect(self.port_change)


    # sends a request to the server
    def sender(self, method=None, params=None):
        url = "http://localhost:4000/jsonrpc"

        payload = {
            "method": method,
            "params": [params],
            "jsonrpc": "2.0",
            "id": 1}

        response = requests.post(url, json=payload).json()
        return response

    # Listen text in name_sereal and add list in port_type
    def port_type_change(self):
        name_sereal = self.Name_sereal.currentText()
        description = self.sender('enumirateBoard')
        result = description.get('result')
        for x in result:
            if x.get('name_sereal') == name_sereal:
                self.Port_type.clear()
                self.Port_type.addItems(x.get('type port'))

    # Listen text in port_type and add list in port
    def port_change(self):
        try:
            port_type = self.Port_type.currentText()
            name_sereal = self.Name_sereal.currentText()
            description = self.sender('enumirateBoard')
            result = description.get('result')
            for x in result:
                if x.get('name_sereal') == name_sereal:
                    count_port = x.get('count port type')
                    self.Port.clear()
                    self.Port.addItems(count_port.get(port_type))
        except Exception as e:
            self.textBrowser.append(f'Error: {e}')
            self.textBrowser.append('')
        self.Method.addItems(['Send signal', 'Stop signal'])

    # Button Enumirate Board
    def send_request_EnumirateBoard(self):
        try:
            req = self.sender('enumirateBoard')
            result = req.get('result')
            for board in result:
                self.name_sereals.append(board.get('name_sereal'))
                description = f"Name: {board.get('name')}" \
                              f"\nSereal: {board.get('sereal')}" \
                              f"\nType port: {board.get('type port')}" \
                              f"\nCount port type: {board.get('count port type')}"
                self.textBrowser.append(description)
                self.textBrowser.append('')
            self.Name_sereal.addItems(self.name_sereals)
        except Exception as e:
            self.textBrowser.append(f'Error: {e}')
            self.textBrowser.append('')

    # Button Call Port Method
    def send_request_CallPortMethod(self):
        try:
            name_serial = self.Name_sereal.currentText()
            port = self.Port.currentText()
            method = self.Method.currentText()
            req = self.sender('callPortMethod', method)
            result = req.get('result')

            if name_serial and port and method:
                self.textBrowser.append(f'{name_serial},  {port} - {result}')
                self.textBrowser.append('')
            else:
                self.textBrowser.append('Dont have a params!')
                self.textBrowser.append('')
        except Exception as e:
            self.textBrowser.append(f'Error: {e}')
            self.textBrowser.append('')

    # Button Save a description in XML
    def save_xml(self):
        try:
            req = self.sender('enumirateBoard')
            result = req.get('result')
            data = ET.Element('data')
            for i, item in enumerate(result, 1):
                board = ET.SubElement(data, 'board' + str(i))
                ET.SubElement(board, 'name').text = item['name']
                ET.SubElement(board, 'sereal').text = item['sereal']
                port_type = f'{item["type port"][0]}'
                for x in item['type port'][1:]:
                    port_type += f', {x}'
                ET.SubElement(board, 'portType').text = port_type
            desc_f = ET.ElementTree(data)
            desc_f.write('board.xml', xml_declaration=True)
            self.textBrowser.append('Done!')
            self.textBrowser.append('')
        except Exception as e:
            self.textBrowser.append(f'Error: {e}')
            self.textBrowser.append('')

app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()

