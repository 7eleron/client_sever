from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import json


class Boards():
    def __init__(self, name, sereal, type_port, coun_port_type):
        self.name = name
        self.sereal = sereal
        self.type_port = type_port
        self.count_port_type = coun_port_type

    def info(self):
        return f"Name: {self.name}, sereal: {self.sereal}, " \
               f"type port: {self.type_port}, coun port type: {self.count_port_type}"

    def port_method_connect(self, port):
        return f"Port {port} connect!"

    def port_method_disconnect(self, port):
        return f"Port {port} disconnect!"



Advantech = Boards('Advantech', 'PCI-1602B', ['RS422', 'RS485'], {'RS422': 1, 'RS485': 1})
MOXA = Boards('MOXA', 'CP-102E', ['RS-232'], {'RS-232': 2})

list_boards = [Advantech, MOXA]
dict_boards_method = {
    "AdvantechPCI-1602B": {
        'RS422': ['connect', 'disconnect'],
        'RS485': ['disconnect']
    },
    "MOXACP-102E": {
        'RS-232': ['connect', 'disconnect']
    }
}


@dispatcher.add_method
def enumirateBoard():
    lis = []
    for board in list_boards:
        lis.append(board.info())
    return lis


@dispatcher.add_method
def getBoardOfType(s):
    lis = []
    for board in list_boards:
        if s in board.info():
            lis.append(board.info())
    return lis


@dispatcher.add_method
def enumirateBoardPorts(board_name, sereal):
    for board in list_boards:
        if board_name and sereal in board.info():
            return board.type_port


@dispatcher.add_method
def getBoardPortsOfType(board_name, sereal, port):
    for board in list_boards:
        if board_name and sereal in board.info():
            return board.count_port_type[port]


@dispatcher.add_method
def getBoardPortsOfType(board_name, sereal, port):
    for board in list_boards:
        if board_name and sereal in board.info():
            return board.count_port_type[port]


@dispatcher.add_method
def enumiratePortCapabilities(board_name, sereal, port):
    for board in dict_boards_method:
        if board_name+sereal == board:
            return dict_boards_method.get(board).get(port)


@dispatcher.add_method
def callPortMethod(board_name, sereal, port, method):
    for board in dict_boards_method:
        if board_name+sereal == board:
            lis_method = dict_boards_method.get(board).get(port)
            for boar in list_boards:
                if board_name and sereal in boar.info():
                    if method == 'connect' and method in lis_method:
                        return boar.port_method_connect(port)
                    elif method == 'disconnect' and method in lis_method:
                        return boar.port_method_disconnect(port)


@Request.application
def application(request):
    dispatcher["enumirateBoard"] = lambda s: enumirateBoard()
    dispatcher["getBoardOfType"] = lambda s: getBoardOfType(s)
    dispatcher["enumirateBoardPorts"] = lambda board_name, sereal: enumirateBoardPorts(board_name, sereal)
    dispatcher["getBoardPortsOfType"] = lambda board_name, sereal, port: getBoardPortsOfType(board_name, sereal, port)
    dispatcher["enumiratePortCapabilities"] = lambda board_name, sereal, port: enumiratePortCapabilities(board_name, sereal, port)
    dispatcher["callPortMethod"] = lambda board_name, sereal, port, method: callPortMethod(board_name, sereal, port, method)

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)

