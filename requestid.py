import logging
import logging.config
from random import randint
from flask import Flask
from flask_log_request_id import RequestID, RequestIDLogFilter

def generic_add(a, b):
    """Simple function to add two numbers that is not aware of the request id"""
    logging.debug('Called generic_add({}, {})'.format(a, b))
    return a + b

app = Flask(__name__)
RequestID(app)

# Setup logging
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - level=%(levelname)s - request_id=%(request_id)s - %(message)s"))
handler.addFilter(RequestIDLogFilter())  # << Add request id contextual filter
logging.getLogger().addHandler(handler)


@app.route('/')
def health():
    a, b = randint(1, 15), randint(1, 15)
    logging.info('Adding two random numbers {} {}'.format(a, b))
    return str(generic_add(a, b))

if __name__ == '__main__':
    app.run()