from sqlalchemy import Column, Integer, String, PickleType
from .sessions import Base


class Country(Base):
    __tablename__ = "Polygon"

    ogc_fid = Column(Integer, primary_key=True, index=True)
    admin = Column(String, unique=True)
    iso_a3 = Column(String)
    geom = Column(PickleType)
