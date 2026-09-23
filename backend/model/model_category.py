from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    games = relationship(
        "Game",
        back_populates="category"
    )