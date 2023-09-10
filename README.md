# stackspy

Python Library to interact with the Stacks blockchain

Example code to sign messages:

```
message = "Hello Stacks From Python"
encoded_message = encryption.encode_message(message)

# now hash it

hash_object = hashlib.sha256(encoded_message)
hex_dig = hash_object.hexdigest()
print(hex_dig) # df0e4af616093dfbe3dcae834b0482c6f59f5845a1085165c7dc069dbf7a8ab6

key = 'edf9aee84d9b7abc145504dde6726c64f369d37ee34ded868fabd876c26570bc'
signature_data = encryption.sign_message_hash_rsv(hex_dig, key)
print(signature_data)
```

Example code for transactions:

```
from network import StacksTestnet
from transactions import make_stx_token_transfer
network = StacksTestnet()
tx_options = {
    "recipient": 'ST319CF5WV77KYR1H3GT0GZ7B8Q4AQPY42ETP1VPF',
    "sender_key": "b244296d5907de9864c0b0d51f98a13c52890be0404e83f273144cd5b9960eed01",
    "network": network,
    "memo": "hello from python",
    "amount": 10000000 #amount is in micro-STX
}

transaction = make_stx_token_transfer(tx_options)
print(transaction.serialize().hex())
broadcast_result = broadcast_transaction(transaction, 'testnet')
print(broadcast_result.json())
```
