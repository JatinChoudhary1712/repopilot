from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Repository(Base):
    # Table name
    __tablename__ = "repositories"

    # Internal ID
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # GitHub ID
    github_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
    )

    # Repo name
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Full repo name
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Owner name
    owner: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Repo description
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Private/public
    private: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    # GitHub URL
    html_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # Default branch
    default_branch: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Main language
    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Creation time
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Update time
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Last push
    pushed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )