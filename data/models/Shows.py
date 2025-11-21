"""
this file create a model for the Shows table
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from ..db.base import Base

class Shows(Base):
    __tablename__ = "shows"
    show_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)