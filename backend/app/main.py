"""The FastAPI application.

Composition happens here and nowhere else: settings are read, logging is
configured, and the GraphQL router is mounted.
"""

import time
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter

from app.core.context import Context
from app.core.db import check_connection, create_engine, create_session_factory
from app.core.deps import build_context
from app.core.logging import configure_logging
from app.core.settings import Settings, get_settings
from app.graphql.schema import schema

REQUEST_ID_HEADER = "X-Request-ID"
PROCESS_TIME_HEADER = "X-Process-Time-Ms"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Configure logging and open the connection pool, from validated settings.

    The engine and session factory live on ``app.state`` because they outlive a
    request and must be shared. Creating an engine per request would open a new
    pool per request, which is the opposite of pooling.
    """
    settings = get_settings()
    configure_logging(
        log_level=settings.log_level,
        secrets=settings.secret_values(),
        json_output=settings.environment != "local",
    )
    engine = create_engine(settings)
    app.state.engine = engine
    app.state.session_factory = create_session_factory(engine)
    structlog.get_logger().info("application.started", environment=settings.environment)
    try:
        yield
    finally:
        await engine.dispose()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the application. Tests call this directly with their own settings."""
    settings = settings or get_settings()

    app = FastAPI(
        title="Slashit API",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if settings.environment == "local" else None,
        redoc_url=None,
    )

    if settings.environment == "local":
        # The Vite dev server's own origin. No production origin is set here;
        # that is a deploy-time decision for whichever host serves the built
        # frontend, not a local default.
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                # vite preview's default port, used for PWA verification —
                # a production service worker only registers against a real
                # build, not the dev server.
                "http://localhost:4173",
                "http://127.0.0.1:4173",
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.middleware("http")
    async def request_context(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Attach a request id and measure how long the handler took.

        The timing header is what NFR-2 will be measured against once the
        gateway exists to measure.
        """
        request_id = request.headers.get(REQUEST_ID_HEADER, str(uuid.uuid4()))
        structlog.contextvars.bind_contextvars(request_id=request_id)
        started = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            structlog.contextvars.unbind_contextvars("request_id")
        elapsed_ms = (time.perf_counter() - started) * 1000
        response.headers[REQUEST_ID_HEADER] = request_id
        response.headers[PROCESS_TIME_HEADER] = f"{elapsed_ms:.2f}"
        return response

    @app.exception_handler(Exception)
    async def unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
        """Return a request id and nothing else.

        The traceback goes to the log, which runs through the redactor. It never
        goes to the client, because FR-2 forbids a credential reaching a client
        in an error body and a traceback is how that happens.
        """
        request_id = request.headers.get(REQUEST_ID_HEADER, "unknown")
        structlog.get_logger().exception("request.unhandled_error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "request_id": request_id},
        )

    @app.get("/health", tags=["ops"])
    async def health() -> dict[str, str]:
        """Liveness. Answers while starting and while the database is down."""
        return {"status": "ok"}

    @app.get("/ready", tags=["ops"])
    async def ready(response: Response) -> dict[str, str]:
        """Readiness. Reports whether the database is actually reachable.

        Separate from liveness on purpose: a database outage should not make an
        orchestrator kill a healthy process, it should take it out of rotation.
        """
        engine = getattr(app.state, "engine", None)
        database_ok = engine is not None and await check_connection(engine)
        if not database_ok:
            response.status_code = 503
            return {"status": "unavailable", "database": "unreachable"}
        return {"status": "ok", "database": "ok"}

    async def get_context(request: Request) -> Context:
        return await build_context(
            authorization_header=request.headers.get("Authorization"),
            request_id=request.headers.get(REQUEST_ID_HEADER, "unknown"),
            session_factory=request.app.state.session_factory,
            settings=settings,
        )

    app.include_router(
        GraphQLRouter(schema, context_getter=get_context), prefix="/graphql"
    )

    return app


app = create_app()
