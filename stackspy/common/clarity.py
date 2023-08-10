from .c32helpers import c32_address_decode
from .helpers import StacksMessageType
from enum import Enum

class ClarityType(Enum):
    Int = 0x00
    UInt = 0x01
    Buffer = 0x02
    BoolTrue = 0x03
    BoolFalse = 0x04
    PrincipalStandard = 0x05
    PrincipalContract = 0x06
    ResponseOk = 0x07
    ResponseErr = 0x08
    OptionalNone = 0x09
    OptionalSome = 0x0a
    List = 0x0b
    Tuple = 0x0c
    StringASCII = 0x0d
    StringUTF8 = 0x0e


def create_address_from_c32_address_string(c32_address_string):
    address_data = c32_address_decode(c32_address_string)
    return {
        "type": StacksMessageType.Address.value,
        "version": address_data[0],
        "hash160": address_data[1]
    }

def standard_principal_cv(address_string):
    address = create_address_from_c32_address_string(address_string)
    return {
        "type": ClarityType.PrincipalStandard.value,
        "address": address
    }

def prinicpal_cv(principal):
    if "." in principal:
        # TODO - Implement Contract Principal CV
        return
    else:
        return standard_principal_cv(principal) 