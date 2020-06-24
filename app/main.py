import uvicorn
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import api_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.include_router(api_router)
app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

