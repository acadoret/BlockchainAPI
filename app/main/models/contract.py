import json
from datetime import datetime

from sqlalchemy.ext.declarative import DeclarativeMeta

from .. import db


class Contract(db.Model):
    __tablename__ = "contracts"
    
    address = db.Column(db.String(42), primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(512))
    end_date = db.Column(db.DateTime, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.address'))
    user = db.relationship("User", back_populates="contract_ids")
    
    def __repr__(self):
        return "<Contract '{}' -> {}>".format(self.address, self.name)

    @property
    def registered_on(self):
        return self.registered_on

    @registered_on.setter
    def registered_on(self, _date):
        self.end_date = datetime.utcnow()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# A specialised JSONEncoder that encodes User
# objects as JSON
class ContractEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and 'password' not in x]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
