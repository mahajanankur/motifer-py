import uuid
import logging
from flask import g, request

# Returns the current request ID or a new one if there is none
# In order of preference:
#   * If we've already created a request ID and stored it in the flask.g context local, use that
#   * If a client has passed in the X-Request-Id header, create a new ID with that prepended
#   * Otherwise, generate a request ID and store it in flask.g.request_id
def request_id():
    if getattr(g, 'request_id', None):
        return g.request_id
    return uuid.uuid4()

class RequestIdFilter(logging.Filter):

    def __init__(self, server, service, *args, **kwargs):
    # def __init__(self, *args, **kwargs):
        super(RequestIdFilter, self).__init__(*args, **kwargs)
        # self.flaskApp = args.get("server")
        # self.service = args.get("service")
        self.flaskApp = server
        self.service = service

    # This is a logging filter that makes the request ID available for use in
    # the logging format. Note that we're checking if we're in a request
    # context, as we may want to log things before Flask is fully loaded.
    def filter(self, record, *args, **kwargs):
        # record.request_id = request_id(self.flaskApp) if (self.flaskApp is not None and self.flaskApp.has_request_context()) else ''
        # record.request_id = request_id(self.flaskApp) if (self.flaskApp is not None) else '00000000-0000-0000-0000-000000000000'
        record.request_id = request_id() if (self.service is not None) else '00000000-0000-0000-0000-000000000000'
        record.service = self.service if self.service is not None else ''
        return super(RequestIdFilter, self).filter(record, *args, **kwargs)