from apps import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dataclasses import dataclass
import datetime


@dataclass
class Images(db.Model):
    __tablename__ = 'images'

    id: int = db.Column(db.Integer, primary_key=True)
    image_name: str = db.Column(db.String(255), nullable=False)
    image_file: str = db.Column(db.String(255), nullable=False)
    image_description: str = db.Column(db.String(500), nullable=False)
    image_version: str = db.Column(db.String(50), nullable=False)
    image_size: int = db.Column(db.Integer, nullable=False)
    image_url: str = db.Column(db.String(255), nullable=False)
    image_created_at: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    image_owner: str = db.Column(db.String(255), nullable=False)
    flag: int = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return '<Images %r>' % self.id