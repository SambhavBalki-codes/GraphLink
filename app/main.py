from fastapi import FastAPI
from app.routes import users, friendships, recommendations

app = FastAPI(
    title="GraphLink",
    description="A graph-based friend recommendation engine",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(friendships.router)
app.include_router(recommendations.router)