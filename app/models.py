from sqlalchemy import Column, String, Integer
from app.database import Base


class Link(Base):
    __tablename__ = "links"

    code = Column(String, primary_key=True, index=True)
    url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)