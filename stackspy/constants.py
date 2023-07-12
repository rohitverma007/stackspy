from enum import Enum

class ChainID(Enum):
  Testnet = 0x80000000
  Mainnet = 0x00000001

class TransactionVersion(Enum):
  Mainnet = 0x00
  Testnet = 0x80