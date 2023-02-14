from flask import Flask
from motifer.index import LogFactory


app = Flask(__name__)
factory = LogFactory(service="flask", log_level="debug", server=app)
logger = factory.get_logger()

@app.route('/')
def health():
    logger.debug("Debug message")
    return 'Server running!'

if __name__ == '__main__':
    app.run()