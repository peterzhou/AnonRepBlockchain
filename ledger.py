class Ledger:
    def __init__(self):
        # each block is a dictionary as follows:
        '''
            {
                "Sender": pseudonym or ID of the user that is sending the reputation points
                "Receiver": pseudonym or ID of the user that is receiving the reputation points
                "Points": the amount of reputation points that is being sent
            }
        '''
        self.blocks = []
        self.awaiting = []

    def send_reputation(self, sender, receiver, amount):
        '''

        '''
        new_block = {
            "Sender": sender,
            "Receiver": receiver,
            "Points": amount
        }
        return self.propose_block(new_block)

    def propose_block(self, new_block):
        # verify that the transaction of the block is legal by looking at the history of the chain
        sender_value = 0
        for block in self.blocks:
            if block["Sender"] == new_block["Sender"]:
                sender_value -= block["Points"]
            if block["Receiver"] == new_block["Sender"]:
                sender_value += block["Points"]

        if sender_value >= new_block["Points"]:
            self.awaiting.append(new_block)
            return True
        else:
            return False
        # ledger needs to be broadcasted

    def sign_block(self, new_block):
        '''
            should be called by the server so that the results can be broadcasted 
            We can make this signing as easy as possible
        '''
        signature = None
        return signature

    def _verify_signature(self, new_block, signature):
        '''
            We can make this crypto as easy or as difficult as we want
        '''
        print("Automatic signature approval")
        return True

    def _append_block(self, new_block, signature):
        # verify legality of block
        if self.verify_signature(new_block, signature):
            self.blocks.append(new_block)
        # ledger needs to be broadcasted