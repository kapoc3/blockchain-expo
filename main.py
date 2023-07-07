#author: kapoc 2023
#single blockchain application for demo purpopose
from hashlib import sha256
from Crypto.PublicKey import RSA


class Transaction:
    def __init__(self, sender, receiver, amount, extradata):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.extradata = extradata


    def to_string(self):
        return f'sender: {self.sender}- receiver: {self.receiver}- ammount: {self.amount}- extradata: {self.extradata}'


class Block:
    def __init__(self, previous_hash, transactions):
        self.previous_hash = previous_hash
        self.transactions = transactions

    #create digital identification for object
    def calculate_hash(self):
        transaction_strings = [transaction.to_string()
                               for transaction in self.transactions]
        print(f'transaction strings: {transaction_strings}')
        block_string = f'{self.previous_hash}-{"".join(transaction_strings)}'
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def create_genesis_block(self):
        genesis_block = Block(previous_hash="0", transactions=[])
        self.chain.append(genesis_block)

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_block(self):
        previous_block = self.chain[-1]
        transactions = list(self.pending_transactions)
        new_block = Block(
            previous_hash=previous_block.calculate_hash(), transactions=transactions)
        self.chain.append(new_block)
        self.pending_transactions = []

    def print_chain(self):
        for i, block in enumerate(self.chain):
            print(f'Block {i + 1}')
            print(f'Previous Hash: {block.previous_hash}')
            print(
                f'Transactions: {", ".join([transaction.to_string() for transaction in block.transactions])}')
            print(f'Block Hash: {block.calculate_hash()}')
            print()

    def get_balance(self, public_key):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == public_key:
                    balance -= transaction.amount
                if transaction.receiver == public_key:
                    balance += transaction.amount
        return balance


# Generate a new RSA key pair
key_pair = RSA.generate(2048)
private_key = key_pair.export_key().decode()
public_key = key_pair.publickey().export_key().decode()

# Create a blockchain instance
blockchain = Blockchain()
blockchain.create_genesis_block()

# Example usage:
transaction1 = Transaction(sender=public_key, receiver="address1", amount=10, extradata="another information into 1 transaction")
transaction2 = Transaction(sender=public_key, receiver="address2", amount=5, extradata="sensible data to sign into transaction")
blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)
blockchain.mine_block()
blockchain.print_chain()

transaction3 = Transaction(sender=public_key, receiver="address3", amount=10, extradata="new transaction")
blockchain.add_transaction(transaction3)
blockchain.mine_block()
blockchain.print_chain()

# Get the balance of the public key
balance = blockchain.get_balance(public_key)
print(f'Balance for public key {public_key}: {balance}')
