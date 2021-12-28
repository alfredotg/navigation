from app.env import load_dotenv

load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, status, Form, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from os import environ
from jose import JWTError, jwt
import base64
from typing import Optional, List

from guide import Client as GuideClient
from users import Client as UsersClient
from navigator import Client as NavigatorClient
from navigator.models.route import Route as NavigatorRoute 

from app import schemas
from app import navigator, guide, users as api_users

PUBLIC_KEY = base64.b64decode(environ.get("JWT_PUBLIC"))
ALGORITHM = environ.get("JWT_ALGORITHM")

users_client = UsersClient(base_url=environ.get("USERS_API_URL"))
navigator_client = NavigatorClient(base_url=environ.get("NAVIGATOR_API_URL"))
guide_client = GuideClient(base_url=environ.get("GUIDE_API_URL"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def get_user_id(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") is None:
            return None
        try:
            user_id = int(payload.get("sub"))
            if user_id <= 0:
                return None
            return user_id
        except ValueError:
            return None
    except JWTError:
        return None

async def get_current_active_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    user_id = get_user_id(token)
    if user_id is None:
        raise credentials_exception
    return user_id 

@app.post(
    "/token", 
    operation_id="token",
    response_model=schemas.Token,
    description="Example: username: alice@gmail.com, password: test")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    token = await api_users.auth_by_password(users_client, form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return schemas.Token(access_token=token, token_type="bearer")

@app.get(
    "/users", 
    operation_id="users",
    response_model=schemas.Profiles)
async def users(_current_user_id: int = Depends(get_current_active_user_id)) -> schemas.Profiles:
    return schemas.Profiles(items=await api_users.find(users_client, None))

@app.get(
    "/points", 
    operation_id="points",
    response_model=schemas.Points)
async def points(_current_user_id: int = Depends(get_current_active_user_id)) -> schemas.Points:
    items = []
    for rpoint in await navigator.find_points(client=navigator_client):
        items.append(schemas.Point(uid=rpoint.uid, name=rpoint.name))
    return schemas.Points(items=items)

@app.post(
    "/route/make/{from_id}/{to_id}", 
    operation_id="makeRoute",
    response_model=schemas.MakeRouteResponse)
async def make_route(from_id: int, to_id: int, name: str = Form(...), current_user_id: int = Depends(get_current_active_user_id)) -> schemas.MakeRouteResponse:
    guide_response = await guide.make_route(guide_client, from_id, to_id)
    if guide_response is None:
        return schemas.MakeRouteResponse()
    
    route = NavigatorRoute(
        name=name,
        user_id=current_user_id,
        distance=guide_response.route.distance,
    )
    response = await navigator.save_route_raw(navigator_client, route, guide_response.route.points)
    return Response(content=response, media_type="application/json")

@app.get(
    "/routes", 
    operation_id="findRoutes",
    response_model=schemas.Routes)
async def find_routes(_current_user_id: int = Depends(get_current_active_user_id)) -> schemas.Routes:
    response = await navigator.find_routes_raw(navigator_client)
    return Response(content=response, media_type="application/json")

@app.get(
    "/routes/stats", 
    operation_id="getRoutesStats",
    response_model=schemas.RoutesStatsByUserList)
async def get_routes_stats(_current_user_id: int = Depends(get_current_active_user_id)) -> schemas.RoutesStatsByUserList:
    stats = await navigator.get_routes_stats(navigator_client)
    users_ids : List[int] = list(map(lambda record: record.user_id, stats.items))
    
    profiles = {} 
    if len(users_ids) > 0:
        for profile in await api_users.find(users_client, users_ids):
            profiles[profile.uid] = profile

    items = [] 
    for stat in stats.items:
        items.append(schemas.RoutesStatsByUser(
            user=profiles.get(stat.user_id, None),
            count=stat.count,
            distance=stat.distance
            ))

    return schemas.RoutesStatsByUserList(items=items)
