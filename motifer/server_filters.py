import logging

def get_log_type(record):
    func_name = record.funcName
    if func_name == "__motifer_before_request__":
        log_type = "request"
    elif func_name == "__motifer_after_request__":
        log_type = "response"
    else:
        log_type = "service"
    return log_type

class ServerLogFilter(logging.Filter):

    def __init__(self, server, service, *args, **kwargs):
        super(ServerLogFilter, self).__init__(*args, **kwargs)
        self.flaskApp = server
        self.service = service

    # This is a logging filter that makes the request ID available for use in the logging format.
    def filter(self, record, *args, **kwargs):
        record.service = self.service if self.service is not None else 'motifer'
        record.log_type = get_log_type(record)
        return super(ServerLogFilter, self).filter(record, *args, **kwargs)