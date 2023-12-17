import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import declarative_base
import apps.main.views.router as main_router
from apps.database.db_connect import DBConnect
from apps.model.main import Model

Base = declarative_base()

app = FastAPI()
model = Model()
query = DBConnect()
main_router.init(app)