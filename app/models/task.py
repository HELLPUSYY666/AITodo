import enum
from typing import Optional

from sqlalchemy import Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class StatusEnum(enum.Enum):
    done = "done"
    pending = "pending"
    reject = "reject"


class PriorityEnum(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    tasks = relationship("Task", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum, name="status_enum", native_enum=False),
        default=StatusEnum.pending,
    )
    priority: Mapped[PriorityEnum] = mapped_column(
        Enum(PriorityEnum, name="priority_enum", native_enum=False),
        default=PriorityEnum.medium,
    )
    due_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    user = relationship("User", back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, status={self.status!r}, priority={self.priority!r})"
