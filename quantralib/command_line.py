import argparse
from .cleos import Cleos
from .testeos import TestEos
from .utils import parse_key_file, str2bool
from .exceptions import InvalidPermissionFormat, EOSSetSameAbi, EOSSetSameCode
import json


def console_print(data):
    print(json.dumps(data, indent=4))


def set_abi(ce, account, permission, abi, key, broadcast, timeout):
    print('setting abi file {}'.format(abi))
    try:
        console_print(ce.set_abi(account, permission, abi, key, broadcast=broadcast, timeout=timeout))
    except EOSSetSameAbi:
        print('Skipping set abi because the new abi is the same as the existing abi')


def set_code(ce, account, permission, code, key, broadcast, timeout):
    print('setting code file {}'.format(code))
    try:
        console_print(ce.set_code(account, permission, code, key, broadcast=broadcast, timeout=timeout))
    except EOSSetSameCode:
        print('Skipping set code because the new code is the same as the existing code')


def cleos():
    parser = argparse.ArgumentParser(description='Command Line Interface to EOSIO via python')
    parser.add_argument('--api-version', '-v', type=str, default='v1', action='store', dest='api_version')
    parser.add_argument('--url', '-u', type=str, action='store', default='https://proxy.eosnode.tools', dest='url')
    parser.add_argument('--time-out', type=int, action='store', default=30, dest='timeout')
    subparsers = parser.add_subparsers(dest='subparser')
    # get
    get_parser = subparsers.add_parser('get')
    get_subparsers = get_parser.add_subparsers(dest='get')
    # info
    get_subparsers.add_parser('info')
    # block
    block_parser = get_subparsers.add_parser('block')
    #block_parser.add_argument('block', type=str)
    block_parser.add_argument('--block', '-b', type=str, action='store', required=True, dest='block')
    # account
    account_parser = get_subparsers.add_parser('account')
    account_parser.add_argument('--account', '-a', type=str, action='store', required=True, dest='account')
    #account_parser.add_argument('account', type=str)
    # code
    code_parser = get_subparsers.add_parser('code')
    code_parser.add_argument('--account', '-a', type=str, action='store', required=True, dest='account')
    #code_parser.add_argument('account', type=str)
    # abi
    abi_parser = get_subparsers.add_parser('abi')
    abi_parser.add_argument('--account', '-a', type=str, action='store', required=True, dest='account')
    abi_parser.add_argument('--raw', action='store_true', dest='raw')
    #abi_parser.add_argument('account', type=str)
    # table
    table_parser = get_subparsers.add_parser('table')
    table_parser.add_argument('--code', '-c', type=str, action='store', required=True, dest='code')
    table_parser.add_argument('--scope', '-S', type=str, action='store', required=True, dest='scope')
    table_parser.add_argument('--table', '-t', type=str, action='store', required=True, dest='table')
    #table_parser.add_argument('contract', type=str, help='The contract who owns the table (required)')
    #table_parser.add_argument('scope', type=str, help='The scope within the contract in which the table is found (required)')
    # table_parser.add_argu`ment('table', type=str, help='The name of the table as specified by the contract abi (required)')
    table_parser.add_argument('--index', type=int, action='store', default=1, dest='index_position', help='Index number')
    table_parser.add_argument('--key-type', type=str, action='store', default="i64", dest='key_type', help='The key type of --index')
    table_parser.add_argument('--lower-bound', type=str, action='store', default=0, dest='lower_bound', help='The name of the key to index by as defined by the abi, defaults to primary key')
    table_parser.add_argument('--upper-bound', type=str, action='store', default=-1, dest='upper_bound')
    table_parser.add_argument('--limit', type=int, action='store', default=1000, dest='limit')
    # currency
    currency = get_subparsers.add_parser('currency')
    currency.add_argument('type', choices=['balance', 'stats'], type=str)
    currency.add_argument('--code', '-c', type=str, action='store', required=True, dest='code')
    currency.add_argument('--symbol', '-s', type=str, action='store', required=True, dest='symbol')
    currency.add_argument('--account', '-a', type=str, action='store', dest='account')
    # accounts
    accounts = get_subparsers.add_parser('accounts')
    accounts.add_argument('--key', '-k', type=str, action='store', required=True, dest='key')
    # transaction
    transaction = get_subparsers.add_parser('transaction')
    transaction.add_argument('--transaction', '-t', type=str, action='store', required=True, dest='transaction')
    # actions
    actions = get_subparsers.add_parser('actions')
    actions.add_argument('--account', '-a', type=str, action='store', required=True, dest='account')
    actions.add_argument('--pos', type=int, action='store', default=-1, dest='pos')
    actions.add_argument('--offset', type=int, action='store', default=-20, dest='offset')
    # bin2json
    bin_json = get_subparsers.add_parser('bin2json')
    bin_json.add_argument('--code', '-c', type=str, action='store', required=True, dest='code')
    bin_json.add_argument('--action', '-a', type=str, action='store', required=True, dest='action')
    bin_json.add_argument('--binargs', '-b', type=str, action='store', required=True, dest='binargs')
    # json2bin
    # create
    create_parser = subparsers.add_parser('create')
    create_subparsers = create_parser.add_subparsers(dest='create')
    # create EOS key
    create_key = create_subparsers.add_parser('key')
    group_key = create_key.add_mutually_exclusive_group(required=True)
    group_key.add_argument('--key-file', '-k', type=str, action='store', help='file to output the keys too', dest='key_file')
    group_key.add_argument('--to-console', '-c', action='store_true', help='output to the console', dest='to_console')
    # push
    push_parser = subparsers.add_parser('push')
    push_subparsers = push_parser.add_subparsers(dest='push')
    push_action = push_subparsers.add_parser('action')
    push_action.add_argument('account', type=str, action='store', help='account name for the contract to execute')
    push_action.add_argument('action', type=str, action='store', help='action to execute')
    push_action.add_argument('data', type=str, action='store', help='JSON string of the arguments to the contract action')
    push_action.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    push_action.add_argument('--permission', '-p', type=str, action='store', required=True, help='account and permission level to use, e.g \'account@permission\'', dest='permission')
    push_action.add_argument('--dont-broadcast', '-d', action='store_false', default=True, help='do not broadcast the transaction to the network.', dest='broadcast')
    # multisig
    msig_parser = subparsers.add_parser('multisig')
    msig_subparsers = msig_parser.add_subparsers(dest='multisig')
    msig_review = msig_subparsers.add_parser('review')
    msig_review.add_argument('proposer', type=str, action='store', help='proposer name')
    msig_review.add_argument('proposal', type=str, action='store', help='proposal name')
    # system commands
    # listproducers
    system_parser = subparsers.add_parser('system')
    system_subparsers = system_parser.add_subparsers(dest='system', help='Send eosio.system contract action to the blockchain')
    producer_sys = system_subparsers.add_parser('listproducers')
    producer_sys.add_argument('--lower-bound', type=str, action='store', default="", dest='lower_bound')
    producer_sys.add_argument('--limit', type=int, action='store', default=50, dest='limit')
    # new account
    newacct_parser = system_subparsers.add_parser('newaccount', help='create a new account')
    newacct_parser.add_argument('creator', type=str, action='store')
    newacct_parser.add_argument('creator_key', type=str, action='store')
    newacct_parser.add_argument('account', type=str, action='store')
    newacct_parser.add_argument('owner', type=str, action='store')
    newacct_parser.add_argument('--active', '-a', type=str, action='store', dest='active')
    newacct_parser.add_argument('--stake-net', type=str, action='store', default='1.0000 EOS', dest='stake_net')
    newacct_parser.add_argument('--stake-cpu', type=str, action='store', default='1.0000 EOS', dest='stake_cpu')
    newacct_parser.add_argument('--buy-ram-kbytes', type=int, action='store', default=8, dest='ramkb')
    newacct_parser.add_argument('--permission', '-p', type=str, action='store', default='active', dest='permission')
    newacct_parser.add_argument('--transfer', action='store_true', default=False, dest='transfer')
    newacct_parser.add_argument('--dont-broadcast', '-d', action='store_false', default=True, dest='broadcast')
    # set
    set_parser = subparsers.add_parser('set')
    set_subparsers = set_parser.add_subparsers(dest='set', help='Set or update blockchain state')
    # abi
    set_abi_parser = set_subparsers.add_parser('abi')
    set_abi_parser.add_argument('account', type=str, action='store', help='The account to set code for')
    set_abi_parser.add_argument('abi', type=str, action='store', help='The fullpath containing the contract abi')
    set_abi_parser.add_argument('key', type=str, action='store', help='Key to sign ')
    set_abi_parser.add_argument('--permission', '-p', type=str, action='store', default='active', dest='permission')
    set_abi_parser.add_argument('--dont-broadcast', '-d', action='store_false', default=True, dest='broadcast')
    # code
    set_code_parser = set_subparsers.add_parser('code')
    set_code_parser.add_argument('account', type=str, action='store', help='The account to set abi for')
    set_code_parser.add_argument('code', type=str, action='store', help='The fullpath containing the contract code')
    set_code_parser.add_argument('key', type=str, action='store', help='Key to sign the transaction')
    set_code_parser.add_argument('--permission', '-p', type=str, action='store', default='active', dest='permission')
    set_code_parser.add_argument('--dont-broadcast', '-d', action='store_false', default=True, dest='broadcast')
    # contract
    set_contract_parser = set_subparsers.add_parser('contract')
    set_contract_parser.add_argument('account', type=str, action='store', help='The account to set abi for')
    set_contract_parser.add_argument('code', type=str, action='store', help='The fullpath containing the contract code')
    set_contract_parser.add_argument('abi', type=str, action='store', help='The fullpath containing the contract abo')
    set_contract_parser.add_argument('key', type=str, action='store', help='Key to sign the transaction')
    set_contract_parser.add_argument('--permission', '-p', type=str, action='store', default='active', dest='permission')
    set_contract_parser.add_argument('--dont-broadcast', '-d', action='store_false', default=True, dest='broadcast')
    # random commands
    random_parser = subparsers.add_parser('random')
    random_parser.add_argument('--contract_account', '-c', type=str, action='store', help='account with QRandom contract', default="quant.random")
    random_parser.add_argument('--tokens_account', '-t', type=str, action='store', help='account with tokens to operate within QRandom contract', default="eosio.token")
    random_subparsers = random_parser.add_subparsers(dest='random', help='Send (q)random action to the blockchain')
    # random getconfig
    getconfig_random = random_subparsers.add_parser('getconfig')
    # random getrandom
    getrandom_random = random_subparsers.add_parser('getrandom')
    getrandom_random.add_argument('account', type=str, action='store', help='account name to buy a random value for')
    # random buyrandom
    buy_random = random_subparsers.add_parser('buyrandom')
    buy_random.add_argument('account', type=str, action='store', help='account name to buy a random value for')
    buy_random.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    # nft command
    nft_parser = subparsers.add_parser('nft')
    nft_parser.add_argument('--contract_account', '-c', type=str, action='store', help='account with NFT contract for actions', default="simpleassets")
    nft_subparsers = nft_parser.add_subparsers(dest='nft', help='Send NFT manipulation actions to the blockchain')
    # nft getassets
    getassets_nft = nft_subparsers.add_parser('getassets')
    getassets_nft.add_argument('account', type=str, action='store', help='account name')
    getassets_nft.add_argument('--limit', type=int, action='store', default=1000, dest='limit')
    # nft authorreg
    authorreg_nft = nft_subparsers.add_parser('authorreg')
    authorreg_nft.add_argument('author', type=str, action='store', help='authors account who will create assets')
    authorreg_nft.add_argument('dappinfo', type=str, action='store', help='stringified json; recommendations to include: game, company, logo, url, desc')
    authorreg_nft.add_argument('fieldtypes', type=str, action='store',
                               help='stringified json with key:state values, where key is key from mdata or idata and state indicates recommended way of displaying field')
    authorreg_nft.add_argument('priorityimg', type=str, action='store', help='json with assosiation category with type of image or video')
    authorreg_nft.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    # nft authorupdate
    authorupdate_nft = nft_subparsers.add_parser('authorupdate')
    authorupdate_nft.add_argument('author', type=str, action='store', help='authors account who will be updated')
    authorupdate_nft.add_argument('dappinfo', type=str, action='store', help='stringified json; recommendations to include: game, company, logo, url, desc')
    authorupdate_nft.add_argument('fieldtypes', type=str, action='store',
                               help='stringified json with key:state values, where key is key from mdata or idata and state indicates recommended way of displaying field')
    authorupdate_nft.add_argument('priorityimg', type=str, action='store', help='json with assosiation category with type of image or video')
    authorupdate_nft.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    # nft setarampayer
    setarampayer_nft = nft_subparsers.add_parser('setarampayer')
    setarampayer_nft.add_argument('author', type=str, action='store', help="asset's author, who will able to update asset's mdata")
    setarampayer_nft.add_argument('category', type=str, action='store', help='assets category')
    setarampayer_nft.add_argument('usearam', type=str2bool, action='store', help='flag for on or off author is a ram payer functionaity')
    setarampayer_nft.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    # nft create
    create_nft = nft_subparsers.add_parser('create')
    create_nft.add_argument('author', type=str, action='store', help="asset's author, who will able to updated asset's mdata")
    create_nft.add_argument('category', type=str, action='store', help='assets category')
    create_nft.add_argument('owner', type=str, action='store', help='assets owner')
    create_nft.add_argument('idata', type=str, action='store', help='stringified json with immutable assets data')
    create_nft.add_argument('mdata', type=str, action='store', help='stringified json with mutable assets data, can be changed only by author')
    create_nft.add_argument('requireclaim', type=str2bool, action='store',
                            help="true or false. If disabled, the asset will be transfered to owner, otherwise author will remain the owner, \
                                  but an offer will be created for the account specified in the owner field to claim the asset using the account's RAM")
    create_nft.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    # nft update
    update_nft = nft_subparsers.add_parser('update')
    update_nft.add_argument('author', type=str, action='store', help="authors account")
    update_nft.add_argument('owner', type=str, action='store', help='current assets owner')
    update_nft.add_argument('assetid', type=int, action='store', help='assetid to update')
    update_nft.add_argument('mdata', type=str, action='store', help='stringified json with mutable assets data. All mdata will be replaced')
    update_nft.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    # nft transfer
    transfer_nft = nft_subparsers.add_parser('transfer')
    transfer_nft.add_argument('account_from', type=str, action='store', help='account who sends the asset')
    transfer_nft.add_argument('account_to', type=str, action='store', help='account of receiver')
    transfer_nft.add_argument('assetids', nargs='+', type=int, help="assetid's to transfer")
    transfer_nft.add_argument('memo', type=str, action='store', help='transfers comment')
    transfer_nft.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')
    # nft delegate
    delegate_nft = nft_subparsers.add_parser('delegate')
    delegate_nft.add_argument('owner', type=str, action='store', help='current asset owner account')
    delegate_nft.add_argument('account_to', type=str, action='store', help='borrower account name')
    delegate_nft.add_argument('assetids', nargs='+', type=int, help="assetid's to delegate")
    delegate_nft.add_argument('period', type=int, action='store', help="time in seconds that the asset will be lent")
    delegate_nft.add_argument('redelegate', type=str2bool, action='store', help='boolean, True if assetids can be re-delegated')
    delegate_nft.add_argument('memo', type=str, action='store', help='memo for delegate action')
    delegate_nft.add_argument('--key-file', '-k', type=str, action='store', required=True, help='file containing the private key that will be used', dest='key_file')


    # process args
    args = parser.parse_args()
    #
    # connect
    ce = Cleos(url=args.url, version=args.api_version)

    # run commands based on subparser
    # GET
    if args.subparser == 'get':
        if args.get == 'info':
            console_print(ce.get_info(timeout=args.timeout))
        elif args.get == 'block':
            console_print(ce.get_block(args.block, timeout=args.timeout))
        elif args.get == 'account':
            console_print(ce.get_account(args.account, timeout=args.timeout))
        elif args.get == 'code':
            console_print(ce.get_code(args.account, timeout=args.timeout))
        elif args.get == 'abi':
            if args.raw:
                console_print(ce.get_raw_abi(args.account, timeout=args.timeout))
            else:
                console_print(ce.get_abi(args.account, timeout=args.timeout))
        elif args.get == 'table':
            console_print(ce.get_table(code=args.code,
                                       scope=args.scope,
                                       table=args.table,
                                       index_position=args.index_position,
                                       key_type=args.key_type,
                                       lower_bound=args.lower_bound,
                                       upper_bound=args.upper_bound,
                                       limit=args.limit,
                                       timeout=args.timeout))

        elif args.get == 'currency':
            if args.type == 'balance':
                if args.account:
                    console_print(ce.get_currency_balance(args.account, code=args.code, symbol=args.symbol, timeout=args.timeout))
                else:
                    raise ValueError('--account is required')
            else:
                console_print(ce.get_currency(code=args.code, symbol=args.symbol, timeout=args.timeout))
        elif args.get == 'accounts':
            console_print(ce.get_accounts(args.key, timeout=args.timeout))
        elif args.get == 'transaction':
            console_print(ce.get_transaction(args.transaction, timeout=args.timeout))
        elif args.get == 'actions':
            console_print(ce.get_actions(args.account, pos=args.pos, offset=args.offset, timeout=args.timeout))
        elif args.get == 'bin2json':
            console_print(ce.abi_bin_to_json(args.code, args.action, args.binargs, timeout=args.timeout))
    # PUSH
    elif args.subparser == 'push':
        if args.push == 'action':
            priv_key = parse_key_file(args.key_file)
            arguments = json.loads(args.data)
            try:
                account, permission = args.permission.split('@')
            except ValueError:
                raise InvalidPermissionFormat('Permission format needs to be account@permission')
            payload = {
                "account": args.account,
                "name": args.action,
                "authorization": [{
                    "actor": account,
                    "permission": permission,
                }],
            }
            data = ce.abi_json_to_bin(args.account, args.action, arguments)
            print(data)
            payload['data'] = data['binargs']
            print(payload)
            trx = {"actions": [payload]}
            resp = ce.push_transaction(trx, priv_key, broadcast=args.broadcast)
            console_print(resp)
    # MULISIG
    elif args.subparser == "multisig":
        if args.multisig == "review":
            console_print(ce.multisig_review(args.proposer, args.proposal))
    # CREATE
    elif args.subparser == 'create':
        if args.create == 'key':
            k = ce.create_key()
            priv_key = 'Private key: {}'.format(k.to_wif())
            pub_key = 'Public key: {}'.format(k.to_public())
            if args.to_console:
                print(priv_key)
                print(pub_key)
            else:
                with open(args.key_file, 'w') as wf:
                    wf.write(priv_key + '\n')
                    wf.write(pub_key + '\n')
                print("Wrote keys to {}".format(args.key_file))
    # SET
    elif args.subparser == 'set':
        if args.set == 'abi':
            set_abi(ce, args.account, args.permission, args.abi, args.key, broadcast=args.broadcast, timeout=args.timeout)
        elif args.set == 'code':
            set_code(ce, args.account, args.permission, args.code, args.key, broadcast=args.broadcast, timeout=args.timeout)
            pass
        elif args.set == 'contract':
            set_abi(ce, args.account, args.permission, args.abi, args.key, broadcast=args.broadcast, timeout=args.timeout)
            set_code(ce, args.account, args.permission, args.code, args.key, broadcast=args.broadcast, timeout=args.timeout)
            pass
    # SYSTEM
    elif args.subparser == 'system':
        if args.system == 'newaccount':
            resp = ce.create_account(args.creator, args.creator_key, args.account, args.owner, args.active,
                                     stake_net=args.stake_net, stake_cpu=args.stake_cpu, ramkb=args.ramkb,
                                     permission=args.permission, transfer=args.transfer, broadcast=args.transfer,
                                     timeout=args.timeout)
            console_print(resp)
        elif args.system == 'listproducers':
            resp = ce.get_producers(lower_bound=args.lower_bound, limit=args.limit)
            console_print(resp)
    # RANDOM
    elif args.subparser == 'random':
        from .erandom import EOSRandom
        if args.random == 'buyrandom':
            priv_key = parse_key_file(args.key_file)
        else:
            from .cipher import generate_dynamic_key
            priv_key = generate_dynamic_key()

        chain = EOSRandom(args.contract_account,
                          p_key=priv_key,
                          tokens_account=args.tokens_account,
                          chain_url=args.url)
        if args.random == 'getconfig':
            console_print(chain.get_config_table())
        if args.random == 'getrandom':
            console_print(chain.get_randresult(account=args.account))
        if args.random == 'buyrandom':
            console_print(chain.buy_random(account=args.account))
    # NFT
    elif args.subparser == 'nft':
        from .spade_nft import EOSSP8DE_NFT

        priv_keys=[]
        if hasattr(args, 'key_file'):
            priv_keys = parse_key_file(args.key_file)

        chain = EOSSP8DE_NFT(contract_account=args.contract_account,
                             p_keys=priv_keys,
                             chain_url=args.url)

        if args.nft == 'getassets':
            console_print(chain.get_assets(args.account, args.limit))
        if args.nft == 'authorreg':
            console_print(chain.authorreg(args.author,
                                          args.dappinfo,
                                          args.fieldtypes,
                                          args.priorityimg))
        if args.nft == 'authorupdate':
            console_print(chain.authorupdate(args.author,
                                             args.dappinfo,
                                             args.fieldtypes,
                                             args.priorityimg))

        if args.nft == 'setarampayer':
            console_print(chain.setarampayer(args.author,
                                             args.category,
                                             args.usearam))
        if args.nft == 'create':
            console_print(chain.create(author=args.author,
                                       category=args.category,
                                       owner=args.owner,
                                       idata=args.idata,
                                       mdata=args.mdata,
                                       requireclaim=args.requireclaim))
        if args.nft == 'update':
            console_print(chain.update(author=args.author,
                                       owner=args.owner,
                                       assetid=args.assetid,
                                       mdata=args.mdata))
        if args.nft == 'transfer':
            console_print(chain.transfer(acc_from=args.account_from,
                                         acc_to=args.account_to,
                                         assetids=args.assetids,
                                         memo=args.memo))
        if args.nft == 'delegate':
            console_print(chain.delegate(owner=args.owner,
                                         acc_to=args.account_to,
                                         assetids=args.assetids,
                                         period=args.period,
                                         redelegate=args.redelegate,
                                         memo=args.memo))

def testeos():
    parser = argparse.ArgumentParser(description='EOSIO testing harness')
    parser.add_argument('--yaml', '-y', type=str, action='store', required=True, dest='yaml_loc')
    parser.add_argument('--tests', '-t', nargs='*', action='store', default="all", dest='tests')
    # process args
    args = parser.parse_args()

    tester = TestEos(args.yaml_loc)
    if args.tests == 'all':
        tester.run_test_all()
    else:
        for test in args.tests:
            tester.run_test_one(test)
