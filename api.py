# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 20:13:35 2020

@author: joakimroeed
"""


# Import libraries
from flask import Flask, jsonify, request
import json
import hashlib
import datetime
from uuid import uuid4
import blockchain



# Web API

app = Flask(__name__)


# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


# Creating a blockchain

blockchain = blockchain.Blockchain()


# Mine a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender = "0",
        recipient = node_identifier,
        amount = 1
    )
    
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous hash': block['previous_hash'],
        'transaction': block['transaction']
    }
    
    return jsonify(response), 200 


@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    
    return jsonify(response), 200


@app.route('/status', methods = ['GET'])
def status():
    valid = blockchain.valid_chain(blockchain.chain)
    if valid:
        response = {
            'message': 'The blockchain is valid.'    
        }
    else:
        response = {
            'message': 'Houston, we have a problem. The Blockchain is not valid.'   
        }
    return jsonify(response), 200


@app.route('/transaction', methods = ['POST'])
def transaction():
    data = request.get_json()
    
    required = [
        'sender',
        'recipient',
        'amount'
    ]
    
    # Checking to see if all the required data has been given
    if not all(k in data for k in required):
        return 'Missing data', 400
    
    # Create a new transaction
    index = blockchain.new_transaction(data['sender'], data['recipient'], data['amount'])

    response = {
        'message': f'The new transaction has been added to block {index}'    
    }

    return jsonify(response), 201


app.run(host = '0.0.0.0', port = 5000)



