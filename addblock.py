import hashlib
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.transactions_hash = self.compute_transactions_hash()
        self.hash = self.compute_hash()

    def compute_transactions_hash(self):
        """
        Computes a hash based on the block's transactions.
        Useful for verifying transaction integrity.
        """
        transactions_string = "".join(self.transactions)
        return hashlib.sha256(transactions_string.encode()).hexdigest()

    def compute_hash(self):
        """
        Computes the main hash of the block.
        Includes the transactions hash.
        """
        block_string = f"{self.index}{self.timestamp}{self.previous_hash}{self.nonce}{self.transactions_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    difficulty = 4  # Number of leading zeros required in the hash

    def __init__(self):
        self.unconfirmed_transactions = []  # Data yet to be added to blocks
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generates the genesis (first) block and adds it to the chain.
        """
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)

    def add_block(self, block):
        """
        Adds a block to the chain after validation.
        """
        if self.chain and block.previous_hash != self.chain[-1].hash:
            return False

        if not self.is_valid_proof(block):
            return False

        self.chain.append(block)
        return True

    def is_valid_proof(self, block):
        """
        Validates the proof-of-work for a block.
        """
        return block.hash.startswith('0' * self.difficulty) and block.hash == block.compute_hash()

    def proof_of_work(self, block):
        """
        Proof-of-Work: Increment the nonce until the hash satisfies the difficulty.
        """
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()
        return block.hash

    def add_new_transaction(self, transaction):
        """
        Adds a transaction to the list of unconfirmed transactions.
        """
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        Mines the unconfirmed transactions, creating a new block.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.chain[-1]
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            timestamp=time.time(),
            previous_hash=last_block.hash,
        )

        new_block.hash = self.proof_of_work(new_block)
        self.add_block(new_block)
        self.unconfirmed_transactions = []
        return new_block


# Example Usage
if __name__ == "__main__":
    blockchain = Blockchain()

    # Add transactions
    blockchain.add_new_transaction("Alice pays Bob 10 BTC")
    blockchain.add_new_transaction("Bob pays Charlie 5 BTC")

    # Mine a block
    print("Mining...")
    mined_block = blockchain.mine()
    if mined_block:
        print(f"Block {mined_block.index} mined with hash: {mined_block.hash}")
        print(f"Transactions Hash: {mined_block.transactions_hash}")

    # Display the blockchain
    print("\nBlockchain:")
    for block in blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Transactions Hash: {block.transactions_hash}, Transactions: {block.transactions}")