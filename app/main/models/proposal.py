class Proposal:
    name, address = ""
    vote_count = 0
    is_winning = False

    def __init__(self, _name, _address):
        self.name = _name
        self.address = _address

    def __repr__(self):
        return "<Proposal '{}' -> {}>".format(self.address, self.name)
