import logging
import time
from fastapi import FastAPI, Request
from app.routes import users, friendships, recommendations
from app.observability import metrics

logger = logging.getLogger("graphlink.api")

app = FastAPI(
    title="GraphLink",
    description="A graph-based friend recommendation engine",
    version="1.0.0"
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