from .cleos import Cleos
from .keys import EOSKey
from .cipher import xor_crypt_decode


class EOSRandom:
    def __init__(self, contract_account, p_key, tokens_account, chain_url="http://localhost", chain_port=None):
        self.chain_url = chain_url
        self.chain_port = chain_port
        if chain_port:
            url = url='%s:%s' %(chain_url, chain_port)
        else:
            url = url='%s' % chain_url
        self.ce = Cleos(url)
        self.contract_account = contract_account
        self.p_key = p_key
        self.tokens_account = tokens_account

    def check_if_validator(self, account):
        ret = False
        r = self.ce.get_table(self.contract_account, self.contract_account, "validators")

        for r in r['rows']:
            if r.get("owner") == account:
                ret = True
                break
        else:
            ret = False

        return ret

    def get_config_table(self):
        return self.ce.get_table(self.contract_account, self.contract_account, "config")

    def get_config_table_value(self, value):
        r = self.get_config_table()
        ret = r['rows'][0][value]

        return ret

    def get_minimal_deposit(self):
        return self.get_config_table_value("minimal_deposit")

    def get_random_price(self):
        return self.get_config_table_value("random_price")

    def get_randresult(self, account):
        r = self.ce.get_table(self.contract_account, account, "randresult2")
        owner = r['rows'][0]["owner"]
        en_value = r['rows'][0]["value"].strip()
        key = self.get_dynamic_encrypt_pubkey(account)

        value = xor_crypt_decode(en_value, key)
        # if key has been changed meantime
        try:
            ret = int(value)
        except Exception:
            raise RuntimeError("Invalid value and key pair: %s/%s..." % (en_value, key[:7])) from None

        return ret

    def _push_action_with_data(self, arguments, payload):
        data = self.ce.abi_json_to_bin(payload['account'], payload['name'], arguments)
        payload['data'] = data['binargs']
        trx = {"actions": [payload]}

        key = EOSKey(self.p_key)
        resp = self.ce.push_transaction(trx, key, broadcast=True)

        return resp

    def register_as_validator(self, account, depos):
        arguments = {
            "from": account,
            "to": self.contract_account,
            "quantity": depos,
            "memo": "registration"
        }
        payload = {
            "account": self.tokens_account,
            "name": "transfer",
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def setrandom(self, random_num, account):
        arguments = {
            "owner": account,
            "value": str(random_num),
        }
        payload = {
            "account": self.contract_account,
            "name": "setrandom",
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

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

    def set_dynamic_encrypt_pubkey(self, account, pubkey):
        authority = {
            "threshold": "1",
            "accounts": [],
            "keys": [{
                "key": pubkey,
                "weight": "1"
            }],
            "waits": []
        }
        return self._set_account_permission(account, 'encrypt', authority)

    def get_dynamic_encrypt_pubkey(self, account):
        key = None
        acc_info = self.ce.get_account(account)
        for perm in acc_info['permissions']:
            if 'encrypt' == perm['perm_name']:
                key = perm["required_auth"]["keys"][-1]["key"]

        return key

    def buy_random_value(self, account, min_depos, memo=""):
        arguments = {
            "from": account,
            "to": self.contract_account,
            "quantity": min_depos,
            "memo": memo
        }
        payload = {
            "account": self.tokens_account,
            "name": "transfer",
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def buy_random(self, account, memo=""):
        rand_price = self.get_random_price()
        self.buy_random_value(account, rand_price, memo)
        return self.get_randresult(account)
