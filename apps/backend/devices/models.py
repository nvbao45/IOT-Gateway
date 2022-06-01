from apps import db
from sqlalchemy.sql import func
from sqlalchemy import Integer, ForeignKey, String, Column, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dataclasses import dataclass
import datetime


@dataclass
class Devices(db.Model):
    __tablename__ = 'devices'

    id: int = db.Column(db.Integer, primary_key=True)
    device_name: str = db.Column(db.String(255), nullable=False)
    device_description: str = db.Column(db.String(500), nullable=False)
    device_token: str = db.Column(db.String(255), nullable=False)
    device_created_at: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    device_owner: str = db.Column(db.String(255), nullable=False)
    device_enable: bool = db.Column(db.Boolean(), nullable=False, default=True)
    request_count: int = db.Column(db.Integer, nullable=False, default=0)
    updated_at: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    flag: int = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return '<Devices %r>' % self.id

