from fastapi import FastAPI
from server import router

app = FastAPI(title = "FirstAPI")

app.include_router(router)

