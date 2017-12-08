import hashlib
import json
from time import time
from urllib.parse import urlparse


class Blockchain:
    DEFAULT_VERSION = '1.0'

    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create genesis block
        self.new_block(100, '1')

    def register_node(self, address):
        self.nodes.add(urlparse(address).netloc)

    def new_block(self, nonce, prevhash):
        """
        Creates new block

        :param nonce: Block's nonce
        :param prevhash: Previous block's hash
        :return: Created block
        """
        block = {
            'version': self.DEFAULT_VERSION,
            'prevhash': prevhash or self.hash_block(self.chain[-1]),
            'transactions': self.current_transactions,
            # Change to merkle tree is better
            'timestamp': time(),
            'nonce': nonce
            # bits, hash required
        }

        self.current_transactions.clear()
        # Clear transactions to generate new block
        self.chain.append(block)
        # Append block to chain

        return block

    @staticmethod
    def hash_block(block):
        block_str = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_str).hexdigest()

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_nonce):
        """
        POW Mining

        :param last_nonce: Last block's nonce
        :return: nonce
        """
        nonce = 0
        while self.is_valid_nonce(last_nonce, nonce) is False:
            nonce += 1

        return nonce

    @staticmethod
    def is_valid_nonce(last_nonce, nonce):
        guess = '{0}{1}'.format(last_nonce, nonce).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == '0000'
