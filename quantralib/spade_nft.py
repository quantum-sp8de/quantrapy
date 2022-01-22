import string
from .spade_base import EOSSP8DEBase


_ALPHABET = string.ascii_lowercase + string.digits[1:6]
_UINT64_MAX= (1 << 64) -1

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

def _validate_u64(s):
    ret = None

    try:
        if isinstance(s, int):
            ret = s
        elif isinstance(s, str):
            ret = int(s)
    except Exception as ex:
        raise ValueError("Invalid uint64 value {}: {}".format(s, ex)) from ex

    if ret is None:
        raise ValueError("Invalid type {} is not a uint64 compatible".format(type(s)))

    if ret < 0 or ret > _UINT64_MAX:
        raise ValueError("Invalid uint64 value {}: out of uint_64 range".format(s))

    return ret

class EOSSP8DE_NFT(EOSSP8DEBase):
    def __init__(self, contract_account, p_keys, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_keys, chain_url=chain_url, chain_port=chain_port)

    def get_assets(self, account, limit=10):
        return self.ce.get_table(self.contract_account, account, "sassets", limit=limit)

    def _author(self, author, dappinfo, fieldtypes, priorityimg, op_type):
        author = _validate_s(author)

        arguments = {
            "author": author,
            "dappinfo": dappinfo,
            "fieldtypes": fieldtypes,
            "priorityimg": priorityimg
        }
        payload = {
            "account": self.contract_account,
            "name": op_type,
            "authorization": [{
                "actor": author,
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
        author = _validate_s(author)

        arguments = {
            "author": author,
            "category": _validate_s(category),
            "usearam": usearam
        }
        payload = {
            "account": self.contract_account,
            "name": 'setarampayer',
            "authorization": [{
                "actor": author,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def create(self, author, category, owner, idata, mdata, requireclaim):
        """Create a new NFT"""
        author = _validate_s(author)

        arguments = {
            "author": author,
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
                "actor": author,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def update(self, author, owner, assetid, mdata):
        """Update NFT info"""
        author = _validate_s(author)

        arguments = {
            "author": author,
            "owner": _validate_s(owner),
            "assetid": _validate_u64(assetid),
            "mdata": mdata
        }
        payload = {
            "account": self.contract_account,
            "name": 'update',
            "authorization": [{
                "actor": author,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def transfer(self, acc_from, acc_to, assetids, memo):
        """Transfer the NFT ownership"""
        assetids = [_validate_u64(a) for a in assetids]
        acc_to = _validate_s(acc_to)
        acc_from = _validate_s(acc_from)

        arguments = {
            "to": acc_to,
            "from": acc_from,
            "assetids": assetids,
            "memo": memo
        }
        payload = {
            "account": self.contract_account,
            "name": 'transfer',
            "authorization": [
            {
                "actor": acc_from,
                "permission": "active",
            },
            {
                "actor": acc_to,
                "permission": "active",

            }],
        }

        return self._push_action_with_data(arguments, payload)

    def delegate(self, owner, acc_to, assetids, period, redelegate, memo):
        """Delegate NFT ownership"""
        assetids = [_validate_u64(a) for a in assetids]
        owner = _validate_s(owner)

        arguments = {
            "owner": owner,
            "to": _validate_s(acc_to),
            "assetids": assetids,
            "period": _validate_u64(period),
            "redelegate": redelegate,
            "memo": memo
        }
        payload = {
            "account": self.contract_account,
            "name": 'delegate',
            "authorization": [{
                "actor": owner,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def undelegate(self, owner, assetids):
        """Undelegate NFT ownership when delegate period is expired"""
        assetids = [_validate_u64(a) for a in assetids]
        owner = _validate_s(owner)

        arguments = {
            "owner": owner,
            "assetids": assetids,
        }
        payload = {
            "account": self.contract_account,
            "name": 'undelegate',
            "authorization": [{
                "actor": owner,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def delegatemore(self, owner, assetid, period):
        """Delegate NFT asset for more period"""
        owner = _validate_s(owner)

        arguments = {
            "owner": owner,
            "assetidc": _validate_u64(assetid),
            "period": _validate_u64(period)
        }
        payload = {
            "account": self.contract_account,
            "name": 'delegatemore',
            "authorization": [{
                "actor": owner,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def mdadd(self, author, data):
        """Add additional info to author"""
        author = _validate_s(author)

        arguments = {
            "author": author,
            "data": data
        }
        payload = {
            "account": self.contract_account,
            "name": 'mdadd',
            "authorization": [{
                "actor": author,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def mdupdate(self, md_id, author, data):
        """Update additional info of NFT author"""
        author = _validate_s(author)

        arguments = {
            "id": _validate_u64(md_id),
            "author": author,
            "data": data
        }
        payload = {
            "account": self.contract_account,
            "name": 'mdupdate',
            "authorization": [{
                "actor": author,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def mdremove(self, md_id, author):
        """Delete additional info of NFT author"""
        author = _validate_s(author)

        arguments = {
            "id": _validate_u64(md_id)
        }
        payload = {
            "account": self.contract_account,
            "name": 'mdremove',
            "authorization": [{
                "actor": author,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)


class EOSSP8DE_NFT_EXCHANGE(EOSSP8DEBase):
    def __init__(self, contract_account, p_keys, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_keys, chain_url=chain_url, chain_port=chain_port)

    def get_lots(self, limit=10):
        return self.ce.get_table(self.contract_account, self.contract_account, "lots", limit=limit)

    def makelot(self, account, assetid, price, period):
        """Create a new NFT lot"""
        account = _validate_s(account)

        arguments = {
            "nft_id": _validate_u64(assetid),
            "price": price,
            "time_period": period
        }
        payload = {
            "account": self.contract_account,
            "name": 'makelot',
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def cancellot(self, account, lot_id):
        """Cancel NFT lot with specific lot id"""
        account = _validate_s(account)

        arguments = {
            "lot_id": _validate_u64(lot_id)
        }
        payload = {
            "account": self.contract_account,
            "name": 'cancellot',
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def returnfunds(self, account, asset_symbol):
        """Return funds for the won NFT"""
        account = _validate_s(account)

        arguments = {
            "asset_symbol": asset_symbol
        }
        payload = {
            "account": self.contract_account,
            "name": 'returnfunds',
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)
