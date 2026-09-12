"""Token verification cases. See 04.2 section 8.

Tokens are minted locally with a throwaway EC key and the JWKS client is
monkeypatched, so these run without the network and without a real Supabase
session. What they exercise is our verification logic, which is the part we own.
"""

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import ec

from app.core import auth as auth_module
from app.core.auth import extract_bearer_token, verify_token
from app.core.errors import AuthenticationError
from app.core.settings import Settings

ALGORITHM = "ES256"


@pytest.fixture
def signing_key() -> ec.EllipticCurvePrivateKey:
    return ec.generate_private_key(ec.SECP256R1())


@pytest.fixture
def patched_jwks(
    monkeypatch: pytest.MonkeyPatch, signing_key: ec.EllipticCurvePrivateKey
) -> None:
    """Serve the matching public key instead of fetching Supabase's JWKS."""

    class FakeKey:
        key = signing_key.public_key()

    class FakeClient:
        def get_signing_key_from_jwt(self, _token: str) -> FakeKey:
            return FakeKey()

    monkeypatch.setattr(auth_module, "_get_jwks_client", lambda _s: FakeClient())


def _token(
    key: ec.EllipticCurvePrivateKey,
    settings: Settings,
    *,
    sub: str | None = None,
    issuer: str | None = None,
    expires_in: timedelta = timedelta(hours=1),
) -> str:
    claims: dict[str, Any] = {
        "sub": sub if sub is not None else str(uuid.uuid4()),
        "iss": issuer if issuer is not None else settings.jwt_issuer,
        "exp": datetime.now(UTC) + expires_in,
    }
    return jwt.encode(claims, key, algorithm=ALGORITHM)


def test_valid_token_returns_the_subject(
    signing_key: ec.EllipticCurvePrivateKey, patched_jwks: None, settings: Settings
) -> None:
    """T-2.4."""
    user_id = uuid.uuid4()
    token = _token(signing_key, settings, sub=str(user_id))

    assert verify_token(token, settings) == user_id


def test_token_signed_by_another_key_is_rejected(
    patched_jwks: None, settings: Settings
) -> None:
    """T-2.1."""
    attacker_key = ec.generate_private_key(ec.SECP256R1())
    token = _token(attacker_key, settings)

    with pytest.raises(AuthenticationError):
        verify_token(token, settings)


def test_expired_token_is_rejected(
    signing_key: ec.EllipticCurvePrivateKey, patched_jwks: None, settings: Settings
) -> None:
    """T-2.2."""
    token = _token(signing_key, settings, expires_in=timedelta(seconds=-30))

    with pytest.raises(AuthenticationError):
        verify_token(token, settings)


def test_wrong_issuer_is_rejected(
    signing_key: ec.EllipticCurvePrivateKey, patched_jwks: None, settings: Settings
) -> None:
    """T-2.3: a token from another Supabase project must not be accepted."""
    token = _token(
        signing_key, settings, issuer="https://someone-else.supabase.co/auth/v1"
    )

    with pytest.raises(AuthenticationError):
        verify_token(token, settings)


def test_non_uuid_subject_is_rejected(
    signing_key: ec.EllipticCurvePrivateKey, patched_jwks: None, settings: Settings
) -> None:
    """A subject that is not a uuid cannot become a user id."""
    token = _token(signing_key, settings, sub="not-a-uuid")

    with pytest.raises(AuthenticationError):
        verify_token(token, settings)


def test_failures_are_indistinguishable(
    signing_key: ec.EllipticCurvePrivateKey, patched_jwks: None, settings: Settings
) -> None:
    """Expiry and forgery must produce the same message.

    Telling a caller which check failed tells them which half of a forged token
    to fix.
    """
    expired = _token(signing_key, settings, expires_in=timedelta(seconds=-30))
    forged = _token(ec.generate_private_key(ec.SECP256R1()), settings)

    messages = set()
    for token in (expired, forged):
        try:
            verify_token(token, settings)
        except AuthenticationError as exc:
            messages.add(str(exc))

    assert len(messages) == 1, f"failure messages differ: {messages}"


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Bearer abc.def.ghi", "abc.def.ghi"),
        ("bearer abc", None),
        ("abc.def.ghi", None),
        ("Bearer ", None),
        ("", None),
        (None, None),
    ],
)
def test_bearer_extraction(header: str | None, expected: str | None) -> None:
    assert extract_bearer_token(header) == expected
