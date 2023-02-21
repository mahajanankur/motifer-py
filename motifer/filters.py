import uuid
import logging
from flask import g, request

# Returns the current request ID or a new one if there is none
def request_id():
    if getattr(g, 'request_id', None):
        return g.request_id
    return uuid.uuid4()

def get_log_type(record):
    func_name = record.funcName
    if func_name == "__motifer_before_request__":
        log_type = "request"
    elif func_name == "__motifer_after_request__":
        log_type = "response"
    else:
        log_type = "service"
    return log_type

class RequestIdFilter(logging.Filter):

    def __init__(self, server, service, *args, **kwargs):
        super(RequestIdFilter, self).__init__(*args, **kwargs)
        self.flaskApp = server
        self.service = service

    # This is a logging filter that makes the request ID available for use in the logging format.
    def filter(self, record, *args, **kwargs):
        # record.request_id = request_id(self.flaskApp) if (self.flaskApp is not None and self.flaskApp.has_request_context()) else ''
        record.request_id = request_id() if (self.flaskApp is not None) else '-'
        # record.request_id = request_id() if (self.service is not None) else '00000000-0000-0000-0000-000000000000'
        record.service = self.service if self.service is not None else 'motifer'
        record.log_type = get_log_type(record)
        return super(RequestIdFilter, self).filter(record, *args, **kwargs)

