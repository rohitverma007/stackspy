from common.helpers import is_single_sig
from transactions import StacksTransaction
class TransactionSigner:
    def __init__(self, transaction: StacksTransaction):
        self.transaction = transaction
        self.sig_hash = transaction.sign_begin()
        self.origin_done = False
        self.check_oversign = True
        self.check_overlap = True

        spending_condition = transaction.auth["spendingCondition"]
        if spending_condition and not is_single_sig(spending_condition):
            # TODO implmenet
            pass
    
    def sign_origin(self, priv_key):
        if self.check_overlap and self.origin_done:
            raise ValueError('Cannot sign origin after sponsor key')

        if self.transaction.auth is None:
            raise ValueError('"transaction.auth" is undefined')
        if self.transaction.auth["spendingCondition"] is None:
            raise ValueError('"transaction.auth.spendingCondition" is undefined')

        if not is_single_sig(self.transaction.auth["spendingCondition"]):
            # TODO - Implement
            pass

        next_sig_hash = self.transaction.sign_next_origin(self.sig_hash, priv_key)
        self.sig_hash = next_sig_hash