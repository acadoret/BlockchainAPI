import json, enum
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta

from .. import db


class Contract(db.Model):
    __tablename__ = 'contracts'
    
    class state_enum(enum.Enum):
        in_progress = "in_progress"
        done = "done"
    
    address = db.Column(db.String(42), primary_key=True)
    state = db.Column(db.Enum(state_enum))
    name = db.Column(db.String(32))
    description = db.Column(db.String(512))
    end_date = db.Column(db.DateTime, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    
    user_address = db.Column(db.ForeignKey('users.address'))
    user = db.relationship('User', foreign_keys=[user_address])
    
    # voter_ids = db.Column(db.String, db.ForeignKey('users.address'))
    """
    Not stored in DB
    """
    # Abi contains a single .sol contract compiled in JSON
    _abi = json.loads('[{"constant":false,"inputs":[{"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"addCandidate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"votersCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getCandidatesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"}]')


    # Bytecode contains the bytecode of a complied contract 
    _bytecode = '608060405234801561001057600080fd5b50610584806100206000396000f3fe608060405234801561001057600080fd5b506004361061007d5760003560e01c8063462e91ec1161005b578063462e91ec1461015e57806398c0793814610204578063a3ec138d1461020c578063bb9aa28f146102465761007d565b80630121b93f146100825780632d35a8a2146100a15780633477ee2e146100bb575b600080fd5b61009f6004803603602081101561009857600080fd5b503561024e565b005b6100a961035e565b60408051918252519081900360200190f35b6100d8600480360360208110156100d157600080fd5b5035610364565b6040518084815260200180602001838152602001828103825284818151815260200191508051906020019080838360005b83811015610121578181015183820152602001610109565b50505050905090810190601f16801561014e5780820380516001836020036101000a031916815260200191505b5094505050505060405180910390f35b61009f6004803603602081101561017457600080fd5b81019060208101813564010000000081111561018f57600080fd5b8201836020820111156101a157600080fd5b803590602001918460018302840111640100000000831117156101c357600080fd5b91908080601f01602080910402602001604051908101604052809392919081815260200183838082843760009201919091525092955061040e945050505050565b6100a961046a565b6102326004803603602081101561022257600080fd5b50356001600160a01b0316610470565b604080519115158252519081900360200190f35b6100a9610485565b3360009081526002602052604090205460ff16156102ac576040805162461bcd60e51b8152602060048201526016602482015275566f7465722063616e277420766f746520747769636560501b604482015290519081900360640190fd5b6000811180156102be57506001548111155b6102f95760405162461bcd60e51b815260040180806020018281038252602b815260200180610525602b913960400191505060405180910390fd5b336000908152600260208181526040808420805460ff19166001908117909155600380548201905585855291849052808420909201805490910190555182917ffff3c900d938d21d0990d786e819f29b8d05c1ef587b462b939609625b684b1691a250565b60015481565b600060208181529181526040908190208054600180830180548551600293821615610100026000190190911692909204601f81018790048702830187019095528482529194929390928301828280156103fe5780601f106103d3576101008083540402835291602001916103fe565b820191906000526020600020905b8154815290600101906020018083116103e157829003601f168201915b5050505050908060020154905083565b6001805481018082556040805160608101825282815260208082018681526000838501819052948552848252929093208151815591518051919492936104599385019291019061048c565b506040820151816002015590505050565b60035481565b60026020526000908152604090205460ff1681565b6001545b90565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106104cd57805160ff19168380011785556104fa565b828001600101855582156104fa579182015b828111156104fa5782518255916020019190600101906104df565b5061050692915061050a565b5090565b61048991905b80821115610506576000815560010161051056fe596f757220766f746520646f65736e2774206d6174636820776974636820616e792063616e646964617465a265627a7a7231582077ee8338e649b26e57a3d89831d16dc5f2f2dacd7f362c1b9cfd9d936e01097764736f6c634300050b0032'
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
