from fastapi import FastAPI 
from app import schemas, storage
from fastapi.logger import logger

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.warning("storage initialization...")
    storage.init()
    logger.warning("storage is ready")

@app.get("/route/{from_id}/{to_id}", response_model=schemas.RouteResponse, operation_id="makeRoute")
def make_route(from_id: int, to_id: int) \
        -> schemas.RouteResponse:
    response = schemas.RouteResponse()
    try:
        route = storage.shortest_path(from_id, to_id)
        if route is None:
            return response
        response.route = route
    except ValueError as e:
        logger.error("routing error: %s", str(e))
    return response
