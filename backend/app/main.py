from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth_routes import router as auth_router
from app.api.uploads_routes import router as uploads_router
from app.core.config import settings
from app.db.session import Base, engine

# Import models to ensure they are registered with SQLAlchemy (under the hood),
# even though they are not directly used in this file.
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CommitMentIssues Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(uploads_router)


@app.get("/")
def root():
    return {"message": "Backend is running."}