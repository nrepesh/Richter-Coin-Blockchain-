"""Provides hashing utility functions"""

import json  # Javascript library to hold complex data structures
import hashlib as hl

#__all__ = ['hash_string_2560', 'hash_block']

def hash_string_256(string):
    return hl.sha256(string).hexdigest()            # easier to return as it calls hexdigest() here

def hash_block(block):
    # Order in dictionary is not permanent so it can change and it can the hash, sort_keys solves it
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())  # use encode to convert to UTF-8 used by SHA 256
# hexdigest() converts to string again