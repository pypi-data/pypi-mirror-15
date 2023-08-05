import logging
import socket
import ssl

from mock import MagicMock

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import amqpstorm.io
from amqpstorm.io import IO
from amqpstorm.exception import *
from amqpstorm import compatibility

from amqpstorm.tests.utility import FakeConnection

logging.basicConfig(level=logging.DEBUG)


class IOTests(unittest.TestCase):
    def test_io_socket_close(self):
        connection = FakeConnection()
        io = IO(connection.parameters)
        io.socket = MagicMock(name='socket', spec=socket.socket)
        io.close()

        self.assertIsNone(io.socket)

    def test_io_use_ssl_false(self):
        connection = FakeConnection()
        io = IO(connection.parameters)

        self.assertFalse(io.use_ssl)

    def test_io_use_ssl_true(self):
        connection = FakeConnection()
        connection.parameters['ssl'] = True
        io = IO(connection.parameters)

        self.assertTrue(io.use_ssl)

    def test_io_create_socket(self):
        connection = FakeConnection()
        io = IO(connection.parameters)

        self.assertFalse(io.use_ssl)

        addresses = io._get_socket_addresses()
        sock_address_tuple = addresses[0]
        sock = io._create_socket(socket_family=sock_address_tuple[0])

        if hasattr(socket, 'socket'):
            self.assertIsInstance(sock, socket.socket)
        elif hasattr(socket, '_socketobject'):
            self.assertIsInstance(sock, socket._socketobject)

    def test_io_get_socket_address(self):
        connection = FakeConnection()
        connection.parameters['hostname'] = '127.0.0.1'
        connection.parameters['port'] = 5672
        io = IO(connection.parameters)
        addresses = io._get_socket_addresses()
        sock_address_tuple = addresses[0]

        self.assertEqual(sock_address_tuple[4],
                         ('127.0.0.1', 5672))

    def test_io_simple_receive(self):
        connection = FakeConnection()
        io = IO(connection.parameters)

        self.assertFalse(io.use_ssl)

        io.socket = MagicMock(name='socket', spec=socket.socket)
        io.socket.recv.return_value = '12345'

        self.assertEqual(io._receive(), '12345')

    def test_io_simple_ssl_receive(self):
        connection = FakeConnection()
        connection.parameters['ssl'] = True
        io = IO(connection.parameters)

        self.assertTrue(io.use_ssl)

        if hasattr(ssl, 'SSLObject'):
            io.socket = MagicMock(name='socket', spec=ssl.SSLObject)
        elif hasattr(ssl, 'SSLSocket'):
            io.socket = MagicMock(name='socket', spec=ssl.SSLSocket)

        io.socket.read.return_value = '12345'

        self.assertEqual(io._receive(), '12345')

    def test_io_simple_send_zero_bytes_sent(self):
        connection = FakeConnection()

        io = IO(connection.parameters)
        io._exceptions = []
        io.socket = MagicMock(name='socket', spec=socket.socket)
        io.poller = MagicMock(name='poller', spec=amqpstorm.io.Poller)
        io.socket.send.return_value = 0
        io.write_to_socket('afasffa')

        self.assertIsInstance(io._exceptions[0], AMQPConnectionError)

    def test_io_default_ssl_version(self):
        if hasattr(ssl, 'PROTOCOL_TLSv1_2'):
            self.assertEqual(compatibility.DEFAULT_SSL_VERSION,
                             ssl.PROTOCOL_TLSv1_2)
        else:
            self.assertEqual(compatibility.DEFAULT_SSL_VERSION,
                             ssl.PROTOCOL_TLSv1)


class IOExceptionTests(unittest.TestCase):
    def test_io_receive_raises_socket_error(self):
        connection = FakeConnection()

        io = IO(connection.parameters)
        io._exceptions = []
        io.socket = MagicMock(name='socket', spec=socket.socket)
        io.socket.recv.side_effect = socket.error('error')
        io._receive()

        self.assertIsInstance(io._exceptions[0], AMQPConnectionError)

    def test_io_receive_raises_socket_timeout(self):
        connection = FakeConnection()
        io = IO(connection.parameters)
        io.socket = MagicMock(name='socket', spec=socket.socket)
        io.socket.recv.side_effect = socket.timeout('timeout')
        io._receive()

    def test_io_simple_send_with_error(self):
        connection = FakeConnection()

        io = IO(connection.parameters)
        io._exceptions = []
        io.socket = MagicMock(name='socket', spec=socket.socket)
        io.poller = MagicMock(name='poller', spec=amqpstorm.io.Poller)
        io.socket.send.side_effect = socket.error('error')
        io.write_to_socket('12345')

        self.assertIsInstance(io._exceptions[0], AMQPConnectionError)

    def test_io_ssl_connection_without_ssl_library(self):
        compatibility.SSL_SUPPORTED = False
        try:
            connection = FakeConnection()
            connection.parameters['hostname'] = 'localhost'
            connection.parameters['port'] = 1234
            parameters = connection.parameters
            parameters['ssl'] = True
            io = IO(parameters)
            self.assertRaisesRegexp(AMQPConnectionError,
                                    'Python not compiled with '
                                    'support for TLSv1 or higher',
                                    io.open, [])
        finally:
            compatibility.SSL_SUPPORTED = True

    def test_io_normal_connection_without_ssl_library(self):
        compatibility.SSL_SUPPORTED = False
        try:
            connection = FakeConnection()
            connection.parameters['hostname'] = 'localhost'
            connection.parameters['port'] = 1234
            parameters = connection.parameters
            io = IO(parameters)
            self.assertRaisesRegexp(AMQPConnectionError,
                                    'Could not connect to localhost:1234',
                                    io.open, [])
        finally:
            compatibility.SSL_SUPPORTED = True
