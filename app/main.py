import uvicorn
from fastapi import FastAPI

from app.config import settings

app = FastAPI(title=settings.APP_NAME.capitalize(), debug=settings.DEBUG)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
