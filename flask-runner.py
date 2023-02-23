# No need to add sys in real implementations.
# gunicorn --capture-output --enable-stdio-inheritance -w 1 --threads 10 -b 0.0.0.0:5002 flask-runner:app --timeout 1000
import sys, logging, time
# from motifer import FlaskLogFactory
# from flask import Flask, g, request
# app = Flask(__name__)
# FlaskLogFactory.alter_any_logger("gunicorn", level=logging.INFO, server=app)

# root_logger = logging.getLogger('root')
# g_logger = logging.getLogger('gunicorn')
# ge_logger = logging.getLogger('gunicorn.error')
# ga_logger = logging.getLogger('gunicorn.access')
# formatter = logging.Formatter("%(asctime)s [service] [-] [ml] [%(levelname)-4s] [%(filename)s:%(lineno)d] %(message)s")
# g_logger.handlers[0].setFormatter(formatter)
# ga_logger.handlers[0].setFormatter(formatter)
# root_logger.handlers[0].setFormatter(formatter)

sys.path.append('../')
from flask import Flask, g, request
# g_logger = logging.getLogger('gunicorn')
# root_logger = logging.getLogger('root')
# ge_logger = logging.getLogger('gunicorn.error')
# ga_logger = logging.getLogger('gunicorn.access')
from motifer import FlaskLogFactory

app = Flask(__name__)
factory = FlaskLogFactory(service="webappname", log_level=logging.DEBUG, server=app)
logger = factory.initialize()

def calculate():
    logger.error("Some error occured")
    logger.info("Some info logs")
    logger.critical("Some critical logs")
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