from .spade_base import EOSSP8DEBase

class TwoFA(EOSSP8DEBase):
    def __init__(self, contract_account, p_keys, twofa_account, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_keys, chain_url=chain_url, chain_port=chain_port)
        self.twofa_account = twofa_account

    def generate(self):
        arguments = {
            "owner": self.twofa_account
        }
        payload = {
            "account": self.contract_account,
            "name": "generate",
            "authorization": [{
                "actor": self.twofa_account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)
    
    def validate(self, twofa_code):
        arguments = {
            "owner": self.twofa_account,
            "twofa_str": twofa_code
        }
        payload = {
            "account": self.contract_account,
            "name": "validate",
            "authorization": [{
                "actor": self.twofa_account,
                "permission": "active",
            }],
        }

        return self._push_action_with_data(arguments, payload)
