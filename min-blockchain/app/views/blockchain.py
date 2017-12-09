from flask import Response
from flask_restful import Resource, request

from app import node_id
from blockchain.blockchain import Blockchain

blockchain = Blockchain()


class Node(Resource):
    def post(self):
        if not request.is_json:
            return Response('', 400)

        req = request.get_json()
        nodes = req.get('nodes')

        if not all([nodes]):
            return Response('', 400)

        if isinstance(nodes, list):
            return Response('Nodes must be a list', 400)

        for node in nodes:
            blockchain.register_node(node)

        return {
            'message': 'New nodes have been added.',
            'nodes': list(blockchain.nodes)
        }, 201


class Chain(Resource):
    def get(self):
        chains = blockchain.chain

        return {
            'chains': chains,
            'length': len(chains)
        }, 200


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
        if not request.is_json:
            return Response('', 400)

        req = request.get_json()
        sender = req.get('sender')
        recipient = req.get('recipient')
        amount = req.get('amount')

        if not all([sender, recipient, amount]):
            return Response('', 400)

        blockchain.new_transaction(sender, recipient, amount)
