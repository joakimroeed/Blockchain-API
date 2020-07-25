# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 10:27:38 2020

@author: joakimroeed
"""


# Import libraries
#from flask import Flask, jsonify
import json
import hashlib
import datetime
from urllib.parse import urlparse
import requests
#import api

# Building our blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transaction = []
        self.create_block(proof = 1, previous_hash = '0') # Genesis block
        self.nodes = set()
        
    def create_block(self, proof, previous_hash):
        
        # Creating a new block in the blockchain
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transaction': self.transaction
        }
        
        transaction = [] # Resetting the current list of transaction
        
        self.chain.append(block)
        
        return block
        
    def previous_block(self):
        return self.chain[-1] # -1 returns the last element
    
    
    
    def new_transaction(self, sender, recipient, amount):
        # Appends a new transaction into the next mined block
        self.transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
        
        previous_block = self.previous_block()
        return previous_block['index'] + 1 
    
    
    def new_node(self, address):
        parsed_url = urlparse(address)
        self.node.add(parsed_url.netloc) # Append parsed url to the set of nodes
    
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.join()['length']
                chain = response.join()['chain']
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
    def proof_of_work(self, previous_proof):
        proof = 1
        check_proof = False
        while check_proof == False:
            hash_op = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_op[:4] == '0000':
                check_proof = True
            else:
                proof += 1
        return proof
                

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


    def valid_chain(self, chain):
        previous_block = chain[0]
        block_index = 1
    
        while block_index < len(chain):
            block = chain[block_index]
            
            # Checking to see if the previous hash of the current block is different than the hash of the previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Checking to see if the proof of each block is valid,
            # that the proof of the previous and current block starts with 4 leading zeros
            previous_proof = previous_block['proof']
            current_proof = block['proof']      
            hash_op = hashlib.sha256(str(current_proof**2 - previous_proof**2)).encode().hexdigest()
            if hash_op[:4] != '0000':
                return False
            previous_block = block # previous block is now equal to current block
            block_index += 1
        return True
            






