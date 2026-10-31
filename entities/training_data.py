"""SQLAlchemy model for the training dataset."""
from sqlalchemy import Column, Float

from entities.schema import Base


class TrainingData(Base):
    """Training table: x plus the four training functions (5 columns)."""
    __tablename__ = 'training_data'
    x = Column(Float, primary_key=True)
    y1 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    y3 = Column(Float, nullable=False)
    y4 = Column(Float, nullable=False)