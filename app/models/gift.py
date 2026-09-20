from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GiftRequestModel(Base):
    __tablename__ = "gift_requests"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    budget: Mapped[int] = mapped_column(
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(2000),
        nullable=False
    )
