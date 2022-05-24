from apps import db
from sqlalchemy.sql import func
from sqlalchemy import Integer, ForeignKey, String, Column, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Devices(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(255), nullable=False)
    device_description = db.Column(db.String(500), nullable=False)
    device_token = db.Column(db.String(255), nullable=False)
    device_created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    device_owner = db.Column(db.String(255), nullable=False)
    request_count = db.Column(db.Integer, nullable=False, default=0)


    def __repr__(self):
        return '<Devices %r>' % self.id

