"""SQLAlchemy model for the ideal functions dataset."""
from sqlalchemy import Column, Float

from entities.schema import Base


class IdealFunctions(Base):
    """Ideal-function table: x plus y1 to y50 (51 columns)."""
    __tablename__ = 'ideal_functions'
    x = Column(Float, primary_key=True)


for i in range(1, 51):
    setattr(IdealFunctions, f'y{i}', Column(Float, nullable=False))