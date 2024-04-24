import random
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from modes import encrypt_with_cbc_mode, decrypt_with_cbc_mode

# Function to compute power modulo (a^b % mod)
def power_modulo(base, exponent, modulus):
    """Compute (base^exponent) % modulus using a fast exponentiation method."""
    return pow(base, exponent, modulus)

def generate_private_and_public(alpha, q):
    private_key = random.randint(1, 2**2048)  
    public_key = power_modulo(alpha, private_key, q)
    return {"private": private_key, "public": public_key}

# Function to compute the shared secret
def compute_shared_secret(other_public_key, private_key, q):
    """Compute the shared secret using the other's public key and your private key."""
    return power_modulo(other_public_key, private_key, q)

# Function to derive a symmetric key from the shared secret
def derive_symmetric_key(shared_secret):
    """Hash the shared secret and truncate to derive the AES key."""
    hasher = sha256()
    hasher.update(shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, byteorder='big'))
    return hasher.digest()[:16]

# Example setup and encryption using Diffie-Hellman and AES-CBC
def diffie_hellman_implementation(q, plaintext, sender, receiver, iv):
    # Compute shared secrets
    sender_shared_secret = compute_shared_secret(receiver["public"], sender["private"], q)
    
    # Derive symmetric keys
    sender_symmetric_key = derive_symmetric_key(sender_shared_secret)
    
    ciphertext = encrypt_with_cbc_mode(plaintext.encode('utf-8'), sender_symmetric_key, iv)
    decrypted_text = decrypt_with_cbc_mode(ciphertext, sender_symmetric_key, iv)

    print("Encrypted:", ciphertext.hex())
    print("Decrypted:", decrypted_text.decode('utf-8'))  # Ensure the decrypted text matches the original plaintext

def message_exchange_mitm_attack(q, alpha):
    # Mallory's intervention - sending q instead of the public keys
    def mallory_send_q_instead(public_key):
        return q

    # Generate keys for Alice, Bob, and Mallory (though Mallory doesn't need them for this attack)
    alice = generate_private_and_public(alpha, q)
    bob = generate_private_and_public(alpha, q)

    # Mallory intercepts and replaces the public keys with q
    alice_believes_bobs_public = mallory_send_q_instead(bob['public'])
    bob_believes_alices_public = mallory_send_q_instead(alice['public'])

    # Both Alice and Bob compute the shared secret using the modified public keys (which is now q)
    alice_shared_secret = compute_shared_secret(alice_believes_bobs_public, alice['private'], q)
    bob_shared_secret = compute_shared_secret(bob_believes_alices_public, bob['private'], q)

    # Derive symmetric keys based on the compromised shared secrets
    alice_symmetric_key = derive_symmetric_key(alice_shared_secret)
    bob_symmetric_key = derive_symmetric_key(bob_shared_secret)
    iv = random.randbytes(16)

    # Alice sends a message to Bob
    alice_msg = "Hi, Bob!"
    alice_ciphertext = encrypt_with_cbc_mode(alice_msg.encode('utf-8'), alice_symmetric_key, iv)

    # Bob tries to decrypt Alice's message using the compromised key
    bob_decrypted_msg = decrypt_with_cbc_mode(alice_ciphertext, bob_symmetric_key, iv)

    # Bob sends a response to Alice
    bob_response = "Hi Alice!"
    bob_ciphertext = encrypt_with_cbc_mode(bob_response.encode('utf-8'), bob_symmetric_key, iv)

    # Alice tries to decrypt Bob's message using the compromised key
    alice_decrypted_response = decrypt_with_cbc_mode(bob_ciphertext, alice_symmetric_key, iv)

    print("Alice's message to Bob decrypted correctly: ", bob_decrypted_msg.decode('utf-8'))
    print("Bob's message to Alice decrypted correctly: ", alice_decrypted_response.decode('utf-8'))

    # Now, Mallory can decrypt both messages because she knows the shared secret is predictable
    mallorys_key = derive_symmetric_key(0)  # or derive_symmetric_key(1), depending on the value of q^private_key mod q
    mallory_decrypted_alice = decrypt_with_cbc_mode(alice_ciphertext, mallorys_key, iv)
    mallory_decrypted_bob = decrypt_with_cbc_mode(bob_ciphertext, mallorys_key, iv)

    print("Mallory decrypted Alice's message: ", mallory_decrypted_alice.decode('utf-8'))
    print("Mallory decrypted Bob's message: ", mallory_decrypted_bob.decode('utf-8'))


def message_exchange_mitm_attack_tampered_generator(q, tampered_alpha):
    alice_private_key = random.randint(1, 2**2048)
    bob_private_key = random.randint(1, 2**2048)

    # Mallory sets the generator to 1, q, or q-1
    alice_public_key = power_modulo(tampered_alpha, alice_private_key, q)
    bob_public_key = power_modulo(tampered_alpha, bob_private_key, q)

    # Alice and Bob compute the shared secret using the tampered generator
    alice_shared_secret = power_modulo(bob_public_key, alice_private_key, q)
    bob_shared_secret = power_modulo(alice_public_key, bob_private_key, q)

    # Derive symmetric keys
    alice_symmetric_key = derive_symmetric_key(alice_shared_secret)
    bob_symmetric_key = derive_symmetric_key(bob_shared_secret)
    iv = random.randbytes(16)

    # Encrypt messages
    alice_msg = "Hi, Bob!"
    alice_ciphertext = encrypt_with_cbc_mode(alice_msg.encode('utf-8'), alice_symmetric_key, iv)
    bob_response = "Hi Alice!"
    bob_ciphertext = encrypt_with_cbc_mode(bob_response.encode('utf-8'), bob_symmetric_key, iv)

    # Mallory derives the key
    # If alpha was tampered with to be 1 or q, the shared secret will be 1 or 0 respectively
    mallorys_key = derive_symmetric_key(1) if tampered_alpha == 1 or tampered_alpha == q else derive_symmetric_key(q-1)
    
    # Mallory decrypts the messages
    mallory_decrypted_alice = decrypt_with_cbc_mode(alice_ciphertext, mallorys_key, iv)
    mallory_decrypted_bob = decrypt_with_cbc_mode(bob_ciphertext, mallorys_key, iv)

    print("Mallory decrypted Alice's message: ", mallory_decrypted_alice.decode('utf-8'))
    print("Mallory decrypted Bob's message: ", mallory_decrypted_bob.decode('utf-8'))
    


def mitm_example():
    q = int("B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371", 16)
    alpha = int("A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5", 16)

    print("ATTACK 1: Mallory knowing q")
    message_exchange_mitm_attack(q, alpha)
    
    print("\n---------------------------------------------\n")

    print("ATTACK 2: Mallory knowing alpha")
    tampered_alpha = 1  # or q or q-1
    message_exchange_mitm_attack_tampered_generator(q, tampered_alpha)

if __name__ == "__main__":
    mitm_example()
