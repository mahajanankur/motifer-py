import uuid
import logging

# Generate a new request ID, optionally including an original request ID
def generate_request_id(original_id=''):
    new_id = uuid.uuid4()

    if original_id:
        new_id = "{},{}".format(original_id, new_id)

    return new_id

# Returns the current request ID or a new one if there is none
# In order of preference:
#   * If we've already created a request ID and stored it in the flask.g context local, use that
#   * If a client has passed in the X-Request-Id header, create a new ID with that prepended
#   * Otherwise, generate a request ID and store it in flask.g.request_id
def request_id(flask):
    if getattr(flask.g, 'request_id', None):
        return flask.g.request_id

    headers = flask.request.headers
    original_request_id = headers.get("X-Request-Id")
    new_uuid = generate_request_id(original_request_id)
    flask.g.request_id = new_uuid

    return new_uuid

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
        record.request_id = request_id(self.flaskApp) if self.flaskApp.has_request_context() else ''
        record.service = request_id(self.service) if self.service is not None else ''
        return super(RequestIdFilter, self).format(record,self.flaskApp, self.service, *args, **kwargs)