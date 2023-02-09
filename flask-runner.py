from flask import Flask
from lib.index import LogFactory


app = Flask(__name__)
factory = LogFactory(service="chatbot", log_level="debug", server=app, console_log_output="stdout", logfile_file="ankur.log")
logger = factory.get_logger()

@app.route('/')
def health():
    logger.debug("Debug message")
    return 'Server running!'

if __name__ == '__main__':
    app.run(debug=True)