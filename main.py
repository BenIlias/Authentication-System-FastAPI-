from fastapi import FastAPI
from database import create_tables
from Auth.routes import router


create_tables()

app = FastAPI()


app.include_router(router)