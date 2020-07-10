# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:54:04 2020

@author: joakimroeed
"""
# Importing necessary dependencies
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binasci


class Wallet:
    
    def __init__(self, node_id):
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key