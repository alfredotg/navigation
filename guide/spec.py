from fastapi.openapi.utils import get_openapi
from main import app
import yaml 

if "__main__" == __name__:
    with open('openapi.yaml', 'w') as f:
        yaml.dump(get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes
        ), f)
