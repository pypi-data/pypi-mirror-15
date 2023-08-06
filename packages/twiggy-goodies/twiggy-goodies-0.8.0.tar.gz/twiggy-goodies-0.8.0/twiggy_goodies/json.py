# coding: utf-8
from __future__ import absolute_import

import os
import calendar
import anyjson
import datetime
import six
import socket
import pytz

from twiggy import outputs, levels
from twiggy_goodies.utils import force_str


class JsonOutput(outputs.Output):
    """Output from twiggy to JSON, useful for processing logs with logstash.
    """

    def __init__(self, filename=None, stream=None, source_host=None):
        self.fd = stream.fileno()
        self.filename = filename

        if source_host is None:
            source_host = socket.gethostname()

        severity_names = {
            levels.CRITICAL: 'CRITICAL',
            levels.DEBUG:    'DEBUG',
            levels.ERROR:    'ERROR',
            levels.INFO:     'INFO',
            levels.WARNING:  'WARNING',
        }


        def format(msg):
            fields = msg.fields.copy()
            fields['level'] = severity_names[fields['level']]
            timestamp = fields.pop('time')
            timestamp = datetime.datetime.utcfromtimestamp(calendar.timegm(timestamp))
            timestamp = timestamp.replace(tzinfo=pytz.utc)

            if msg.traceback:
                fields['exception'] = force_str(msg.traceback)

            for key, value in fields.items():
                if not isinstance(value, (int, float)) \
                   and not isinstance(value, six.string_types):
                    fields[key] = six.text_type(value)


            entry = {'@message': msg.text,
                     '@timestamp': timestamp.isoformat(),
                     '@source_host': source_host,
                     '@fields': fields}
            return anyjson.serialize(entry)

        super(JsonOutput, self).__init__(format=format, close_atexit=True)


    def _open(self):
        if self.filename:
            assert self.fd is None, 'You should not use arguments "stream" and "filename" together'

            dirname = os.path.dirname(self.filename)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)

            self.fd = os.open(self.filename, os.O_WRONLY | os.O_APPEND | os.O_CREAT)

    def _close (self):
        if self.filename:
            os.close(self.fd)

    def _write(self, msg):
        os.write(self.fd, (msg + '\n').encode('utf-8'))
