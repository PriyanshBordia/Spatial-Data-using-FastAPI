from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String

from .sessions import Base


class Country(Base):
	__tablename__ = "Polygon"

	id = Column(Integer, primary_key=True)
	admin = Column(String, unique=True)
	iso_a3 = Column(String)
	geom = Column(PickleType)
