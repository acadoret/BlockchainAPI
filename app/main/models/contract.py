from .. import db, flask_bcrypt

class Contract(db.Model):
    __tablename__ = "contracts"
    
    address = db.Column(db.String(42), primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(512))
    end_date = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.String, db.ForeignKey('users.address'))
    user = db.relationship("User", back_populates="contract_ids")
    
    def __repr__(self):
        return "<Contract '{}' -> {}>".format(self.address, self.name)
