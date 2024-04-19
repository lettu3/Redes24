#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
import connection
from constants import *
import threading
import sys

class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
       
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((addr, port))
            self.socket = server_socket
            self.directory = directory
            # Escuchar conexiones entrantes, va en serve()
            #server_socket.listen(1)
            print(f"Serving {directory} on {addr}:{port}.")
            self.threadLimiter = threading.BoundedSemaphore(5)
            #print("Servidor escuchando en", server_socket.getsockname())
        except Exception as e:
            print("Error al configurar el servidor:", str(e))

    def handle(self, conn: connection):
        """
        Función que para manejar un cliente.
        """
        self.threadLimiter.acquire()
        def handler():
            try:
                conn.handle()
            finally:
                self.threadLimiter.release()
        thread = threading.Thread(target = handler)
        thread.start()

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        self.socket.listen(1)
        while True:
        # Aceptar una conexión al servidor
            client_socket, _ = self.socket.accept()
            # Crear una instancia de Connection para manejar la conexión
            my_connection = connection.Connection(client_socket, self.directory)
            # Atender la conexión hasta que termine
            self.handle(my_connection)

def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()
