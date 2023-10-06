from stackspy.common.clarity import create_address_from_c32_address_string
from stackspy.constants import PostConditionPrincipalID, StacksMessageType

def create_standard_principal(address_string):
    addr = create_address_from_c32_address_string(address_string)
    return {
        'type': StacksMessageType.Principal.value,
        'prefix': PostConditionPrincipalID.Standard.value,
        'address': addr
    }