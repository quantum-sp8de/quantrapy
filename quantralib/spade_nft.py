import string
from .spade_base import EOSSP8DEBase


_ALPHABET = string.ascii_lowercase + string.digits[1:6]


def _validate_s(s):
    ''' Basic blockchain checking for valid syms in account names'''
    invalid = []
    for i,sym in enumerate(s):
        if sym not in _ALPHABET:
            invalid.append("{} at index {}".format(sym, i))
    if invalid:
        er_desc = ";".join(invalid)
        raise ValueError("Invalid symbols found in name {}: {}".format(s, er_desc))

    return s


class EOSSP8DE_NFT(EOSSP8DEBase):
    def __init__(self, account, contract_account, p_key, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_key, chain_url=chain_url, chain_port=chain_port)
        self.account = _validate_s(account)

    def _author(self, author, dappinfo, fieldtypes, priorityimg, op_type):
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
                "actor": self.account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def authorreg(self, author, dappinfo, fieldtypes, priorityimg):
        """Register new NFT author"""
        return self._author(author, dappinfo, fieldtypes, priorityimg, 'authorreg')

    def authorupdate(self, author, dappinfo, fieldtypes, priorityimg):
        """Update data for registered NFT author"""
        return self._author(author, dappinfo, fieldtypes, priorityimg, 'authorupdate')

    def setarampayer(self, author, category, usearam):
        """Set ram payer for NFTs"""
        arguments = {
            "author": _validate_s(author),
            "category": _validate_s(category),
            "usearam": usearam
        }
        payload = {
            "account": self.contract_account,
            "name": 'setarampayer',
            "authorization": [{
                "actor": self.account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def create(self, author, category, owner, idata, mdata, requireclaim):
        """Create a new NFT"""
        arguments = {
            "author": _validate_s(author),
            "category": _validate_s(category),
            "owner": _validate_s(owner),
            "idata": idata,
            "mdata": mdata,
            "requireclaim": requireclaim
        }
        payload = {
            "account": self.contract_account,
            "name": 'create',
            "authorization": [{
                "actor": self.account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)
