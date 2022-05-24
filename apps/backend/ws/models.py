from sqlalchemy import UniqueConstraint, Constraint
from apps import db
from dataclasses import dataclass
from apps.backend.devices.models import Devices
import uuid
import re


@dataclass
class SensorParser(db.Model):
    __tablename__ = 'sensor_parser'
    id: int
    node_id: str
    node_name: str
    sensor: str
    value: float
    timestamp: str
    access_token: str
    gateway_id: str

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(50), nullable=False)
    node_name = db.Column(db.String(50), nullable=False)
    sensor = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    gateway_id = db.Column(db.String(255), default=':'.join(re.findall('..', '%012x' % uuid.getnode())), nullable=False)

    def __repr__(self):
        return str(self.node_name) + ' ' + str(self.sensor) + ' ' + str(self.value) + ' ' + str(self.timestamp)


class LastData(db.Model):
    __tablename__ = 'last_data'
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, nullable=False)
    node_name = db.Column(db.String(50), nullable=False)
    sensor = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    __table_args__ = (UniqueConstraint('node_id', 'node_name', 'sensor', 'timestamp', name='_node_sensor_timestamp_uc'),
                      )

    def __repr__(self):
        return str(self.node_name) + ' ' + str(self.sensor) + ' ' + str(self.value) + ' ' + str(self.timestamp)
