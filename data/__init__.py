"""
this package give access to all data used in the project (like the database connection instance)
"""

from .db import db
from .kafka import load_to_kafka
from .models import Reviews, Shows