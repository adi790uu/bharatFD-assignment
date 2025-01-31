from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the server...")
    yield
    print("Closing the server...")


app = FastAPI(title="BharatFD", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to the server!"}
