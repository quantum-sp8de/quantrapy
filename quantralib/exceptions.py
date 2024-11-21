
class InvalidKeyFile(Exception):
    ''' Raised when the key file format is invalid '''
    pass


class InvalidPermissionFormat(Exception):
    ''' Raised when the permission format is invalid'''
    pass


class EOSKeyError(Exception):
    ''' Raised when there is an EOSKey error '''
    pass


class EOSMsigInvalidProposal(Exception):
    ''' Raised when an invalid proposal is queried'''
    pass


class EOSBufferInvalidType(Exception):
    ''' Raised when trying to encode/decode an invalid type '''
    pass


class EOSInvalidSchema(Exception):
    ''' Raised when trying to process a schema '''
    pass


class EOSUnknownObj(Exception):
    ''' Raised when an object is not found in the ABI '''
    pass


class EOSAbiProcessingError(Exception):
    ''' Raised when the abi action cannot be processed '''
    pass


class EOSSetSameCode(Exception):
    ''' Raised when the code would not change on a set'''
    pass


class EOSSetSameAbi(Exception):
    ''' Raised when the abi would not change on a set'''
    pass

class EOSIncorectContractVersion(Exception):
    ''' Raised when incorect contract version'''
    pass