from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

Base = declarative_base()


class LocalLandCharge(Base):
    __tablename__ = 'local_land_charge'

    id = Column(BigInteger, primary_key=True)
    geometry = relationship('GeometryFeature', backref='local_land_charge',
                            cascade="all, delete-orphan")
    type = Column(String, nullable=False)
    llc_item = Column(JSONB, nullable=False)
    cancelled = Column(Boolean, nullable=False)
    further_information_reference = Column(String, nullable=True)

    def __init__(self, id, type, llc_item, cancelled, further_information_reference):
        self.id = id
        self.type = type
        self.llc_item = llc_item
        self.cancelled = cancelled
        self.further_information_reference = further_information_reference


class LocalLandChargeHistory(Base):
    __tablename__ = 'local_land_charge_history'

    id = Column(BigInteger, primary_key=True)
    llc_item = Column(JSONB, nullable=False)
    cancelled = Column(Boolean, nullable=False)
    entry_number = Column(BigInteger, primary_key=True, index=True)
    entry_timestamp = Column(DateTime, nullable=False)
    item_changes = Column(JSONB)

    def __init__(self, id, llc_item, cancelled, entry_number, entry_timestamp, item_changes=None):
        self.id = id
        self.llc_item = llc_item
        self.cancelled = cancelled
        self.entry_number = entry_number
        self.entry_timestamp = entry_timestamp
        self.item_changes = item_changes


class GeometryFeature(Base):
    __tablename__ = 'geometry_feature'

    id = Column(BigInteger, primary_key=True)
    local_land_charge_id = Column(BigInteger, ForeignKey('local_land_charge.id'), primary_key=True)
    geometry = Column(Geometry(srid=27700), nullable=False)

    def __init__(self, geometry, geometry_id):
        self.geometry = geometry
        self.id = geometry_id
