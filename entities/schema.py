"""Shared SQLAlchemy metadata and auxiliary table definitions."""
from sqlalchemy import Column, Float, String, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()

test_data_table = Table(
    'test_data', Base.metadata,
    Column('x', Float, nullable=False),
    Column('y', Float, nullable=False),
)

mapped_test_data_table = Table(
    'mapped_test_data', Base.metadata,
    Column('x', Float, nullable=False),
    Column('y', Float, nullable=False),
    Column('delta_y', Float, nullable=False),
    Column('ideal_func_no', String, nullable=False),
)