import unittest
import stackspy

class TestStacks(unittest.TestCase):

    def test_stacks_mainnet(self):
        stacks_mainnet = stackspy.StacksMainnet()
        self.assertEqual(stacks_mainnet.version(), 0)
        self.assertEqual(stacks_mainnet.chain_id(), 1)
        self.assertEqual(stacks_mainnet.base_url(), "https://stacks-node-api.mainnet.stacks.co")

    def test_stacks_testnet(self):
        stacks_testnet = stackspy.StacksTestnet()
        self.assertEqual(stacks_testnet.version(), 128)
        self.assertEqual(stacks_testnet.chain_id(), 2147483648)
        self.assertEqual(stacks_testnet.base_url(), "https://stacks-node-api.testnet.stacks.co")

    def test_stacks_mocknet(self):
        stacks_mocknet = stackspy.StacksMocknet()
        self.assertEqual(stacks_mocknet.version(), 128)
        self.assertEqual(stacks_mocknet.chain_id(), 2147483648)
        self.assertEqual(stacks_mocknet.base_url(), "http://localhost:3999")

if __name__ == '__main__':
    unittest.main()