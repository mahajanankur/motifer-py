import uuid
import logging, contextvars
from fastapi import Request

# Returns the current request ID or a new one if there is none
# def request_id(request: Request):
def request_id(context):
    request_id = context.get()
    if request_id:
        return request_id
    return uuid.uuid4()

def get_log_type(record):
    func_name = record.funcName
    if func_name != "__motifer_middleware__":
        log_type = "service"
    return log_type

class FastRequestIdFilter(logging.Filter):

    def __init__(self, server, service, context, *args, **kwargs):
        super(FastRequestIdFilter, self).__init__(*args, **kwargs)
        self.fastApp = server
        self.service = service
        self.context = context

    # This is a logging filter that makes the request ID available for use in the logging format.
    def filter(self, record, *args, **kwargs):
        # record.request_id = request_id(self.flaskApp) if (self.flaskApp is not None and self.flaskApp.has_request_context()) else ''
        record.request_id = request_id(self.context) if (self.fastApp is not None) else '-'
        # record.request_id = request_id() if (self.service is not None) else '00000000-0000-0000-0000-000000000000'
        record.service = self.service if self.service is not None else 'motifer'
        func_name = record.funcName
        if func_name != "__motifer_middleware__":
            record.log_type = "service"
        # record.log_type = get_log_type(record)
        return super(FastRequestIdFilter, self).filter(record, *args, **kwargs)

