# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

from socket import *
from constants import *
from base64 import b64encode
import os


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.activa = True
        self.socket = socket
        self.buffer = ''
        self.directory = directory

    def _recv(self):
        try:
            data = self.socket.recv(4096).decode("ascii")
            self.buffer += data
            if len(data) == 0:
                self.activa = False

        except UnicodeError:
            response = handle_error(BAD_REQUEST)
            self.send(response)
            self.activa = False
            print("Closing connection...")

    def readline(self):
        while EOL not in self.buffer and self.activa:
            self._recv()
        if EOL in self.buffer:
            response, self.buffer = self.buffer.split(EOL, 1)
            return response.strip()
        else:
            #El comando no sirve, termino la conexión.
            self.activa = False
            return ""

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        # activa es el booleano que va a controlar todo.
        print("Conectado!")
        while self.activa:
            comando = self.readline()
            if "\n" in comando:
                comando = handle_error(BAD_EOL)
                self.send(comando)
                self.activa = False
            if len(comando) > 0:
                self.parser(comando)
        self.socket.close()

    def parser(self, comando: str):
        args = comando.split()
        if args[0] == 'quit':
            if len(args) == 1:
                self.quit()
            else:
                code_error = handle_error(INVALID_ARGUMENTS)
                self.send(code_error)
        elif args[0] == 'get_file_listing':
            if len(args) == 1:
                self.get_file_listing()
            else:
                code_error = handle_error(INVALID_ARGUMENTS)
                self.send(code_error)
        elif args[0] == 'get_metadata':
            if len(args) == 2:
                filename = args[1]
                self.get_metadata(filename)
            else:
                ret_error = handle_error(INVALID_ARGUMENTS)
                self.send(ret_error)
                #No queda nada por hacer, retorno
                return
        elif  args[0] == 'get_slice':
            if len(args) == 4:
                filename = args[1]
                offset = args[2]
                size = args[3]
                self.get_slice(filename, offset, size)
            else:
                ret_error = handle_error(INVALID_ARGUMENTS)
                self.send(ret_error)
        else:
            response = handle_error(INVALID_COMMAND)
            self.send(response)

    def get_file_listing(self):
        """
        Obtiene un listado de los archivos en el directorio de @self
        """
        print("Request: get_file_listing")
        ret_code = handle_error(CODE_OK)
        my_files = os.listdir(self.directory)
        l = len(my_files)
        for j in range(1,l):
            #  [a,b] --> [a, '\r\n\', b, '\r\n]
            my_files.insert(l-j, EOL)
        self.send(ret_code)
        self.send(''.join(my_files) + EOL)
        
    def valido(self, archivo):
        return os.path.isfile(os.path.join(self.directory, archivo))

    def get_metadata(self, archivo):
        """
        Obtiene el tamano de un @archivo si es que existe en el directorio de @self
        """
        print("Request: get_metadata")
        ret_code = handle_error(CODE_OK)
        validos = set(archivo).difference(VALID_CHARS)
        #Argumentos inválidos
        if not len(validos) == 0:
            error1 = handle_error(INVALID_ARGUMENTS)
            self.send(error1)
        #No tiene argumentos o no existe el archivo.
        elif not self.valido(archivo):
            error2 = handle_error(FILE_NOT_FOUND)
            self.send(error2)
        else:
            data = os.path.getsize(os.path.join(self.directory, archivo))
            #Devuelvo el tamaño del archivo en formato string.
            tamaño = str(data)
            self.send(ret_code)
            self.send(tamaño)
        
    def get_slice(self, file, offset, size):
        """
        Obtiene un fragmento de un archivo @file, de tamano @size, a partir de un byte @offset
        """
        print("Request: get_slice")
        # Convertimos a enteros
        if(offset.isdigit() and size.isdigit()):
            offset = int(offset)
            size = int(size)
        else:
            error_ret = handle_error(INVALID_ARGUMENTS)
            self.send(error_ret)
            return
            
        
        if not self.valido(file):
            error_ret = handle_error(FILE_NOT_FOUND)
            self.send(error_ret)
            

        if offset < 0:
            error_ret = handle_error(BAD_OFFSET)
            self.send(error_ret)
            
        
        file = os.path.join(self.directory, file)
        if (size < 0 or size > os.path.getsize(file) or
              offset > os.path.getsize(file)):
            
            error_ret = handle_error(INVALID_ARGUMENTS)
            self.send(error_ret)
            return

        f = open(file, 'rb')
        f.seek(offset)
        out = f.read(size)
        f.close()
        error_ret = handle_error(CODE_OK)
        self.send(error_ret)
        self.send(out, 'b64encode')
        self.send('') # Se agrega EOL

        
    def quit(self):
        """
        Termina la conexión terminando el loop en la función handle.
        """
        codigo_ret = handle_error(CODE_OK)
        self.send(codigo_ret)
        self.activa = False
        print("Conexión terminada")

    # El mensaje puede ser en bytes o un string
    # Es en bytes cuando tiene un caracter fuera del idioma inglés.
    def send(self, contenido, instance='ascii'):
        if instance == 'ascii':
            # Lo agrego a mano
            contenido += EOL
            contenido = contenido.encode("ascii")
        elif instance == 'b64encode':
            contenido = b64encode(contenido)
        while len(contenido) > 0:
            envio = self.socket.send(contenido)
            contenido = contenido[envio:]

            
# Para manejar o enviar códigos.
def handle_error(j):
    assert j in error_messages.keys()
    return f"{j} {error_messages[j]}"
