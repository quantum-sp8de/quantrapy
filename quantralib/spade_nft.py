from .spade_base import EOSSP8DEBase


class EOSSP8DE_NFT(EOSSP8DEBase):
    def __init__(self, contract_account, p_key, chain_url="http://localhost", chain_port=None):
        EOSSP8DEBase.__init__(self, contract_account, p_key, chain_url=chain_url, chain_port=chain_port)

    def _author(self, account, author, dappinfo, fieldtypes, priorityimg, op_type):
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
        """Register new NFT author"""
        return self._author(account, author, dappinfo, fieldtypes, priorityimg, 'authorreg')

    def authorupdate(self, account, author, dappinfo, fieldtypes, priorityimg):
        """Update data for registered NFT author"""
        return self._author(account, author, dappinfo, fieldtypes, priorityimg, 'authorupdate')
