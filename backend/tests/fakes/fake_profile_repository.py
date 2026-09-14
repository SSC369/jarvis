"""An in-memory ProfileRepository. Not a mock: it behaves, so tests read as
behaviour."""

from uuid import UUID

from app.domains.identity.interfaces.dtos import ProfileDTO


class FakeProfileRepository:
    """Satisfies identity's ProfileRepository Protocol without inheriting
    from it."""

    def __init__(self) -> None:
        self.rows: dict[UUID, ProfileDTO] = {}

    async def get_for_user(self, *, user_id: UUID) -> ProfileDTO | None:
        return self.rows.get(user_id)
