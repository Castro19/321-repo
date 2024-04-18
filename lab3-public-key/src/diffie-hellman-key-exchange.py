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

def message_exchange(q, alpha):
    alice = generate_private_and_public(alpha, q)
    bob = generate_private_and_public(alpha, q)

    # Alice sends a message to Bob
    alice_shared_secret = compute_shared_secret(bob['public'], alice['private'], q)
    alice_symmetric_key = derive_symmetric_key(alice_shared_secret)
    iv = random.randbytes(16)
    alice_msg = "Hi, Bob!"
    ciphertext = encrypt_with_cbc_mode(alice_msg.encode('utf-8'), alice_symmetric_key, iv)

    # Bob decrypts Alice's message
    bob_shared_secret = compute_shared_secret(alice['public'], bob['private'], q)
    bob_symmetric_key = derive_symmetric_key(bob_shared_secret)
    # In practice, Bob would receive the IV along with the ciphertext
    decrypted_msg = decrypt_with_cbc_mode(ciphertext, bob_symmetric_key, iv)

    # Check if decryption is correct
    assert alice_msg == decrypted_msg.decode('utf-8'), "Decryption failed"
 
    bob_response = "Hi Alice!"
    ciphertext_response = encrypt_with_cbc_mode(bob_response.encode('utf-8'), bob_symmetric_key, iv)

    # Alice decrypts Bob's message
    # Alice must use the same IV that Bob used to encrypt the response
    decrypted_response = decrypt_with_cbc_mode(ciphertext_response, alice_symmetric_key, iv)

    # Check if decryption is correct
    assert bob_response == decrypted_response.decode('utf-8'), "Decryption failed"

    print("Alice's message to Bob decrypted correctly: ", decrypted_msg.decode('utf-8'))
    print("Bob's message to Alice decrypted correctly: ", decrypted_response.decode('utf-8'))


def diffie_hellman_example():
    q = int("B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371", 16)
    alpha = int("A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5", 16)
    message_exchange(q, alpha)

if __name__ == "__main__":
    diffie_hellman_example()
