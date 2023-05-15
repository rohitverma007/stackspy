import unittest
import stackspy

class TestStacksAccount(unittest.TestCase):

    def test_account_address(self):
        secret_key = "sound idle panel often situate develop unit text design antenna vendor screen opinion balcony share trigger accuse scatter visa uniform brass update opinion media"
        wallet = stackspy.StacksWallet(secret_key)
        account = wallet.get_account(0)

        mainnet_p2pkh = account.get_address(stackspy.AddressVersion.MainnetP2PKH)
        mainnet_p2sh = account.get_address(stackspy.AddressVersion.MainnetP2SH)
        testnet_p2pkh = account.get_address(stackspy.AddressVersion.TestnetP2PKH)
        testnet_p2sh = account.get_address(stackspy.AddressVersion.TestnetP2SH)

        self.assertEqual(mainnet_p2pkh, "SP384CVPNDTYA0E92TKJZQTYXQHNZSWGCAG7SAPVB")
        self.assertEqual(mainnet_p2sh, "SM384CVPNDTYA0E92TKJZQTYXQHNZSWGCAGRD22C9")
        self.assertEqual(testnet_p2pkh, "ST384CVPNDTYA0E92TKJZQTYXQHNZSWGCAH0ER64E")
        self.assertEqual(testnet_p2sh, "SN384CVPNDTYA0E92TKJZQTYXQHNZSWGCAKNRHMGW")

    def test_account_address_index(self):
        secret_key = "sound idle panel often situate develop unit text design antenna vendor screen opinion balcony share trigger accuse scatter visa uniform brass update opinion media"
        wallet = stackspy.StacksWallet(secret_key)
        account = wallet.get_account(1)

        mainnet_p2pkh = account.get_address(stackspy.AddressVersion.MainnetP2PKH)
        mainnet_p2sh = account.get_address(stackspy.AddressVersion.MainnetP2SH)
        testnet_p2pkh = account.get_address(stackspy.AddressVersion.TestnetP2PKH)
        testnet_p2sh = account.get_address(stackspy.AddressVersion.TestnetP2SH)

        self.assertEqual(mainnet_p2pkh, "SP23K7K2V45JFZVBMQBE8R0PP8SQG7HZF9473KBD")
        self.assertEqual(mainnet_p2sh, "SM23K7K2V45JFZVBMQBE8R0PP8SQG7HZFB7DZ2RK")
        self.assertEqual(testnet_p2pkh, "ST23K7K2V45JFZVBMQBE8R0PP8SQG7HZFA6Z68VE")
        self.assertEqual(testnet_p2sh, "SN23K7K2V45JFZVBMQBE8R0PP8SQG7HZFAFNYMDJ")

if __name__ == '__main__':
    unittest.main()