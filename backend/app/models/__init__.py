"""The declarative base every domain's tables share.

Alembic's autogenerate needs one place to find metadata. Each domain defines its
own tables against this base and imports nothing from another domain's models.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base."""
