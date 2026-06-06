from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import Base, engine
from app.routers import auth, profile, match, interaction, activity, matchmaker
from app.init_data import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    init_database()
    yield


app = FastAPI(title="相亲平台 API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(match.router)
app.include_router(interaction.router)
app.include_router(activity.router)
app.include_router(matchmaker.router)


@app.get("/")
def root():
    return {"message": "相亲平台 API 运行中"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
