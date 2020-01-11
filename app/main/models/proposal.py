import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class Proposal:
    name = ""
    index = 0
    vote_count = 0
    is_winning = False

    def __init__(self, name, index=0, vote_count=0):
        self.name = name
        self.vote_count = vote_count
        self.index = index

    def __repr__(self):
        return "<Proposal -> {}>".format(self.name)
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class ProposalEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
