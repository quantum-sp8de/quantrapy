# quantralib library
This is a fork from https://github.com/eosnewyork/eospy with additional
support of QRandom ecosystem.

For the supported API endpoints, please refer to the original eospy library

## Command line tool examples (QRandom related)

### Buy a random value for "valera123456" user
`quantrapy -u http://1.2.3.4:888 random -c lalalalala12 -t erergerer541 buyrandom -k /home/user/project/quantra/q.key valera123456`

### Get random config
`quantrapy -u http://1.2.3.4:888 random -c lalalalala12 -t erergerer541 getconfig`

## Command line tool examples (NFT related)

### Create a new NFT
`quantrapy --url http://1.2.3.4:4444 nft create tester selfcategory tester "{some_key} : {some_data}" "" false -k ./my_private.key`

### Delegate your NFT
`quantrapy --url http://1.2.3.4:4444 nft delegate tester creator 100000000000129 90 false "90 sec delegation test" -k ./my_private.key`

### Transfer multiple NFTs
`quantrapy --url http://1.2.3.4:4444 nft transfer tester creator 100000000000128 100000000000127 "transfering 2 NFTs" -k ./my_private.key`

## For Developers
Please , refer to the `quantralib.erandom` and `quantralib.nft*` modules to figure out how to integrate sp8de project into your application
