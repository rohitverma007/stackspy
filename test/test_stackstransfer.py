import unittest
import binascii
import stackspy


def get_private_key():
    pk_hex = "edf9aee84d9b7abc145504dde6726c64f369d37ee34ded868fabd876c26570bc"
    pk_bytes = binascii.unhexlify(pk_hex)
    return stackspy.PyPrivateKey(pk_bytes)

class TestMyRustLib(unittest.TestCase):
    def test_signed_token_transfer_mainnet(self):
        # print(stackspy.PostConditions.empty())
        post_conditions = stackspy.PostConditions.empty()

        stacks_mainnet = stackspy.StacksMainnet()  # create an instance of StacksMainnet
        transaction = stackspy.STXTokenTransfer(
            "SP3FGQ8Z7JY9BWYZ5WM53E0M9NK7WHJF0691NZ159",
            get_private_key(),
            12345,
            0,
            0,
            stacks_mainnet,
            stackspy.AnchorMode.Any,
            "test memo",
            stackspy.PostConditionMode.Deny,
            post_conditions,
            False
        )
        transaction.sign()

        serialized = transaction.serialize()
        tx_id = transaction.tx_id().to_bytes()

        tx_hex = serialized.hex()
        tx_id_hex = tx_id.hex()

        expected_tx_hex = "0000000001040015c31b8c1c11c515e244b75806bac48d1399c7750000000000000000000000000000000000008b316d56e35b3b8d03ab3b9dbe05eb44d64c53e7ba3c468f9a78c82a13f2174c32facb0f29faeb21075ec933db935ebc28a8793cc60e14b8ee4ef05f52c94016030200000000000516df0ba3e79792be7be5e50a370289accfc8c9e032000000000000303974657374206d656d6f00000000000000000000000000000000000000000000000000"
        expected_txid_hex = "84cccb05f4bd0e1b08905ef1f1350ad635a6474448310548bdccfa04e0121bab"

        self.assertEqual(tx_hex, expected_tx_hex)
        self.assertEqual(tx_id_hex, expected_txid_hex)


if __name__ == '__main__':
    unittest.main()
