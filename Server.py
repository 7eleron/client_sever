from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import json


class Board:
    all_name_bords = []
    all_bords = []

    def __init__(self, name, sereal, type_port, coun_port_type):
        self.name_sereal = name + '_' + sereal
        self.name = name
        self.sereal = sereal
        self.type_port = type_port
        self.count_port_type = coun_port_type

        # add charact and description in list
        Board.all_bords.append({'name': self.name,
                                'sereal': self.sereal,
                                'type port': self.type_port,
                                'count port type': self.count_port_type})
        if self.name not in self.all_name_bords:
            Board.all_name_bords.append(self.name)


    def port_method(self, methods):
        self.port_method = methods


class SaveXML:
    def save(self):
        pass


@dispatcher.add_method
def enumirateBoard():
    return Board.all_name_bords


@dispatcher.add_method
def getBoardOfType(name):
    lis = []
    for board in Board.all_bords:
        if name == board.get('name'):
            lis.append(f'{board.get("name")}_{board.get("sereal")}')
    return lis


@dispatcher.add_method
def enumirateBoardPorts(name_sereal):
    obj_board = eval(name_sereal)
    return obj_board.type_port


@dispatcher.add_method
def getBoardPortsOfType(name_sereal, port):
    obj_board = eval(name_sereal)
    return obj_board.count_port_type[port]


@dispatcher.add_method
def enumiratePortCapabilities(name_sereal, port):
    object_board = eval(name_sereal)
    return object_board.port_method.get(port)


@dispatcher.add_method
def callPortMethod(name_sereal, port, method):
    object_board = eval(name_sereal)
    if method == 'send signal':
        return 'Signal sent!'
    elif method == 'stop signal':
        return 'Signal stopped!'


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    Advantech_PCI_1602 = Board('Advantech', 'PCI_1602', ['RS422', 'RS485'], {'RS422': 1, 'RS485': 1})
    Advantech_PCI_1602.port_method({'RS422': ['send signal', 'stop signal'],
                                     'RS485': ['send signal', 'stop signal']})

    Advantech_PCI_1610 = Board('Advantech', 'PCI_1610', ['RS232', 'RS422', 'RS485'], {'RS232': 2, 'RS422': 1, 'RS485': 1})
    Advantech_PCI_1610.port_method({'RS232': ['send signal', 'stop signal'],
                                    'RS422': ['send signal', 'stop signal'],
                                     'RS485': ['send signal', 'stop signal']})

    MOXA_CP_102E = Board('MOXA', 'CP_102E', ['RS232'], {'RS232': 2})
    MOXA_CP_102E.port_method({'RS232': ['send signal', 'stop signal']})
    run_simple('localhost', 4000, application)

