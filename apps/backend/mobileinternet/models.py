from apps import db


class SerialConfig(db.Model):
    __tablename__ = 'serial_config'

    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.String(255), nullable=False)
    baudrate = db.Column(db.Integer, nullable=False)
    timeout = db.Column(db.Integer, nullable=False)
    apn = db.Column(db.String(255), nullable=False)
    apn_user = db.Column(db.String(255), nullable=True)
    apn_pwd = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<SerialConfig %r>' % self.port
