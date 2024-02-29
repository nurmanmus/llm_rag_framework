import logging.config
import os

import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .config import app_configs, settings
from .middlewares.route_logger.middleware import RouteLoggerMiddleware

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)
app.add_middleware(RouteLoggerMiddleware)

logging.config.fileConfig(f"{os.path.dirname(__file__)}/logging.conf")

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
