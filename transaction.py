"""Provides transactions helper modules"""


from collections import OrderedDict
from utility.printable import  Printable

class Transaction(Printable):
    """A transaction class which will add a transaction to a block in the blockchain """

    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        # Converts this transaction into an OrderedDict
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])

