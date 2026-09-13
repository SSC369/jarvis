"""Settings end to end: schema, auth, resolver, interactor, repository, RLS."""

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from httpx import AsyncClient

from app.core import auth as auth_module
from app.core.settings import Settings

ALGORITHM = "ES256"


@pytest.fixture
def signing_key() -> ec.EllipticCurvePrivateKey:
    return ec.generate_private_key(ec.SECP256R1())


@pytest.fixture
def patched_jwks(
    monkeypatch: pytest.MonkeyPatch, signing_key: ec.EllipticCurvePrivateKey
) -> None:
    class FakeKey:
        key = signing_key.public_key()

    class FakeClient:
        def get_signing_key_from_jwt(self, _token: str) -> FakeKey:
            return FakeKey()

    monkeypatch.setattr(auth_module, "_get_jwks_client", lambda _s: FakeClient())


def _token(
    key: ec.EllipticCurvePrivateKey, settings: Settings, *, user_id: uuid.UUID
) -> str:
    claims: dict[str, Any] = {
        "sub": str(user_id),
        "iss": settings.jwt_issuer,
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }
    return jwt.encode(claims, key, algorithm=ALGORITHM)


async def test_settings_creates_a_row_with_the_detected_timezone(
    client: AsyncClient,
    signing_key: ec.EllipticCurvePrivateKey,
    patched_jwks: None,
    settings: Settings,
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-2.10."""
    user_a, _user_b = two_users
    token = _token(signing_key, settings, user_id=user_a)

    response = await client.post(
        "/graphql",
        json={
            "query": (
                "query($tz: String) { settings(detectedTimezone: $tz) { timezone } }"
            ),
            "variables": {"tz": "Asia/Kolkata"},
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    body = response.json()

    assert response.status_code == 200, body
    assert body["data"]["settings"] == {"timezone": "Asia/Kolkata"}


async def test_settings_second_call_returns_the_same_row(
    client: AsyncClient,
    signing_key: ec.EllipticCurvePrivateKey,
    patched_jwks: None,
    settings: Settings,
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-2.10."""
    user_a, _user_b = two_users
    token = _token(signing_key, settings, user_id=user_a)
    headers = {"Authorization": f"Bearer {token}"}
    query = "query($tz: String) { settings(detectedTimezone: $tz) { timezone } }"

    first = await client.post(
        "/graphql",
        json={"query": query, "variables": {"tz": "Asia/Kolkata"}},
        headers=headers,
    )
    second = await client.post(
        "/graphql",
        json={"query": query, "variables": {"tz": "America/New_York"}},
        headers=headers,
    )

    assert first.json()["data"]["settings"]["timezone"] == "Asia/Kolkata"
    assert second.json()["data"]["settings"]["timezone"] == "Asia/Kolkata"


async def test_update_timezone_changes_the_value(
    client: AsyncClient,
    signing_key: ec.EllipticCurvePrivateKey,
    patched_jwks: None,
    settings: Settings,
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    user_a, _user_b = two_users
    token = _token(signing_key, settings, user_id=user_a)

    response = await client.post(
        "/graphql",
        json={
            "query": (
                "mutation($input: UpdateTimezoneInput!) "
                "{ updateTimezone(input: $input) "
                "{ __typename ... on Settings { timezone } } }"
            ),
            "variables": {"input": {"timezone": "Europe/London"}},
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    body = response.json()

    assert body["data"]["updateTimezone"] == {
        "__typename": "Settings",
        "timezone": "Europe/London",
    }


async def test_update_timezone_with_an_invalid_zone_is_refused(
    client: AsyncClient,
    signing_key: ec.EllipticCurvePrivateKey,
    patched_jwks: None,
    settings: Settings,
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-2.12."""
    user_a, _user_b = two_users
    token = _token(signing_key, settings, user_id=user_a)

    response = await client.post(
        "/graphql",
        json={
            "query": (
                "mutation($input: UpdateTimezoneInput!) "
                "{ updateTimezone(input: $input) { __typename } }"
            ),
            "variables": {"input": {"timezone": "not/a/zone"}},
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    body = response.json()

    assert body["data"]["updateTimezone"]["__typename"] == "InvalidTimezone"


async def test_user_a_and_user_b_each_get_their_own_settings_row(
    client: AsyncClient,
    signing_key: ec.EllipticCurvePrivateKey,
    patched_jwks: None,
    settings: Settings,
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-2.13, rule T7."""
    user_a, user_b = two_users
    query = "query($tz: String) { settings(detectedTimezone: $tz) { timezone } }"

    token_a = _token(signing_key, settings, user_id=user_a)
    await client.post(
        "/graphql",
        json={"query": query, "variables": {"tz": "Asia/Kolkata"}},
        headers={"Authorization": f"Bearer {token_a}"},
    )

    token_b = _token(signing_key, settings, user_id=user_b)
    response_b = await client.post(
        "/graphql",
        json={"query": query, "variables": {"tz": "Pacific/Auckland"}},
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert response_b.json()["data"]["settings"] == {"timezone": "Pacific/Auckland"}
