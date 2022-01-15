import string
from .spade_base import EOSSP8DEBase


_alphabet = string.ascii_lowercase + string.digits[1:6]

def _validate_s(s):
    invalid = []
    for i,sym in enumerate(s):
        if sym not in _alphabet:
            invalid.append("{} at index {}".format(sym, i))
    if invalid:
        er_desc = ";".join(invalid)
        raise ValueError("Invalid symbols found in name {}: {}".format(s, er_desc))

    return s

class EOSSP8DE_NFT(EOSSP8DEBase):
    def __init__(self, contract_account, p_key, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_key, chain_url=chain_url, chain_port=chain_port)

    def _author(self, account, author, dappinfo, fieldtypes, priorityimg, op_type):
        arguments = {
            "author": _validate_s(author),
            "dappinfo": dappinfo,
            "fieldtypes": fieldtypes,
            "priorityimg": priorityimg
        }
        payload = {
            "account": self.contract_account,
            "name": op_type,
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def authorreg(self, account, author, dappinfo, fieldtypes, priorityimg):
        """Register new NFT author"""
        return self._author(account, author, dappinfo, fieldtypes, priorityimg, 'authorreg')

    def authorupdate(self, account, author, dappinfo, fieldtypes, priorityimg):
        """Update data for registered NFT author"""
        return self._author(account, author, dappinfo, fieldtypes, priorityimg, 'authorupdate')
