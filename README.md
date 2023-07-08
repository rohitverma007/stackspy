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
