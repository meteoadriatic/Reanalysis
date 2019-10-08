# -*- coding: utf-8 -*-

from reanalysis.database import ExtendedModel
from sqlalchemy import Column, DateTime, Float, ForeignKey, LargeBinary
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, VARCHAR
from sqlalchemy.orm import relationship

metadata = ExtendedModel.metadata


class Location(ExtendedModel):
    __tablename__ = 'locations'

    name = Column(VARCHAR(45), primary_key=True)
    latitude = Column(Float(6), nullable=False)
    longitude = Column(Float(7), nullable=False)
    height = Column(INTEGER(4), nullable=False)


class Model(ExtendedModel):
    __tablename__ = 'models'

    name = Column(VARCHAR(45), primary_key=True)
    description = Column(MEDIUMTEXT)
    namelist_input = Column('namelist.input', LargeBinary)
    namelist_wps = Column('namelist.wps', LargeBinary)


class ModelOutput(ExtendedModel):
    __tablename__ = 'model_output'

    id = Column(INTEGER(11), primary_key=True)
    model = Column(ForeignKey('models.name', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    location = Column(ForeignKey('locations.name', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    datetime = Column(DateTime, nullable=False, index=True)
    TMP_2 = Column(INTEGER(2))
    DPT_2 = Column(INTEGER(2))
    RH_2 = Column(INTEGER(3))
    RH_700 = Column(INTEGER(3))
    MSLET_SF = Column(INTEGER(4))
    TMP_850 = Column(INTEGER(2))
    CAPE_180 = Column(INTEGER(5))
    CIN_180 = Column(INTEGER(4))
    PWAT_CLM = Column(INTEGER(3))
    UGRD_10 = Column(INTEGER(2))
    VGRD_10 = Column(INTEGER(2))
    UGRD_850 = Column(INTEGER(2))
    VGRD_850 = Column(INTEGER(2))
    UGRD_500 = Column(INTEGER(3))
    VGRD_500 = Column(INTEGER(3))
    UGRD_300 = Column(INTEGER(3))
    VGRD_300 = Column(INTEGER(3))
    GUST_SF = Column(INTEGER(2))
    HGT_0C = Column(INTEGER(4))
    TMP_500 = Column(INTEGER(2))
    HGT_850 = Column(INTEGER(4))
    HGT_500 = Column(INTEGER(4))
    VVEL_900 = Column(Float(3))
    VVEL_700 = Column(Float(3))
    SNOD_SF = Column(INTEGER(3))
    TMP_1000 = Column(INTEGER(2))
    HGT_1000 = Column(INTEGER(4))
    DSWRF_SF = Column(INTEGER(4))
    DLWRF_SF = Column(INTEGER(4))
    USWRF_SF = Column(INTEGER(4))
    ULWRF_SF = Column(INTEGER(4))
    TMP_SF = Column(INTEGER(4))
    rdrmax = Column(INTEGER(2))
    cldave = Column(INTEGER(3))
    precave = Column(Float(4))
    precpct = Column(INTEGER(3))

    location1 = relationship('Location')
    model1 = relationship('Model')
