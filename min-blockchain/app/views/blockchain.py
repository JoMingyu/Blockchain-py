from flask_restful import Resource, request

from app import node_id
from blockchain.blockchain import Blockchain

blockchain = Blockchain()


class Chain(Resource):
    def get(self):
        chains = blockchain.chain

        return {
            'chains': chains,
            'length': len(chains)
        }


class Mine(Resource):
    def get(self):
        last_block = blockchain.last_block
        nonce = blockchain.proof_of_work(last_block['nonce'])
        # Mine

        blockchain.new_transaction(
            sender='0',
            recipient=node_id,
            amount=1
        )

        previous_hash = blockchain.hash_block(last_block)
        new_block = blockchain.new_block(nonce, previous_hash)
        # Generates new block

        return {
            'message': 'New Block Forged',
            'block': {
                'version': new_block['version'],
                'transactions': new_block['transactions'],
                'timestamp': new_block['timestamp'],
                'nonce': new_block['nonce']
            }
        }, 200


class Transaction(Resource):
    def post(self):
        sender = request.form['sender']
        recipient = request.form['recipient']
        amount = request.form['amount']

        blockchain.new_transaction(sender, recipient, amount)
