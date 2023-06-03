from fastapi import FastAPI

from .database import create_tables
from .routers import routers

app = FastAPI()

app.include_router(routers.router)

create_tables()
