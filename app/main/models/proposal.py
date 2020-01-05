class Proposal:
    name = ""
    vote_count = 0
    is_winning = False

    def __init__(self, _name):
        self.name = _name

    def __repr__(self):
        return "<Proposal -> {}>".format(self.name)
