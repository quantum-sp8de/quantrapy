from .cleos import Cleos
from .keys import EOSKey


class EOSSP8DEBase:
    def __init__(self, contract_account, p_key, chain_url="http://localhost", chain_port=None):
        self.chain_url = chain_url
        self.chain_port = chain_port
        if chain_port:
            url = url='%s:%s' %(chain_url, chain_port)
        else:
            url = url='%s' % chain_url
        self.ce = Cleos(url)
        self.contract_account = contract_account
        self.p_key = p_key

    def _push_action_with_data(self, arguments, payload):
        data = self.ce.abi_json_to_bin(payload['account'], payload['name'], arguments)
        payload['data'] = data['binargs']
        trx = {"actions": [payload]}

        key = EOSKey(self.p_key)
        resp = self.ce.push_transaction(trx, key, broadcast=True)

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
