# coding: utf-8

# $Id: $
from logging.handlers import SocketHandler
import socket
import time
import errno

from amqp import Message
from amqp.connection import AMQP_LOGGER
from six.moves.urllib.parse import urlparse

from logcollect.nonblocking import NonBlockingConnection


class AMQPHandler(SocketHandler, object):

    def __init__(self, broker_uri='amqp://localhost/', exchange='logstash',
                 exchange_type='topic',
                 durable=True, routing_key='logstash', auto_delete=False):
        super(AMQPHandler, self).__init__(None, None)
        self.broker_uri = broker_uri
        self.exchange = exchange
        self._routing_key = routing_key
        self._suffix = None
        self.exchange_type = exchange_type
        self.durable = durable
        self.auto_delete = auto_delete
        self._timeouted = False

    def get_routing_key(self):
        if self._suffix:
            return '%s.%s' % (self._routing_key, self._suffix)
        return self._routing_key

    def emit(self, record):
        try:
            self._suffix = record.name
            return super(AMQPHandler, self).emit(record)
        finally:
            self._suffix = None

    def makeSocket(self, **kwargs):
        propagate = AMQP_LOGGER.propagate
        # try to connect only for 1 second in a minute
        if self._timeouted and self._timeouted > time.time() - 60:
            raise socket.timeout()

        try:
            AMQP_LOGGER.propagate = False
            amqp_socket = AMQPSocket(self.broker_uri,
                                     self.exchange,
                                     self.exchange_type,
                                     self.get_routing_key,
                                     self.durable,
                                     self.auto_delete)
            self._timeouted = False
        except socket.timeout:
            self._timeouted = time.time()
            raise
        finally:
            AMQP_LOGGER.propagate = propagate
        return amqp_socket

    def makePickle(self, record):
        return self.formatter.format(record)


class AMQPSocket(object):
    connect_timeout = 10.0

    def __init__(self, broker_uri, exchange, exchange_type, routing_key_func,
                 durable, auto_delete):
        self.is_logging = True
        self.conn = NonBlockingConnection(
            connect_timeout=self.connect_timeout,
            **self._parse_broker_uri(broker_uri))
        self.channel = self.conn.channel()
        self.channel.exchange_declare(exchange=exchange,
                                      type=exchange_type,
                                      durable=durable,
                                      auto_delete=auto_delete)
        self.is_logging = False
        self.exchange = exchange
        if callable(routing_key_func):
            self.routing_key = routing_key_func
        else:
            self.routing_key = lambda: routing_key_func

    def sendall(self, data):
        if self.is_logging:
            return
        self.is_logging = True
        try:
            msg = Message(data)
            self.channel.basic_publish(msg, self.exchange, self.routing_key())
        finally:
            self.is_logging = False

    def close(self):
        try:
            self.conn.close()
        except socket.error:
            pass
        except IOError as e:
            # handle already closed connections
            if e.errno != errno.EPIPE:
                raise

    @staticmethod
    def _parse_broker_uri(broker_uri):
        url = urlparse(broker_uri)
        return {
            'host': url.hostname,
            'virtual_host': url.path,
            'userid': url.username,
            'password': url.password
        }
