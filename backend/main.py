from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.config_variables import settings
from .database import Base, engine
from .model import Category, Game
from .routes import routes_category, routes_game


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(routes_category.router)
app.include_router(routes_game.router)