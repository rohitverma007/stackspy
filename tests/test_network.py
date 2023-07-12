import unittest
from stackspy.network import StacksMainnet, StacksTestnet, StacksMocknet, StacksNetwork
from stackspy.network import HIRO_MAINNET_DEFAULT, HIRO_TESTNET_DEFAULT, HIRO_MOCKNET_DEFAULT

class TestStacksNetwork(unittest.TestCase):
    def test_sets_mainnet_default_url(self):
        mainnet = StacksMainnet()
        self.assertEqual(mainnet.coreApiUrl, HIRO_MAINNET_DEFAULT)
        
    def test_sets_testnet_url(self):
        testnet = StacksTestnet()
        self.assertEqual(testnet.coreApiUrl, HIRO_TESTNET_DEFAULT)
        
    def test_sets_mocknet_url(self):
        mocknet = StacksMocknet()
        self.assertEqual(mocknet.coreApiUrl, HIRO_MOCKNET_DEFAULT)
        
    def test_sets_custom_url(self):
        custom_url = 'https://customurl.com'
        custom_net = StacksMainnet({'url': custom_url})
        self.assertEqual(custom_net.coreApiUrl, custom_url)
        
    def test_correct_constructor_for_stacks_network_from_name_strings(self):
        self.assertEqual(StacksNetwork.fromName('mainnet').__class__, StacksMainnet)
        self.assertEqual(StacksNetwork.fromName('testnet').__class__, StacksTestnet)
        self.assertEqual(StacksNetwork.fromName('devnet').__class__, StacksMocknet)
        self.assertEqual(StacksNetwork.fromName('mocknet').__class__, StacksMocknet)
    
if __name__ == '__main__':
    unittest.main()