from .cleos import Cleos
from .keys import EOSKey
from .cipher import xor_crypt_decode


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

class EOSRandom(EOSSP8DEBase):
    def __init__(self, contract_account, p_key, tokens_account, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_key, chain_url=chain_url, chain_port=chain_port)
        self.tokens_account = tokens_account

    def check_if_validator(self, account):
        """Check if account is already registered to generate randoms"""
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
        """Get main configuration for QRandom"""
        return self.ce.get_table(self.contract_account, self.contract_account, "config")

    def get_config_keystable(self):
        return self.ce.get_table(self.contract_account, self.contract_account, "keysconfig")

    def get_rkeys(self, account):
        return self.ce.get_table(self.contract_account, account, "keys")

    def get_config_table_value(self, value):
        r = self.get_config_table()
        ret = r['rows'][0][value]

        return ret

    def get_minimal_deposit(self):
        """Returns the minimal price for registration as random value generator"""
        return self.get_config_table_value("minimal_deposit")

    def get_random_price(self):
        """Returns the price for buying a random value"""
        return self.get_config_table_value("random_price")

    def _try_with_key(self, account, en_value, key_type):
        if key_type == 'dynamic':
            key = self.get_dynamic_encrypt_pubkey(account)
        elif key_type == 'backup':
            key = self.get_dynamic_backup_pubkey(account)
        else:
            raise RuntimeError("Invilid key type, must be 'dynamic' or 'backup'")

        value = xor_crypt_decode(en_value, key)
        return int(value)

    def get_randresult(self, account):
        """Get the bought decrypted random value for account"""
        r = self.ce.get_table(self.contract_account, account, "randresult2")
        owner = r['rows'][0]["owner"]
        en_value = r['rows'][0]["value"].strip()

        ret = None
        for key_type in ("dynamic", "backup"):
            try:
                ret = self._try_with_key(owner, en_value, key_type)
                break
            except Exception:
                continue

        if not ret:
            raise RuntimeError("Invalid value: %s can not be restored with both dynamic/backup keys" % en_value) from None

        return ret

    def register_as_validator(self, account, depos):
        """Register account to be able generate and send randoms"""
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

    def setrandom(self, random_num, account, pin):
        """Set the new value in QRandom subsystem"""
        arguments = {
            "owner": account,
            "value": str(random_num),
            "password": pin,
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

    def setuserkey(self, account, generator, key):
        """Set the new key for random values for a specific generator"""
        arguments = {
            "generator": generator,
            "key": key,
        }
        payload = {
            "account": self.contract_account,
            "name": "setuserkey",
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)


    def _set_dynamic_pubkey(self, account, pubkey, key_type):
        authority = {
            "threshold": "1",
            "accounts": [],
            "keys": [{
                "key": pubkey,
                "weight": "1"
            }],
            "waits": []
        }
        return self._set_account_permission(account, key_type, authority)

    def set_dynamic_encrypt_pubkey(self, account, pubkey):
        return self._set_dynamic_pubkey(account, pubkey, 'encrypt')

    def set_dynamic_backup_pubkey(self, account, pubkey):
        return self._set_dynamic_pubkey(account, pubkey, 'backup')

    def _get_dynamic_pubkey(self, account, key_type):
        key = None
        acc_info = self.ce.get_account(account)
        for perm in acc_info['permissions']:
            if key_type == perm['perm_name']:
                key = perm["required_auth"]["keys"][-1]["key"]

        return key

    def get_dynamic_encrypt_pubkey(self, account):
        return self._get_dynamic_pubkey(account, 'encrypt')

    def get_dynamic_backup_pubkey(self, account):
        return self._get_dynamic_pubkey(account, 'backup')

    def buy_random_value(self, account, min_depos, memo=""):
        """Buy a random value for the account in QRandom system"""
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
        """Buy a random value for the account in QRandom system and return result"""
        rand_price = self.get_random_price()
        self.buy_random_value(account, rand_price, memo)
        return self.get_randresult(account)

class EOSSP8DE_NFT(EOSSP8DEBase):
    def __init__(self, contract_account, p_key, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_key, chain_url=chain_url, chain_port=chain_port)

    def _author(self, account, author, dappinfo, fieldtypes, priorityimg, op_type):
        """"""
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
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def authorreg(self, account, author, dappinfo, fieldtypes, priorityimg):
        return self._author(account, author, dappinfo, fieldtypes, priorityimg, 'authorreg')

    def authorupdate(self, account, author, dappinfo, fieldtypes, priorityimg):
        return self._author(account, author, dappinfo, fieldtypes, priorityimg, 'authorupdate')
