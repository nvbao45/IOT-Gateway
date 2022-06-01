from apps import db
from sqlalchemy.sql import func
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Charts(db.Model):
    __tablename__ = 'charts'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    device_id: int = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    sensor: str = db.Column(db.String(20), nullable=False)
    samples: int = db.Column(db.Integer, nullable=False)
    size: int = db.Column(db.Integer, nullable=False)
    type: str = db.Column(db.String(50), nullable=False)
    color: str = db.Column(db.String(10), nullable=False)
    enable: bool = db.Column(db.Boolean, nullable=False)
    created_at: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    owner: str = db.Column(db.String(255), nullable=False)
    flag: int = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return '<Charts %r>' % self.id
