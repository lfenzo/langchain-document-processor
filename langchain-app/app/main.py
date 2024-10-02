from fastapi import FastAPI

from app.routers.process import router as processing_router

app = FastAPI()

app.include_router(processing_router)
