"""Provides verification helper methods"""

from utility.hash_utilities import hash_block, hash_string_256
from wallet import Wallet

class Verification:

    @staticmethod                                       # we only use passed variables and do not use class attributes
    def valid_proof(transactions, last_hash, nonce):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(nonce)).encode()
        guess_hash = hash_string_256(guess)  # cannot just pass in because we need to add proof and not just the block
        # print(guess_hash)                     # prints all the guess hashes
        return guess_hash[0:2] == '00'  # Our condition for a valid hash

    @classmethod                            # will use class attributes
    def validate_chain(cls, blockchain):
        for (index, block) in enumerate(blockchain):  # enumerate returns the index and value of the element
            if index == 0:  # we dont want to validate the genesis block
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash,
                               block.proof):  # we remove the rewards transactions because we calculate proof of work before including it
                print('proof of work is invalid')
                return False
        return True

    @staticmethod                                               # we only use passed variables and do not use class attributes
    def verify_transaction(transaction, get_balance, check_funds = True):
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod                        # will use class attributes
    def verify_all_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx,get_balance,False) for tx in open_transactions])
