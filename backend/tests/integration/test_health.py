"""Slice 1 cases. See 04.1-api-skeleton.md section 7."""

from httpx import AsyncClient

from app.main import PROCESS_TIME_HEADER, REQUEST_ID_HEADER


async def test_health_returns_ok(client: AsyncClient) -> None:
    """T-1.1: GET /health returns 200 and {"status": "ok"}."""
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_graphql_answers_introspection(client: AsyncClient) -> None:
    """T-1.2: POST /graphql answers an introspection query."""
    response = await client.post(
        "/graphql", json={"query": "{ __schema { queryType { name } } }"}
    )

    assert response.status_code == 200
    assert response.json()["data"]["__schema"]["queryType"]["name"] == "Query"


async def test_response_carries_timing_and_request_id(client: AsyncClient) -> None:
    """T-1.7: every response carries the timing header the middleware sets."""
    response = await client.get("/health")

    assert PROCESS_TIME_HEADER in response.headers
    assert float(response.headers[PROCESS_TIME_HEADER]) >= 0
    assert REQUEST_ID_HEADER in response.headers


async def test_supplied_request_id_is_echoed(client: AsyncClient) -> None:
    """A caller's request id survives, so a trace can be followed across systems."""
    response = await client.get("/health", headers={REQUEST_ID_HEADER: "abc-123"})

    assert response.headers[REQUEST_ID_HEADER] == "abc-123"


async def test_lifespan_populates_application_state() -> None:
    """The lifespan must open the pool.

    Added after a silent edit left the lifespan without it. The other tests did
    not catch it, because the client fixture sets app.state by hand and so
    papered over a server that could not serve a single GraphQL request.
    """
    from app.core.settings import get_settings
    from app.main import create_app, lifespan

    app = create_app(get_settings())
    async with lifespan(app):
        assert hasattr(app.state, "engine"), "lifespan did not create the engine"
        assert hasattr(app.state, "session_factory"), (
            "lifespan did not create the session factory"
        )
