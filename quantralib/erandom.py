from .cipher import xor_crypt_decode
from .spade_base import EOSSP8DEBase
from .utils import MIN_CONTRACT_VERSION, EOSIncorectContractVersion


class EOSRandom(EOSSP8DEBase):
    def __init__(self, contract_account, p_keys, tokens_account, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_keys, chain_url=chain_url, chain_port=chain_port)
        self.tokens_account = tokens_account

        if self.get_random_contract_version() < MIN_CONTRACT_VERSION:
            raise EOSIncorectContractVersion('Invalid contract version, please update quatrapy library to latest version')

    def check_if_generator(self, account):
        """Check if account is already registered to generate randoms"""
        ret = False
        r = self.ce.get_table(self.contract_account, self.contract_account, "generators")

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
        return self.ce.get_table(self.contract_account, self.contract_account, "confencrpt")

    def get_rkeys(self, account):
        return self.ce.get_table(self.contract_account, account, "generatorkey")

    def get_config_table_value(self, value):
        r = self.get_config_table()
        ret = r['rows'][0][value]
        return ret

    def get_random_price(self):
        """Returns the price for buying a random value"""
        return self.get_config_table_value("random_price")
    
    def get_random_contract_version(self):
        table = self.ce.get_table(self.contract_account, self.contract_account, "version")
        return table['rows'][0]['version']

    def _try_with_key(self, account, en_value, key_type):
        if key_type == 'encrypt':
            key = self.get_dynamic_encrypt_pubkey(account)
        elif key_type == 'backup':
            key = self.get_dynamic_backup_pubkey(account)
        else:
            raise RuntimeError("Invilid key type, must be 'encrypt' or 'backup'")

        value = xor_crypt_decode(en_value, key)
        return int(value)

    def get_randresult(self, account):
        """Get the bought decrypted random value for account"""
        r = self.ce.get_table(self.contract_account, account, "randresult2")

        encrypt_level = r['rows'][0]["encrypt_level"]
        results = r['rows'][0]["results"]

        ret = [] 
        for data in results:
            owner = data["owner"]
            en_value = data["value"].strip()
        
            res = ''
            for key_type in ("encrypt", "backup"):
                try:
                    res = self._try_with_key(owner, en_value, key_type)
                    break
                except Exception:
                    continue

            if not res:
                continue
                # raise RuntimeError("Invalid value: %s can not be restored with both encrypt/backup keys" % en_value) from None

            ret.append(res) 

        return ret

    def register_as_generator(self, account, public_key, creator_account):
        """Register account to be able generate and send randoms"""
        arguments = {
            "owner": account,
            "pk": public_key
        }
        payload = {
            "account": self.contract_account,
            "name": "reggenerator",
            "authorization": [{
                "actor": creator_account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def setrandom(self, random_value, random_digest, account, sign, pin):
        """Set the new value in QRandom subsystem"""
        arguments = {
            "owner": account,
            "value": str(random_value),
            "digest": random_digest,
            "sign": sign,
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

    def setgenkey(self, account, generator, key):
        """Set the new key for random values for a specific generator"""
        arguments = {
            "generator": generator,
            "key": key,
        }
        payload = {
            "account": self.contract_account,
            "name": "setgenkey",
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def _set_dynamic_pubkey(self, account, pubkey, key_type):
        """Set the new pass for random decrypt value"""

        arguments = {
            "account": account,
            "encrypt": ("", pubkey)[key_type == "encrypt"],
            "backup":  ("", pubkey)[key_type == "backup"],
        }
        payload = {
            "account": self.contract_account,
            "name": "setacctpass",
            "authorization": [{
                "actor": account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)

    def set_dynamic_encrypt_pubkey(self, account, pubkey):
        return self._set_dynamic_pubkey(account, pubkey, 'encrypt')

    def set_dynamic_backup_pubkey(self, account, pubkey):
        return self._set_dynamic_pubkey(account, pubkey, 'backup')

    def _get_dynamic_pubkey(self, account, key_type):
        r = self.ce.get_table(self.contract_account, account, "acctpass")
        try:
            return r["rows"][0][key_type]
        except Exception:
            return None

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
