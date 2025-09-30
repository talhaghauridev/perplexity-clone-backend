import uuid
from typing import Annotated

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    """Modern SQLAlchemy 2.0 Base class with type mapping"""

    type_annotation_map = {
        str: String(255),
    }


UUIDPk = Annotated[
    str, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
]
UUIDFk = Annotated[str, UUID(as_uuid=True)]
