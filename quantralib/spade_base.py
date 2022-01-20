from .cleos import Cleos
from .keys import EOSKey


class EOSSP8DEBase:
    def __init__(self, contract_account, p_keys, chain_url="http://localhost", chain_port=None):
        self.chain_url = chain_url
        self.chain_port = chain_port
        if chain_port:
            url = url='%s:%s' %(chain_url, chain_port)
        else:
            url = url='%s' % chain_url
        self.ce = Cleos(url)
        self.contract_account = contract_account
        self.p_keys = p_keys

    def _push_action_with_data(self, arguments, payload):
        data = self.ce.abi_json_to_bin(payload['account'], payload['name'], arguments)
        payload['data'] = data['binargs']
        trx = {"actions": [payload]}

        if isinstance(self.p_keys, list):
            keys = [EOSKey(pk) for pk in self.p_keys]
        else:
            keys = EOSKey(self.p_keys)
        resp = self.ce.push_transaction(trx, keys, broadcast=True)

        return resp

    def _set_account_permission(self, account, permission, authority, parent="active" ):
        arguments = {
            "account": account,
            "permission": permission,
            "parent": parent,
            "auth": authority
        }
        payload = {
            "account": "eosio",
            "name": "updateauth",
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)
