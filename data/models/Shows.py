"""
this file create a model for the Shows table
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from ..db.base import Base

class Shows(Base):
    __tablename__ = "shows"
    show_id = Column(String, primary_key=True, index=True)
    name = Column(String)