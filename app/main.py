import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.observability import metrics
from app.routes import friendships, recommendations, users

logger = logging.getLogger("graphlink.api")

app = FastAPI(
    title="GraphLink",
    description="A graph-based friend recommendation engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(friendships.router)
app.include_router(recommendations.router)


@app.middleware("http")
async def record_request_metrics(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - started) * 1000
    metrics.record_request(
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    logger.info(
        "request method=%s path=%s status=%s duration_ms=%.3f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response