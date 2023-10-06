from .clarity import create_address_from_c32_address_string
from constants import PostConditionPrincipalID
from .helpers import StacksMessageType

def create_standard_principal(address_string):
    addr = create_address_from_c32_address_string(address_string)
    return {
        'type': StacksMessageType.Principal.value,
        'prefix': PostConditionPrincipalID.Standard.value,
        'address': addr
    }