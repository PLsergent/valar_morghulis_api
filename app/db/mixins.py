from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import UUID


class UUIDPKMixin:
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default=text("gen_random_uuid()"),
    )
