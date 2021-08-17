# quantralib library
This is a fork from https://github.com/eosnewyork/eospy with additional
support of QRandom ecosystem.

For the supported API endpoints, please refer to the original eospy library

## Command line Tool Examples (QRandom related)

# buy a random value for "valera123456" user
quantrapy -u http://1.2.3.4:888 random -c lalalalala12 -k /home/user/project/quantra/q.key -t erergerer541 buyrandom valera123456

# get config
quantrapy -u http://1.2.3.4:888 random -c lalalalala12 -k /home/user/project/quantra/q.key -t erergerer541 getconfig

## For Developers
Please , refer to the quantralib.erandom.EOSRandom class to figure out how to integrate QRandom into your application
