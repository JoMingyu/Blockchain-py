from uuid import uuid4

from flask import Response
from flask_restful import Resource, request

from blockchain.blockchain import Blockchain

blockchain = Blockchain()


class Node(Resource):
    def post(self):
        """
        Add new node to blockchain
        """
        node_id = blockchain.register_node(request.host)

        return {
            'message': 'New node have been added.',
            'node_id': node_id,
            'nodes': list(blockchain.nodes)
        }, 201


class Chain(Resource):
    def get(self):
        """
        Returns blockchain
        """
        chains = blockchain.chain

        return {
            'chains': chains,
            'length': len(chains)
        }, 200


class Mine(Resource):
    def post(self):
        if not request.is_json:
            return Response('', 400)

        req = request.get_json()
        node_id = req.get('node_id')

        if not all([node_id]):
            return Response('', 400)

        if node_id not in blockchain.nodes:
            return Response('Invalid node id', 400)

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

        if sender not in blockchain.nodes or recipient not in blockchain.nodes:
            return Response('Invalid sender id or recipient id', 400)

        blockchain.new_transaction(sender, recipient, amount)

        return Response('', 201)
