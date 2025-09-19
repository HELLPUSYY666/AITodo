import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.routers import main_router

app = FastAPI(title=settings.APP_NAME.capitalize(), debug=settings.DEBUG)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
