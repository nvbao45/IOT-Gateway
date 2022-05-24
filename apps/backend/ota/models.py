from apps import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(255), nullable=False)
    image_file = db.Column(db.String(255), nullable=False)
    image_description = db.Column(db.String(500), nullable=False)
    image_version = db.Column(db.String(50), nullable=False)
    image_size = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    image_created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    image_owner = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Images %r>' % self.id