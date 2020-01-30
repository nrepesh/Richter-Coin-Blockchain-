from functools import reduce
import json
import requests
from block import Block
from transaction import Transaction
from utility.verification import Verification
from utility.hash_utilities import hash_block
from wallet import Wallet

MINING_REWARD = 10      # Reward given to miners for validating and creating new block


class Blockchain:
    """Blockchain class manages the chain and open trasnactions"""

    def __init__(self, public_key, node_id):            # Constructor class
        genesis_block = Block(0, '', [], 0, 0)          # The first block of the blockchain
        self.chain = [genesis_block]                    # Initialize our blockchain list
        self.__open_transactions = []
        self.__peer_nodes = set()
        self.public_key = public_key
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        """ Returns a copy of the open transactions list """
        return self.__open_transactions[:]

    def load_data(self):
        try:
            """Initialize blockchain and open transactions data from file"""
            # with open('blockchain.p', mode='rb') as file:   # For Pickle
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as file:
                file_contents = file.readlines()                # List of strings of contents of file
                # file_contents = pickle.loads(file.read())        # PICKLE import
                '''
                blockchain = file_contents['chain']          #Pickle imports 
                open_transactions = file_contents['ot']
                '''
                blockchain = json.loads(file_contents[0][:-1])  # {:-1] for \n
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                                    for tx in block['transactions']]  # we load block here so it will be a dictionary
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'],
                                          block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_contents[1][:-1])
                updated_open_tran = []                        # We convert to OrderedDict
                for tx in open_transactions:
                    updated_tran = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_open_tran.append(updated_tran)
                self.__open_transactions = updated_open_tran
                peer_nodes = json.loads(file_contents[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as file:
                '''
                with open('blockchain.p', mode='wb') as file:
                saves blockchain and open_transactions
                with closes the file automatically
                '''
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp)
                        for block_el in self.__chain]]       # Need to convett the block object inorder to dump in Json
                file.write(json.dumps(saveable_chain))
                file.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                file.write(json.dumps(saveable_tx))
                file.write('\n')
                file.write(json.dumps(list(self.__peer_nodes)))
                '''
                save_data = {           For Pickle 
                    'chain': blockchain,
                    'ot' : open_transactions
                }
                file.write(pickle.dumps(save_data))
                '''
        except IOError:
            print('Saving Failed ')

    def proof_of_work(self):        # Guesses number till the difficulty matches and returns a proof of work number
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        nonce = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, nonce):
            nonce += 1
        return nonce

    def get_balance(self,sender=None):      # Returns balance of participants
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
    # We do this so that we also account for the transactions in open_transactions and not only verify open transactions
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)            # includes all current and on hold transactions
        total_amt_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # This uses lambda to map over the tx_sender list to sum up all transactions sent
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        total_amt_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient,0)
        return total_amt_received-total_amt_sent

    def get_last_value(self):
        """ Returns the last value of the blockchain """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transactions(self, recipient, sender, signature, amount=1.0, is_receiving_broadcast=False):
        """ Appends transaction dictionary of sender recipient and amount to open_transactions.
        transaction = {                     We will use ordered dictionary instead of this
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        """
        # if self.public_key == None:
         # return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving_broadcast:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={'sender': sender, 'recipient': recipient, 'amount': amount, 'signature': signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined, needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):       # To validate the transaction andd add a new block
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # print(proof)                              # prints the nonce value required
        '''
        reward_transaction = {              #Use Ordered dictionary instead
            'sender': 'MINING',
            'recipient': owner,
            'amount': MINING_REWARD
        }
        '''
        reward_transaction = Transaction('MINING', self.public_key,'', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]          # A local copy beacuse of the transaction fails then we still have a copy
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)      # adds the mining rewards to open transaction immediately

        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        '''
        block = OrderedDict([
            ('previous_hash', hashed_block),
            ('index', len(blockchain)),
            ('transactions', copied_transactions),
            ('proof', proof)
        ])
        '''
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):         # Add a block after it has been received to local blockchain
        transactions = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed')
        self.save_data()
        return True

    def resolve(self):              # This resolves conflict by replacing the longest chain
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                response =requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'], block['previous_hash'], [Transaction(
                                tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']],
                                                block['proof'], block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                if node_chain_length > local_chain_length and Verification.validate_chain(node_chain):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:             #Offline
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:                                     # replace will be set true which says there are problems with transactions
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        """Adds a new node to the peer node set."""

        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Removes a new node to the peer node set."""
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Returns a list of all connected peer nodes"""
        return list(self.__peer_nodes)