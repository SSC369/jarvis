"""captureHistory end to end: schema, auth, resolver, interactor, repository,
RLS. Uses "/add-task" with no arguments, which asks a pending question without
calling the vendor, so this costs nothing to run. 04.4 sub-plan, T-4.8.
"""

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


HISTORY_QUERY = (
    "query($cursor: String) { captureHistory(cursor: $cursor) { "
    "nextCursor items { inputText outcome questionText answerText } } }"
)


async def test_a_question_asked_turn_appears_in_history(
    client: AsyncClient,
    signing_key: ec.EllipticCurvePrivateKey,
    patched_jwks: None,
    settings: Settings,
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    user_a, _user_b = two_users
    token = _token(signing_key, settings, user_id=user_a)
    headers = {"Authorization": f"Bearer {token}"}

    await client.post(
        "/graphql",
        json={
            "query": 'mutation { submitCapture(rawInput: "/add-task") { __typename } }'
        },
        headers=headers,
    )

    response = await client.post(
        "/graphql", json={"query": HISTORY_QUERY, "variables": {}}, headers=headers
    )
    body = response.json()

    assert response.status_code == 200, body
    items = body["data"]["captureHistory"]["items"]
    assert len(items) == 1
    assert items[0]["inputText"] == "/add-task"
    assert items[0]["outcome"] == "QUESTION_ASKED"
    assert items[0]["questionText"] == "What should the task be called?"
    assert items[0]["answerText"] is None


async def test_user_a_never_sees_user_bs_history(
    client: AsyncClient,
    signing_key: ec.EllipticCurvePrivateKey,
    patched_jwks: None,
    settings: Settings,
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """Rule T7."""
    user_a, user_b = two_users
    token_a = _token(signing_key, settings, user_id=user_a)
    token_b = _token(signing_key, settings, user_id=user_b)

    await client.post(
        "/graphql",
        json={
            "query": 'mutation { submitCapture(rawInput: "/add-task") { __typename } }'
        },
        headers={"Authorization": f"Bearer {token_b}"},
    )

    response = await client.post(
        "/graphql",
        json={"query": HISTORY_QUERY, "variables": {}},
        headers={"Authorization": f"Bearer {token_a}"},
    )

    assert response.json()["data"]["captureHistory"]["items"] == []


async def test_capture_history_refuses_without_a_token(client: AsyncClient) -> None:
    response = await client.post(
        "/graphql", json={"query": HISTORY_QUERY, "variables": {}}
    )
    body = response.json()

    assert body.get("errors")
    assert "Not authenticated" in str(body["errors"])
