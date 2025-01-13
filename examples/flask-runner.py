# gunicorn --capture-output --enable-stdio-inheritance -w 1 --threads 10 -b 0.0.0.0:5002 flask-runner:app --timeout 1000
# No need to add sys in real implementations.
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
    logger.info("Some info logs")
    logger.critical("Some critical logs.")
    # time.sleep(2)
    return 10

@app.route('/health', methods=["GET", "POST"])
def health():
    logger.debug("In the root route of sample app.")
    req_body = request.get_json() if(request is not None and request.is_json == True) else {}
    req_args = dict(request.args) if request.args is not None else {}
    logger.info(f"Body: {req_body}")
    logger.info(f"Args: {req_args}")
    calculate()
    logger.warning("Some warnings in the code.")
    logger.suAlert("Some SU Alert message")
    logger.suAlert({"tenant_id": "123", "alertType": "Test Alert Type", "message": "SU Alert Message"})
    return {"status": "okay"}


if __name__ == '__main__':
    app.run()