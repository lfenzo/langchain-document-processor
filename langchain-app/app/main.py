from fastapi import FastAPI

from app.routers.process import router as processing_router
from app.routers.feedback import router as feedback_router

app = FastAPI()

app.include_router(processing_router)
app.include_router(feedback_router)
