import socket
import threading
import uuid
import util
from random import *
from ledger import Ledger

class Client():
    def __init__(self, client_id):
        # I imagined wallets to be a list of dictionaries and each dictionary would have the following:
        # {
        #    "PrivateKey": the key that will be used to sign new messages
        #    "PublicKey": the public key of the wallet
        #    "Reputation": the amount of reputation that the wallet has
        # maybe we want to add another item in here for the wallet's identity
        # }
        self.wallets = []

        # start with 1 wallet with reputation=1 (feel free to change this)
        first_wallet = self.createwallet()
        # maybe we want to publish to the ledger? it's not an important issue, but we want to make sure that we can't just create random wallets out of nowhere
        self.wallets.append(first_wallet)

        # Client ID is just the ID of the port it's on, since we only have 1 client/port
        # Long standing private key
        # I think we're going to need a list of private keys that correspond to the individual wallets
        # ^that should be taken care of by self.wallets 
        self.client_id = client_id
        self.private_key = util.generatePrivateKey()
        self.public_key = util.generatePublicKey(self.private_key)

        self.threshold = 1 # the maximum amount of reputation a wallet is allowed to have

        self.my_ledger = Ledger()
        print("Client ID: ", self.client_id)
        print("Client public key: ", self.public_key)
        print("Client private key: ", self.private_key)

    # Called by the server, returns a list of new wallets
    # the private keys will be kept by the client, but the public keys will be shared with the server
    def split(self, walletid):

        # I'm assuming that walletid is the oldwallet that needs to be split
        # maybe we should be looping through all the wallets that the client has and calling a split on all of them
        oldwallet = None #TODO @Eugine - once you figure createwallet out find out how to get the wallet by reference
        new_wallets = []

        # do some kind of signing with the privatekey of the oldwallet
        signed_oldwallet = oldwallet["PrivateKey"] # we obviously do NOT want to send the private key
        while oldwallet['Reputation'] > self.threshold:
            newwallet = self.createwallet()
            # TODO: Split currency among the new wallets

            # transfer threshold reputation points from oldwallet to newwallet
            self.my_ledger.send_reputation(signed_oldwallet, newwallet["PublicKey"], self.threshold)
            # make sure that the server is publishing/broadcasting the new updated ledger with this change
            newwallet["Reputation"] += self.threshold
            new_wallets.append(newwallet)

        return new_wallets

    # Adds the wallet to the dictionary. Returns the key for the wallet in the dict
    def createwallet(self):
        # TODO @Eugine: Add in crypto code for initializing wallets - the way I
        # imagined it was a mapping of either publickey/privatekey/address to currency amt
        # maybe we can have currency be determined elsewhere

        # 1. make private and public key and maybe some ID
        private_key = util.generatePrivateKey()
        public_key = util.generatePublicKey(private_key)
        reputation = 1 # going to leave reputation empty, so that transfer of reputation points can be handled elsewhere

        wallet = {
            "private_key": private_key,
            "public_key": public_key,
            "reputation": reputation
        }
        return wallet

    def generate_signed_messages(self, message_text):
        # TODO: get last_highest_rep from coordinator and choose amount of reputation to use
        signed_messages = []

        # currently use all reputation
        for wallet in self.wallets:
            message_dict = {
                "text": message_text,
                "signature": wallet["private_key"]
                # TODO: not sure we need to add a nym here? isn't the signature sufficient?
                #"nym" =
            }
            signed_messages.append(message_dict)
        return signed_messages
