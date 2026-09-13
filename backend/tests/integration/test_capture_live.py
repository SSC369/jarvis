"""End to end against the real gateway and the real database.

T-1.13 spends a fraction of a cent, the same as the gateway's own T-3.13.
Runs locally, not in CI, per 04.3 Q4's precedent.
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
    return jwt.encode(claims, key, algorithm="ES256")


@pytest.mark.live
async def test_add_task_end_to_end_returns_task_created(
    client: AsyncClient,
    signing_key: ec.EllipticCurvePrivateKey,
    patched_jwks: None,
    settings: Settings,
    two_users: tuple[uuid.UUID, uuid.UUID],
) -> None:
    """T-1.13: FR-4, FR-5. The whole stack, a real model call included."""
    user_a, _user_b = two_users
    token = _token(signing_key, settings, user_id=user_a)

    response = await client.post(
        "/graphql",
        json={
            "query": (
                "mutation($input: String!) { submitCapture(rawInput: $input) "
                "{ __typename ... on TaskCreated { task { title dueAt } } } }"
            ),
            "variables": {"input": "/add-task Finish the quarterly docs tomorrow"},
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    body = response.json()

    assert response.status_code == 200, body
    assert body["data"]["submitCapture"]["__typename"] == "TaskCreated", body
    task = body["data"]["submitCapture"]["task"]
    assert task["title"], "the model returned no title"
    assert task["dueAt"], "the model resolved no due date for 'tomorrow'"
