import unittest

import os
import sys
import string
import secrets
import requests
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)),'..'))
from quantralib.spade_nft import EOSSP8DE_NFT

# ===
# Adjust to your values
NFT_CONTRACT = os.environ.get('TEST_NFT_CONTRACT', 'nft_contract')
NFT_PKEY = os.environ.get('TEST_NFT_PKEY', 'your_private_key')
NFT_CHAIN = os.environ.get('TEST_NFT_CHAIN', 'http://123.123.123.123:4444')
NFT_ACCOUNT = os.environ.get('TEST_NFT_ACCOUNT', 'tester')
# ===

class TestNFT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.q = EOSSP8DE_NFT(contract_account=NFT_CONTRACT,
                             p_key=NFT_PKEY,
                             chain_url=NFT_CHAIN,
                             chain_port=None)

        # contains forbidden digits for some author
        alphabet = string.ascii_lowercase + string.digits[7:]
        cls.invalid_author = '9'+''.join(secrets.choice(alphabet) for i in range(10))

    def test_authorreg_existing_user(self):
        with self.assertRaises(requests.exceptions.HTTPError) as cm:
            r = TestNFT.q.authorreg(NFT_ACCOUNT,
                                    NFT_ACCOUNT,
                                    "{'info': 'app info'}",
                                    fieldtypes="type",
                                    priorityimg="http://unknown.irh/a/b/c/image.png")

        resp = cm.exception.response.json()
        self.assertEqual(resp['code'], 500)
        self.assertIn('already registered', resp['error']['details'][0]['message'])

    def test_authorreg_invalid_user(self):
        with self.assertRaises(ValueError) as cm:
            r = TestNFT.q.authorreg(NFT_ACCOUNT,
                                    TestNFT.invalid_author,
                                    "{'info': 'app info'}",
                                    fieldtypes="type",
                                    priorityimg="http://unknown.irh/a/b/c/image.png")

    def test_authorupdate_user(self):
        r = TestNFT.q.authorupdate(NFT_ACCOUNT,
                                   NFT_ACCOUNT,
                                   "{'info': 'updated app info'}",
                                   fieldtypes="updated type",
                                   priorityimg="http://unknown.irh/a/b/c/updated_image.png")

        self.assertEqual(r['processed']['receipt']['status'], 'executed')

    def test_authorupdate_invalid_user(self):
        with self.assertRaises(ValueError) as cm:
            r = TestNFT.q.authorupdate(NFT_ACCOUNT,
                                       TestNFT.invalid_author,
                                       "{'info': 'updated app info'}",
                                       fieldtypes="updated type",
                                       priorityimg="http://unknown.irh/a/b/c/updated_image.png")
