# Lab 3: Public Key Cryptography Implementation

- In this lab I will learn about asymmetric key (public key) cryptography. I will implement the Diffie-Hellman Key Exchange protocol and RSA ecryption scheme.

  - I will explore the properties of these schemes to see how naive approaches to these implementations can lead to insecurity

## Task 1: Implementing the Diffie-Hellman Key Exchange Protocol

### Initial Setup

1. **Create Public Parameters:**
   - The two people sending & receiving ecrypted messages (Alice & Bob) must agree on a large prime number \(q\) and a base (alpha)
   - These parameters are made public and can be transferred openly.

### Key Creation Process

2. **Private and Public Keys:**

   - **Private Key:** Each person must pick a random 2048 bit number \(X_A\) as their private key, which will be kept a secret.
     - This key must not leave the machine it was created on.
   - **Public Key:** Each person must also have a public key that is avalable to the public. This will be computed using alpha^X_sender \* mod q

   ```
   def generate_private_and_public(alpha, q):
      private_key = random.randint(1, 2**2048)
      public_key = pow(alpha, private_key, q)
      return {"private": private_key, "public": public_key}
   ```

### Generating the Shared Secret

3. Each prerson must generate their shared key which should be equal to each others.
   - Compute the shared secret by raising the other party's public key to the power of their own private \* modulo q
   ```
   def compute_shared_secret(other_public_key, private_key, q):
      """Compute the shared secret using the other's public key and your private key."""
      return power_modulo(other_public_key, private_key, q)
   ```

### Deriving a Symmetric Key

4. Both parties must also hash the shared secret using SHA256 and truncate the output ti 16 bytes, so it can be used to AES-CBC encrypt the messages sent.

   ```
   def derive_symmetric_key(shared_secret):
      """Hash the shared secret and truncate to derive the AES key."""
      hasher = sha256()
      hasher.update(shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, byteorder='big'))
      return hasher.digest()[:16]
   ```

### Message Encryption and Transmission

5. Using the symmetric key to encrypt messages with AES in CBC mode

   ```
    ciphertext = encrypt_with_cbc_mode(plaintext.encode('utf-8'), sender_symmetric_key, iv)
    decrypted_text = decrypt_with_cbc_mode(ciphertext, sender_symmetric_key, iv)
   ```

---

## Task 2: Implement Man-in-the-Middle Attack
