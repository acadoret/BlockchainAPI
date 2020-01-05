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
    
    """
    Not stored in DB
    """
    # Abi contains a single .sol contract compiled in JSON
    _abi = json.loads('[{"constant":false,"inputs":[{"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"addCandidate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"votersCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"}]')

    # Bytecode contains the bytecode of a complied contract 
    _bytecode = '608060405234801561001057600080fd5b5061055d806100206000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c80630121b93f146100675780632d35a8a2146100865780633477ee2e146100a0578063462e91ec1461014357806398c07938146101e9578063a3ec138d146101f1575b600080fd5b6100846004803603602081101561007d57600080fd5b503561022b565b005b61008e61033b565b60408051918252519081900360200190f35b6100bd600480360360208110156100b657600080fd5b5035610341565b6040518084815260200180602001838152602001828103825284818151815260200191508051906020019080838360005b838110156101065781810151838201526020016100ee565b50505050905090810190601f1680156101335780820380516001836020036101000a031916815260200191505b5094505050505060405180910390f35b6100846004803603602081101561015957600080fd5b81019060208101813564010000000081111561017457600080fd5b82018360208201111561018657600080fd5b803590602001918460018302840111640100000000831117156101a857600080fd5b91908080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152509295506103eb945050505050565b61008e610447565b6102176004803603602081101561020757600080fd5b50356001600160a01b031661044d565b604080519115158252519081900360200190f35b3360009081526002602052604090205460ff1615610289576040805162461bcd60e51b8152602060048201526016602482015275566f7465722063616e277420766f746520747769636560501b604482015290519081900360640190fd5b60008111801561029b57506001548111155b6102d65760405162461bcd60e51b815260040180806020018281038252602b8152602001806104fe602b913960400191505060405180910390fd5b336000908152600260208181526040808420805460ff19166001908117909155600380548201905585855291849052808420909201805490910190555182917ffff3c900d938d21d0990d786e819f29b8d05c1ef587b462b939609625b684b1691a250565b60015481565b600060208181529181526040908190208054600180830180548551600293821615610100026000190190911692909204601f81018790048702830187019095528482529194929390928301828280156103db5780601f106103b0576101008083540402835291602001916103db565b820191906000526020600020905b8154815290600101906020018083116103be57829003601f168201915b5050505050908060020154905083565b60018054810180825560408051606081018252828152602080820186815260008385018190529485528482529290932081518155915180519194929361043693850192910190610462565b506040820151816002015590505050565b60035481565b60026020526000908152604090205460ff1681565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106104a357805160ff19168380011785556104d0565b828001600101855582156104d0579182015b828111156104d05782518255916020019190600101906104b5565b506104dc9291506104e0565b5090565b6104fa91905b808211156104dc57600081556001016104e6565b9056fe596f757220766f746520646f65736e2774206d6174636820776974636820616e792063616e646964617465a265627a7a7231582006b2d533071df7b9888c9367a825a15feafdd14a8e3730fc488a6dd67bf652fd64736f6c634300050b0032'
    _proposals = list() 
  
        

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
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and ['abi', 'bytecode', 'proposal_names'] not in x ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) or data # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
