import app
import json
import datetime

db = app.get_db()
c = db.cursor()
c.execute('DESCRIBE items;')
items = c.fetchall()
c.execute('DESCRIBE users;')
users = c.fetchall()

def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

with open('schema.json', 'w') as f:
    json.dump({'items': items, 'users': users}, f, default=json_serial)
