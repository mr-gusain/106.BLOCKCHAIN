import hashlib
import time

class Block:
    def __init__(self, index, votes, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.votes = votes
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    # hash function - work
    def calculate_hash(self):
        block_content = f"{self.index}{self.timestamp}{self.votes}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    # mine_block -  working 
    def mine_block(self, difficulty=2):
        
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"⛏️ Block #{self.index} Mined Successfully! Hash: {self.hash}")


class BlockchainVotingSystem:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.registered_voters = {}  
        self.candidates = {"Candidate A": 0, "Candidate B": 0, "Candidate C": 0}
        self.difficulty = 2

    def create_genesis_block(self):
        genesis_block = Block(0, "Genesis Block - Voting System Initialized", "0")
        genesis_block.mine_block(2)
        return genesis_block

    def get_latest_block(self):
        return self.chain[-1]

    def register_voter(self, voter_id):
        if voter_id in self.registered_voters:
            print(f"\n⚠️ Voter ID '{voter_id}' is already registered!")
            return
        self.registered_voters[voter_id] = False
        print(f"\n👤 Voter '{voter_id}' registered successfully!")

    def cast_vote(self, voter_id, candidate):
        if voter_id not in self.registered_voters:
            print("\n❌ Error: Voter ID not registered! Register first.")
            return False

        if self.registered_voters[voter_id]:
            print("\n🚫 Error: You have already voted!")
            return False

        if candidate not in self.candidates:
            print("\n❌ Error: Invalid Candidate selection!")
            return False

        
        self.registered_voters[voter_id] = True
        self.candidates[candidate] += 1

       
        voter_hash = hashlib.sha256(voter_id.encode()).hexdigest()[:10]
        vote_data = {"voter_hash": voter_hash, "candidate": candidate}

        new_block = Block(
            index=len(self.chain),
            votes=vote_data,
            previous_hash=self.get_latest_block().hash
        )
        print("\n⏳ Mining new block for your vote...")
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        print(f"✅ Vote successfully recorded for {candidate}!")
        return True

    def display_results(self):
        print("\n" + "="*35)
        print("      📊 LIVE ELECTION RESULTS      ")
        print("="*35)
        for candidate, votes in self.candidates.items():
            print(f"• {candidate}: {votes} votes")
        print("="*35)

    def print_chain(self):
        print("\n" + "="*50)
        print("            🔗 BLOCKCHAIN LEDGER            ")
        print("="*50)
        for block in self.chain:
            print(f"Block Index   : #{block.index}")
            print(f"Timestamp     : {time.ctime(block.timestamp)}")
            print(f"Data/Votes    : {block.votes}")
            print(f"Previous Hash : {block.previous_hash}")
            print(f"Current Hash  : {block.hash}")
            print(f"Nonce         : {block.nonce}")
            print("-" * 50)

    def verify_integrity(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False, f"Block #{current.index} data has been tampered!"

            if current.previous_hash != previous.hash:
                return False, f"Block #{current.index} previous hash does not match!"

        return True, "Blockchain integrity verified! No tampering detected."


def run_app():
    voting_system = BlockchainVotingSystem()

    while True:
        print("\n=== BLOCKCHAIN VOTING MANAGEMENT SYSTEM ===")
        print("1. Register Voter")
        print("2. Cast Vote")
        print("3. View Election Results")
        print("4. View Complete Blockchain Ledger")
        print("5. Verify Blockchain Integrity")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            voter_id = input("Enter Voter ID/Aadhar/PAN: ").strip()
            voting_system.register_voter(voter_id)

        elif choice == '2':
            voter_id = input("Enter your Voter ID: ").strip()
            print("Candidates: Candidate A | Candidate B | Candidate C")
            candidate = input("Choose Candidate Name: ").strip()
            voting_system.cast_vote(voter_id, candidate)

        elif choice == '3':
            voting_system.display_results()

        elif choice == '4':
            voting_system.print_chain()

        elif choice == '5':
            is_valid, message = voting_system.verify_integrity()
            if is_valid:
                print(f"\n🟢 {message}")
            else:
                print(f"\n🔴 ALERT: {message}")

        elif choice == '6':
            print("\nThank you for using the Blockchain Voting System!")
            break

        else:
            print("\n❌ Invalid selection! Try again.")

if __name__ == "__main__":
    run_app()