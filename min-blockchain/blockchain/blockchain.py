import copy
import json
from hashlib import sha256
from time import time
from urllib.parse import urlparse
from uuid import uuid4


class Blockchain:
    DEFAULT_VERSION = '1.0'

    def __init__(self):
        """
        Initializes Chain, Nodes, Current Transactions
        """
        self.current_transactions = []
        self.chain = []
        self.nodes = dict()

        # Create genesis block
        self.new_block(100, '1')

    def register_node(self, address):
        """
        Registers new full node

        :param address: Host's address

        :return: Node's ID
        :rtype: str
        """
        node_id = str(uuid4()).replace('-', '')
        self.nodes[node_id] = urlparse(address).netloc

        return node_id

    def new_block(self, nonce, prevhash):
        """
        Generates new block

        :param nonce: Block's nonce
        :param prevhash: Previous block's hash

        :return: Created block
        :rtype: dict
        """
        new_block = {
            'version': self.DEFAULT_VERSION,
            'prevhash': prevhash or self.hash_block(self.chain[-1]),
            'transactions': copy.deepcopy(self.current_transactions),
            # Change to merkle tree's hash is better
            'timestamp': time(),
            'nonce': nonce
            # bits, hash required
        }

        self.chain.append(new_block)
        # Append block to chain
        self.current_transactions.clear()
        # Clear transactions to generate new block

        return new_block

    @staticmethod
    def hash_block(block):
        """
        Hashes the block by two times of sha256 algorithm

        :param block: Non-hashed block dictionary
        :type block: dict

        :return: Hashed block's hexdigest
        :rtype: str
        """
        block_str = json.dumps(block, sort_keys=True).encode()

        return sha256(sha256(block_str).digest()).hexdigest()

    def new_transaction(self, sender, recipient, amount):
        """
        Adds new transaction on standby block

        :param sender: Sender's wallet ID of transaction
        :type sender: str
        :param recipient: Recipient wallet ID of transaction
        :type recipient: str
        :param amount: Amount of transaction
        :type amount: int

        :return: None
        :rtype: None
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    @property
    def last_block(self):
        """
        Returns most recent block of chain

        :return: Most recent block of chain
        :rtype: dict
        """
        return self.chain[-1]

    def proof_of_work(self, prev_nonce):
        """
        Finds current block's nonce

        :param prev_nonce: Last block's nonce
        :type prev_nonce: int

        :return: nonce
        :rtype: int
        """
        nonce = 0
        while self.is_valid_nonce(prev_nonce, nonce) is False:
            nonce += 1

        return nonce

    @staticmethod
    def is_valid_nonce(prev_nonce, nonce):
        """
        Checks nonce is valid

        :param prev_nonce: Previous block's nonce
        :param nonce: Current block's nonce

        :return: Whether nonce is valid
        :rtype: bool
        """
        guess = '{0}{1}'.format(prev_nonce, nonce).encode()
        guess_hash = sha256(guess).hexdigest()

        return guess_hash[:5] == '00000'
