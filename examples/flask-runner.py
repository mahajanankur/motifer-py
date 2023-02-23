# No need to add sys in real implementations.
# gunicorn --capture-output --enable-stdio-inheritance -w 1 --threads 10 -b 0.0.0.0:5002 flask-runner:app --timeout 1000
import sys
sys.path.append('../')
from flask import Flask, g, request
import uuid, logging, time
from motifer import FlaskLogFactory

app = Flask(__name__)
factory = FlaskLogFactory(service="webappname", log_level=logging.DEBUG, server=app)
logger = factory.initialize()

def calculate():
    logger.error("Some error occured")
    # time.sleep(2)
    return 10

@app.route('/')
def health():
    logger.debug("In the root route of sample app.")
    calculate()
    logger.warning("Some warnings in the code.")
    return {"status": "okay"}

if __name__ == '__main__':
    app.run()