from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, index=True)
    developer = Column(String(120), nullable=False)
    release_year = Column(Integer, nullable=False)
    # price = Column(Float, nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    category = relationship(
        "Category",
        back_populates="games"
    )