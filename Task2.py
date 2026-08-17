import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

vehicles = {}

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()
latest_signature = None
signed_message = None


def generate_sha256():
    """1. SHA-256 Hashing"""
    msg = input("\nEnter message to hash: ")
    hashed_msg = hashlib.sha256(msg.encode()).hexdigest()
    print(f"SHA-256 Hash: {hashed_msg}")


def digital_signature_menu():
    """2. Digital Signature System"""
    global latest_signature, signed_message
    print("\n--- Digital Signature System ---")
    print("1. Sign a Message")
    print("2. Verify Signature")
    choice = input("Enter choice (1-2): ")

    if choice == '1':
        signed_message = input("Enter message to sign: ")
        latest_signature = private_key.sign(
            signed_message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Message signed successfully!")
        print(f"Signature (hex): {latest_signature.hex()[:50]}...")

    elif choice == '2':
        if latest_signature is None:
            print("Error: No signed message found! Sign a message first.")
            return
        
        # Verify using public key
        try:
            public_key.verify(
                latest_signature,
                signed_message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("Signature Verification SUCCESSFUL! (Valid Signature)")
        except Exception:
            print("Signature Verification FAILED! (Invalid Signature)")
    else:
        print("Invalid choice.")


def register_vehicle():
    """3. Vehicle Registration System - Store"""
    print("\n--- Register Vehicle ---")
    plate = input("Enter Number Plate (e.g., DL01AB1234): ").strip().upper()
    
    if plate in vehicles:
        print(f"Error: Vehicle with number plate '{plate}' is already registered!")
        return

    owner = input("Enter Owner Name: ").strip()
    model = input("Enter Car Model: ").strip()

    if not owner or not model or not plate:
        print("Error: All fields are required!")
        return

    vehicles[plate] = {"owner": owner, "model": model}
    print(f"Vehicle '{plate}' registered successfully!")


def retrieve_vehicle():
    """3. Vehicle Registration System - Get"""
    print("\n--- Retrieve Vehicle Details ---")
    plate = input("Enter Number Plate: ").strip().upper()

    if plate in vehicles:
        details = vehicles[plate]
        print(f"\nDetails for {plate}:")
        print(f"Owner Name: {details['owner']}")
        print(f"Car Model : {details['model']}")
    else:
        print(f"Error: No vehicle found with number plate '{plate}'.")


def main():
    while True:
        print("\n==================================")
        print(" BLOCKCHAIN & CRYPTO ASSIGNMENT ")
        print("==================================")
        print("1. Generate SHA-256 Hash")
        print("2. Digital Signature (Sign/Verify)")
        print("3. Register Vehicle")
        print("4. Retrieve Vehicle Details")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")

        if choice == '1':
            generate_sha256()
        elif choice == '2':
            digital_signature_menu()
        elif choice == '3':
            register_vehicle()
        elif choice == '4':
            retrieve_vehicle()
        elif choice == '5':
            print("Exiting program... Bye!")
            break
        else:
            print("Invalid choice! Please select 1 to 5.")


if __name__ == "__main__":
    main()
