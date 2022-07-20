from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String

from ..app.config import settings
from .sessions import Base


class Country(Base):
    __tablename__ = settings.MODEL_NAME

    id = Column(Integer, primary_key=True)
    admin = Column(String, unique=True)
    iso_a3 = Column(String, unique=True)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))
