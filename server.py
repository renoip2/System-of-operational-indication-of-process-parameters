#!/usr/bin/env python

import socket
import serial
import threading
import socketserver
import time

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

PORT = '/dev/ttyUSB0'

master = modbus_rtu.RtuMaster(serial.Serial(
    port=PORT, baudrate=9600, bytesize=8, parity='E', stopbits=1, xonxoff=0))
master.set_timeout(5.0)
master.set_verbose(True)
global request_list, data_list
request_list = [' ',' ',' ']
data_list = [' ',' ',' ']

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'utf-8')
        data = data.split(', ')
        global request_list, data_list
        for i in reversed(range(len(request_list))):
            if data == request_list[i]:
                mes = data_list[i]
                request_list.append(' ')
                data_list.append(' ')
                break
        else:
            hr = []
            for i in range(int(data[1])//120,
                           (int(data[1])+int(data[2]))//120 + bool((
                               int(data[0])+int(data[1]))%120)):
                if int(data[0]) == 4:hr.extend(list(master.execute(
                    1, cst.READ_HOLDING_REGISTERS,i*120,120)))
                elif int(data[0]) == 0:hr.extend(list(master.execute(
                    1, cst.READ_COILS,i*120,120)))
                elif int(data[0]) == 1:hr.extend(list(master.execute(
                    1, cst.READ_DISCRETE_INPUTS,i*120,120)))
                elif int(data[0]) == 3:hr.extend(list(master.execute(
                    1, cst.READ_INPUT_REGISTERS,i*120,120)))
            print(hr)
            mes = str(hr[int(data[1])//120:int(data[1])//120+int(data[2])])
            mes = bytes(mes, 'utf-8')
            request_list.append(data)
            data_list.append(mes)

        request_list = request_list[1:]
        data_list = data_list[1:]
        self.request.sendall(mes)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "192.168.0.103", 5005

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    while 1:
        time.sleep(1)

    server.shutdown()
    server.server_close()
