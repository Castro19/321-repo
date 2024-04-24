from Crypto.Util.number import getPrime, inverse

def generate_rsa_keys(bit_length):
    e = 65537
    p = getPrime(bit_length)
    q = getPrime(bit_length)    
    while p == q:
        q = getPrime(bit_length)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = inverse(e, phi_n)
    return ((n, e), d)

def rsa_encrypt(public_key, m):
    n, e = public_key
    return pow(m, e, n)

def rsa_decrypt(private_key, public_key, c):
    n, _ = public_key
    d = private_key
    return pow(c, d, n)


def malleability():
    bit_length = 1024
    public_key, private_key = generate_rsa_keys(bit_length)
    message = 123456

    # Alice encrypts a message
    c = rsa_encrypt(public_key, message)

    # Mallory intercepts and modifies the ciphertext
    s = 3
    c_prime = (c * pow(s, public_key[1], public_key[0])) % public_key[0]

    # Alice decrypts the modified ciphertext
    m_prime = rsa_decrypt(private_key, public_key, c_prime)

    # Mallory calculates the original message
    recovered_message = (m_prime * inverse(s, public_key[0])) % public_key[0]

    print("Original message:", message)
    print("Decrypted modified message:", m_prime)
    print("Mallory's recovered message:", recovered_message)

def rsa_signature(message, private_key, n):
    """Create an RSA signature using the private key."""
    return pow(message, private_key, n)

def forge_signature(sig1, sig2, n):
    """Forge a new signature by multiplying two signatures."""
    return (sig1 * sig2) % n

def signature_forgery():
    # Example RSA parameters
    n = 3233  # public modulus
    d = 2753  # private key (in a real scenario, this would not be known to Mallory)
    e = 17    # public exponent

    # Two messages and their RSA signatures
    m1 = 123
    m2 = 456
    sig_m1 = rsa_signature(m1, d, n)
    sig_m2 = rsa_signature(m2, d, n)

    # Mallory forges a signature for m3 = m1 * m2
    m3 = m1 * m2
    forged_sig_m3 = forge_signature(sig_m1, sig_m2, n)

    print("Original Signature for m1:", sig_m1)
    print("Original Signature for m2:", sig_m2)
    print("Forged Signature for m3:", forged_sig_m3)
    print("Verification of forged signature:", pow(forged_sig_m3, e, n) == m3 % n)

def main():
    print("Malleability Example:")
    malleability()

    print("\n-------------------------------------\n")

    print("Signature Forgery Example:")
    signature_forgery()

if __name__ == "__main__":
    main()