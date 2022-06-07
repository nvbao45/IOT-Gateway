from apps import sock, db
from flask_login import login_required
from apps.backend.ws.models import LastData, SensorParser
from sqlalchemy import desc
import time
import json


@login_required
@sock.route('/chart/data/<int:device_id>/<string:sensor>/<int:limit>')
def chart_data(ws, device_id, sensor, limit):
    while True:
        _data = None
        _data = SensorParser.query.with_entities(SensorParser.value, SensorParser.timestamp)\
            .filter_by(sensor=sensor, device_id=device_id) \
            .order_by(desc(SensorParser.timestamp)).limit(limit).all()
        data = [x[0] for x in _data]
        timestamp = [x[1].strftime("%m/%d/%Y-%H:%M:%S") for x in _data]
        data.reverse()
        timestamp.reverse()

        db.session.commit()

        ws.send(json.dumps(dict(
            device_id=device_id,
            sensor=sensor,
            limit=limit,
            data=data,
            timestamp=timestamp
        )))

        time.sleep(1)
