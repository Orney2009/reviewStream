"""
this file create a model for the Reviews table
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from ..db.base import Base

class Reviews(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    show_id = Column(Integer, ForeignKey("shows.show_id"), index=True)
    review = Column(String)
    label = Column(String)
    created_at = Column(Integer)