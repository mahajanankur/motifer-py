# uvicorn fast-api-runner:app --reload
# uvicorn fast-api-runner:app --log-level critical --reload
import sys
sys.path.append('../')
import uuid, logging, time
import uvicorn
from fastapi import FastAPI, Request
from motifer import FastApiLogFactory

app = FastAPI()
factory = FastApiLogFactory(service="webappname", log_level=logging.DEBUG, server=app)
logger = factory.initialize()


# @app.middleware("http")
# async def before_request(request: Request, call_next):
#     # Execute some code before each request
#     print("***** Before request *****")
#     app.state.requestId = "ankur"
#     response = await call_next(request)
#     return response

# @app.middleware("http")
# async def after_request(request: Request, call_next):
#     response = await call_next(request)
#     # Execute some code after each request
#     print("##### After request #####")
#     print(f"Fast API state {app.state.requestId}")
#     return response

@app.get("/")
async def read_root():
    logger.warning("/ API function.")
    return {"Hello": "World"}

@app.get("/health")
async def health_check():
    logger.warning("Health API function.")
    return {"status": "ok"}

# @app.get("/api/v1/health")
# async def health_check():
#     print("Health API function.")
#     return {"status": "ok"}

# @app.get("/api/v1/health/{id}")
# async def health_check(id: str):
#     print("Health API function.")
#     return {"status": "ok"}

# def reverse_string(s):
#     return s[::-1]

if __name__ == '__main__':
    uvicorn.run("fast-api-runner:app", host="0.0.0.0",  port=8000, reload=True, workers=1)