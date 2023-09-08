from enum import Enum

class ChainID(Enum):
  Testnet = 0x80000000
  Mainnet = 0x00000001

class TransactionVersion(Enum):
  Mainnet = 0x00
  Testnet = 0x80

class PubKeyEncoding(Enum):
  Compressed = 0x00
  Uncompressed = 0x01  

class AuthType(Enum):
  Standard = 0x04
  Sponsored = 0x05

class AnchorMode(Enum):
  OnChainOnly = 0x01
  OffChainOnly = 0x02
  Any = 0x03

RECOVERABLE_ECDSA_SIG_LENGTH_BYTES = 65