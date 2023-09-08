from constants import TransactionVersion, ChainID
from fetch import createFetchFn

HIRO_MAINNET_DEFAULT = 'https://stacks-node-api.mainnet.stacks.co'
HIRO_TESTNET_DEFAULT = 'https://stacks-node-api.testnet.stacks.co'
HIRO_MOCKNET_DEFAULT = 'http://localhost:3999'

StacksNetworks = ['mainnet', 'testnet', 'devnet', 'mocknet']

class StacksNetwork:
    version = TransactionVersion.Mainnet
    chainId = ChainID.Mainnet
    bnsLookupUrl = 'https://stacks-node-api.mainnet.stacks.co'
    broadcastEndpoint = '/v2/transactions'
    transferFeeEstimateEndpoint = '/v2/fees/transfer'
    transactionFeeEstimateEndpoint = '/v2/fees/transaction'
    accountEndpoint = '/v2/accounts'
    contractAbiEndpoint = '/v2/contracts/interface'
    readOnlyFunctionCallEndpoint = '/v2/contracts/call-read'

    def __init__(self, config):
        self.coreApiUrl = config['url']
        self.fetchFn = config.get('fetchFn', createFetchFn())

    @staticmethod
    def fromName(networkName):
        if networkName == 'mainnet':
            return StacksMainnet()
        elif networkName == 'testnet':
            return StacksTestnet()
        elif networkName == 'devnet':
            return StacksDevnet()
        elif networkName == 'mocknet':
            return StacksMocknet()
        else:
            raise ValueError("Invalid network name provided. Must be one of the following: {}".format(
                ', '.join(StacksNetworks)))

    @staticmethod
    def fromNameOrNetwork(network):
        if isinstance(network, StacksNetwork) and network.version is not None:
            return network
        return StacksNetwork.fromName(network)

    def isMainnet(self):
        return self.version == TransactionVersion.Mainnet

    def getBroadcastApiUrl(self):
        return "{}{}".format(self.coreApiUrl, self.broadcastEndpoint)

    def getTransferFeeEstimateApiUrl(self):
        return "{}{}".format(self.coreApiUrl, self.transferFeeEstimateEndpoint)

    def getTransactionFeeEstimateApiUrl(self):
        return "{}{}".format(self.coreApiUrl, self.transactionFeeEstimateEndpoint)

    def getAccountApiUrl(self, address):
        return "{}{}/{}?proof=0".format(self.coreApiUrl, self.accountEndpoint, address)

    def getAccountExtendedBalancesApiUrl(self, address):
        return "{}/extended/v1/address/{}/balances".format(self.coreApiUrl, address)

    def getAbiApiUrl(self, address, contract):
        return "{}{}{}/{}/".format(self.coreApiUrl, self.contractAbiEndpoint, address, contract)

    def getReadOnlyFunctionCallApiUrl(self, contractAddress, contractName, functionName):
        return "{}{}{}/{}/{}".format(self.coreApiUrl, self.readOnlyFunctionCallEndpoint, contractAddress,
                                     contractName, functionName)

    def getInfoUrl(self):
        return "{}/v2/info".format(self.coreApiUrl)

    def getBlockTimeInfoUrl(self):
        return "{}/extended/v1/info/network_block_times".format(self.coreApiUrl)

    def getPoxInfoUrl(self):
        return "{}/v2/pox".format(self.coreApiUrl)

    def getRewardsUrl(self, address, options):
        url = "{}/extended/v1/burnchain/rewards/{}".format(self.coreApiUrl, address)
        if options:
            url = "{}?limit={}&offset={}".format(url, options.limit, options.offset)
        return url

    def getRewardsTotalUrl(self, address):
        return "{}/extended/v1/burnchain/rewards/{}/total".format(self.coreApiUrl, address)

    def getRewardHoldersUrl(self, address, options):
        url = "{}/extended/v1/burnchain/reward_slot_holders/{}".format(self.coreApiUrl, address)
        if options:
            url = "{}?limit={}&offset={}".format(url, options.limit, options.offset)
        return url

    def getStackerInfoUrl(self, contractAddress, contractName):
        return "{}/v2/contracts/call-read/{}/{}".format(self.coreApiUrl, contractAddress, contractName)

    def getDataVarUrl(self, contractAddress, contractName, dataVarName):
        return "{}/v2/data_var/{}/{}/{}?proof=0".format(self.coreApiUrl, contractAddress, contractName, dataVarName)

    def getMapEntryUrl(self, contractAddress, contractName, mapName):
        return "{}/v2/map_entry/{}/{}/{}?proof=0".format(self.coreApiUrl, contractAddress, contractName, mapName)

    def getNameInfo(self, fullyQualifiedName):
        nameLookupURL = "{}/v1/names/{}".format(self.bnsLookupUrl, fullyQualifiedName)
        try:
            resp = self.fetchFn(nameLookupURL)
            if resp.status_code == 404:
                raise Exception('Name not found')
            elif resp.status_code != 200:
                raise Exception("Bad response status: {}".format(resp.status_code))
            else:
                return resp.json()
        except Exception as e:
            print("An error occurred : ", str(e))


class StacksMainnet(StacksNetwork):
    version = TransactionVersion.Mainnet
    chainId = ChainID.Mainnet

    def __init__(self, opts={}):
        super().__init__({
            'url': opts.get('url', HIRO_MAINNET_DEFAULT),
            'fetchFn': opts.get('fetchFn'),
        })


class StacksTestnet(StacksNetwork):
    version = TransactionVersion.Testnet
    chainId = ChainID.Testnet

    def __init__(self, opts={}):
        super().__init__({
            'url': opts.get('url', HIRO_TESTNET_DEFAULT),
            'fetchFn': opts.get('fetchFn'),
        })


class StacksMocknet(StacksNetwork):
    version = TransactionVersion.Testnet
    chainId = ChainID.Testnet

    def __init__(self, opts={}):
        super().__init__({
            'url': opts.get('url', HIRO_MOCKNET_DEFAULT),
            'fetchFn': opts.get('fetchFn'),
        })


StacksDevnet = StacksMocknet