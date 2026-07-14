import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda:str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    notifications = relationship("Notofication", back_populates="owner", cascade="all, delete-orphan")