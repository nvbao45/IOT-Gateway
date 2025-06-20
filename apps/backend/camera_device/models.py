from apps import db
from sqlalchemy.sql import func
from sqlalchemy import Integer, ForeignKey, String, Column, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dataclasses import dataclass
import datetime

@dataclass
class CameraDevices(db.Model):
    __tablename__ = 'camera_devices'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.String(500), nullable=True)
    protocol: str = db.Column(db.String(255), nullable=True)
    port: int = db.Column(db.Integer, nullable=True)
    uri: str = db.Column(db.String(255), nullable=True)
    ip_address: str = db.Column(db.String(255), nullable=True)
    username: str = db.Column(db.String(255), nullable=True)
    password: str = db.Column(db.String(255), nullable=True)
    stream_path: str = db.Column(db.String(255), nullable=True)

    flag: int = db.Column(db.Integer, nullable=False, default=1)
    owner: str = db.Column(db.String(255), nullable=False)
    created_at: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return '<CameraDevices %r>' % self.id