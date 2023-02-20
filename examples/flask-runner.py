from flask import Flask, g, request
import uuid
from motifer import FlaskLogFactory


app = Flask(__name__)
factory = FlaskLogFactory(service="chatbot", log_level="debug", server=app)
logger = factory.initialize()

def calculate():
    logger.error("Some error occured")
    return 10

# @app.before_request
# def before_request():
#     # g.request_id = request.headers.get('X-Request-Id', str(uuid.uuid4())
#     randUid = str(uuid.uuid4())
#     print("Random UID generated before request", randUid)
#     g.request_id = randUid

@app.route('/')
def health():
    logger.debug("In the root route of sample app.")
    calculate()
    return {"status": "okay"}

if __name__ == '__main__':
    app.run()
