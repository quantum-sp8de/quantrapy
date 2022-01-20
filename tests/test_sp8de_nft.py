import unittest

import os
import sys
import string
import secrets
import requests
import logging
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)),'..'))
from quantralib.spade_nft import EOSSP8DE_NFT

unittest.sortTestMethodsUsing = lambda *args: -1

# ===
# Adjust to your values
NFT_CONTRACT = os.environ.get('TEST_NFT_CONTRACT', 'nft_contract')
NFT_PKEY = os.environ.get('TEST_NFT_PKEY', 'your_private_key') # or [PKEY1, PKEY2,...]
NFT_CHAIN = os.environ.get('TEST_NFT_CHAIN', 'http://123.123.123.123:4444')
NFT_ACCOUNT = os.environ.get('TEST_NFT_ACCOUNT', 'tester')
NFT_NONEXISTENT_ACCOUNT = os.environ.get('TEST_NFT_NONEXISTENT_ACCOUNT', 'tester22')
NFT_OWNER = os.environ.get('TEST_NFT_OWNER', 'creator')
# ===

class TestNFT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.q = EOSSP8DE_NFT(contract_account=NFT_CONTRACT,
                             p_keys=NFT_PKEY,
                             chain_url=NFT_CHAIN,
                             chain_port=None)

        # contains forbidden digits for some author
        alphabet = string.ascii_lowercase + string.digits[7:]
        cls.invalid_author = '9'+''.join(secrets.choice(alphabet) for i in range(10))

    @classmethod
    def get_last_assetid(cls, account):
        r = TestNFT.q.get_assets(account, limit=1000)
        if len(r['rows']) < 1:
            return None

        return r['rows'][-1]['id']

    @classmethod
    def generate_invalid_assetids(cls, account):
        """ Figure out 3 invalid asset ids for account"""
        invalid_assetids = []

        r = TestNFT.q.get_assets(account, limit=1000)
        asset_ids = [ obj['id'] for obj in r['rows'] ]

        # those in range 0...1000 are likely to be invalid ids, but check anyway this
        for i in range(1000):
            if i not in asset_ids:
                invalid_assetids.append(i)
                if len(invalid_assetids) == 3:
                    break

        return invalid_assetids

    def test_authorreg_existing_user(self):
        with self.assertRaises(requests.exceptions.HTTPError) as cm:
            r = TestNFT.q.authorreg(NFT_ACCOUNT,
                                    "{'info': 'app info'}",
                                    fieldtypes="type",
                                    priorityimg="http://unknown.irh/a/b/c/image.png")

        resp = cm.exception.response.json()
        self.assertEqual(resp['code'], 500)
        self.assertIn('already registered', resp['error']['details'][0]['message'])

    def test_authorreg_invalid_user(self):
        with self.assertRaises(ValueError) as cm:
            r = TestNFT.q.authorreg(TestNFT.invalid_author,
                                    "{'info': 'app info'}",
                                    fieldtypes="type",
                                    priorityimg="http://unknown.irh/a/b/c/image.png")

    def test_authorupdate(self):
        r = TestNFT.q.authorupdate(NFT_ACCOUNT,
                                   "{'info': 'updated app info'}",
                                   fieldtypes="updated type",
                                   priorityimg="http://unknown.irh/a/b/c/updated_image.png")

        self.assertEqual(r['processed']['receipt']['status'], 'executed')

    def test_authorupdate_invalid_author(self):
        with self.assertRaises(ValueError) as cm:
            r = TestNFT.q.authorupdate(TestNFT.invalid_author,
                                       "{'info': 'updated app info'}",
                                       fieldtypes="updated type",
                                       priorityimg="http://unknown.irh/a/b/c/updated_image.png")

    def test_setarampayer(self):
        r = TestNFT.q.setarampayer(NFT_ACCOUNT,
                                   category="test123",
                                   usearam=True)

        self.assertEqual(r['processed']['receipt']['status'], 'executed')

    def test_create_nft_self_owner(self):
        r = TestNFT.q.create(NFT_ACCOUNT,
                             category="test123",
                             owner=NFT_ACCOUNT,
                             idata="{'somedata' : 'someoption'}",
                             mdata="{'somedata2' : 'someoption2'}",
                             requireclaim=False)

        self.assertEqual(r['processed']['receipt']['status'], 'executed')

    def test_create_nft_different_owner(self):
        r = TestNFT.q.create(NFT_ACCOUNT,
                             category="test123",
                             owner=NFT_OWNER,
                             idata="{'somedata' : 'someoption'}",
                             mdata="{'somedata2' : 'someoption2'}",
                             requireclaim=True)

        self.assertEqual(r['processed']['receipt']['status'], 'executed')

    def test_create_nft_with_nonex_owner(self):
        with self.assertRaises(requests.exceptions.HTTPError) as cm:
            r = TestNFT.q.create(NFT_ACCOUNT,
                                 category="test123",
                                 owner=NFT_NONEXISTENT_ACCOUNT,
                                 idata="{'somedata' : 'someoption'}",
                                 mdata="{'somedata2' : 'someoption2'}",
                                 requireclaim=True)

        resp = cm.exception.response.json()
        self.assertEqual(resp['code'], 500)
        self.assertIn('owner account does not exist', resp['error']['details'][0]['message'])

    def test_nft_update_assetid(self):
        last_assetid = TestNFT.get_last_assetid(NFT_ACCOUNT)
        if last_assetid is None:
            logging.warning("No valid assetids found for {}, skipping {}".format(NFT_ACCOUNT,
                                                                                 sys._getframe().f_code.co_name))
            return

        r = TestNFT.q.update(NFT_ACCOUNT,
                             owner=NFT_ACCOUNT,
                             assetid=last_assetid,
                             mdata="{'somedata2' : 'someoption_updated2'}")

        self.assertEqual(r['processed']['receipt']['status'], 'executed')

    def test_nft_update_invalid_assetid(self):
        with self.assertRaises(requests.exceptions.HTTPError) as cm:
            r = TestNFT.q.update(NFT_ACCOUNT,
                                 owner=NFT_OWNER,
                                 assetid=0, # 0 is likely to be an invalid assetid
                                 mdata="{'somedata2' : 'someoption_updated2'}")

        resp = cm.exception.response.json()
        self.assertEqual(resp['code'], 500)
        self.assertIn('not found', resp['error']['details'][0]['message'])

    def test_nft_update_invalid_assetid2(self):
        with self.assertRaises(ValueError) as cm:
            r = TestNFT.q.update(NFT_ACCOUNT,
                                 owner=NFT_OWNER,
                                 assetid=(1<<64),
                                 mdata="{'somedata2' : 'someoption_updated2'}")

    def test_nft_transfer_assetids(self):
        ''' Assuming that 'acc_from' and 'acc_to' accounts have both the same pkey '''
        last_assetid = TestNFT.get_last_assetid(NFT_ACCOUNT)
        if last_assetid is None:
            logging.warning("No valid assetids found for {}, skipping {}".format(NFT_ACCOUNT,
                                                                                 sys._getframe().f_code.co_name))
            return

        r = TestNFT.q.transfer(acc_from=NFT_ACCOUNT,
                       acc_to=NFT_OWNER,
                       assetids=[last_assetid,],
                       memo="Transfering just for fun")

        self.assertEqual(r['processed']['receipt']['status'], 'executed')

    def test_nft_transfer_invalid_assetids(self):
        invalid_assetids = TestNFT.generate_invalid_assetids(NFT_ACCOUNT)

        if not invalid_assetids:
            # no data - no test
            logging.warning("There are no invalid assetids found for {} in range 0-10".format(NFT_ACCOUNT))
            return

        with self.assertRaises(requests.exceptions.HTTPError) as cm:
            r = TestNFT.q.transfer(acc_from=NFT_ACCOUNT,
                                   acc_to=NFT_OWNER,
                                   assetids=invalid_assetids,
                                   memo="Just for fun broken transfer")


        resp = cm.exception.response.json()
        self.assertEqual(resp['code'], 500)
        self.assertIn('cannot be found', resp['error']['details'][0]['message'])

    def test_nft_delegate_assetids(self):
        last_assetid = TestNFT.get_last_assetid(NFT_OWNER)
        if last_assetid is None:
            logging.warning("No valid assetids found for {}, skipping {}".format(NFT_OWNER,
                                                                                 sys._getframe().f_code.co_name))
            return

        r = TestNFT.q.delegate(owner=NFT_OWNER,
                               acc_to=NFT_ACCOUNT,
                               assetids=[last_assetid,],
                               period=55000,
                               redelegate=False,
                               memo="Delegating ownership just for fun")

        self.assertEqual(r['processed']['receipt']['status'], 'executed')

    def test_nft_delegate_invalid_assets(self):
        invalid_assetids = TestNFT.generate_invalid_assetids(NFT_OWNER)

        if not invalid_assetids:
            # no data - no test
            logging.warning("There are no invalid assetids found for {} in range 0-10".format(NFT_ACCOUNT))
            return

        with self.assertRaises(requests.exceptions.HTTPError) as cm:
            r = TestNFT.q.delegate(owner=NFT_OWNER,
                                   acc_to=NFT_ACCOUNT,
                                   assetids=invalid_assetids,
                                   period=55000,
                                   redelegate=False,
                                   memo="Delegating ownership of invalid assets just for fun")

        resp = cm.exception.response.json()
        self.assertEqual(resp['code'], 500)
        self.assertIn('cannot be found', resp['error']['details'][0]['message'])
