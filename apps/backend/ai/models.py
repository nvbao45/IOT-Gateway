from apps import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dataclasses import dataclass
import datetime


@dataclass
class AIModel(db.Model):
    __tablename__ = 'ai-models'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    file: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.String(500), nullable=False)
    version: str = db.Column(db.String(50), nullable=False)
    size: int = db.Column(db.Integer, nullable=False)
    url: str = db.Column(db.String(255), nullable=False)
    created_at: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    owner: str = db.Column(db.String(255), nullable=False)
    flag: int = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return '<Models %r>' % self.id