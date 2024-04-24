from Crypto.Util.number import getPrime

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_euclidean(a, b):
    if b == 0:
        return a, 1, 0  
    
    x2, x1 = 1, 0
    y2, y1 = 0, 1
    
    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1

        a, b = b, r
        x2, x1 = x1, x
        y2, y1 = y1, y

    return a, x2, y2

def mod_inverse(e, phi):
    gcd, x, _ = extended_euclidean(e, phi)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi

def generate_rsa_keys(bit_length, e=65537):
    p = getPrime(bit_length)
    q = getPrime(bit_length)
    if p == q:
        q = getPrime(bit_length)  # Ensure p and q are distinct
    n = p * q
    phi_n = (p - 1) * (q - 1)

    while gcd(e, phi_n) != 1:
        p = getPrime(bit_length)
        q = getPrime(bit_length)
        n = p * q
        phi_n = (p - 1) * (q - 1)

    d = mod_inverse(e, phi_n)
    return ((n, e), d)

def rsa_encrypt(public_key, plaintext):
    n, e = public_key
    # Convert plaintext string to an integer
    m = int.from_bytes(plaintext.encode('utf-8'), 'big')
    if m >= n:
        raise ValueError("Plaintext too long for key size")
    c = pow(m, e, n)
    return c

def rsa_decrypt(private_key, public_key, ciphertext):
    n, e = public_key
    d = private_key
    m = pow(ciphertext, d, n)
    plaintext = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode('utf-8')
    return plaintext

def main():
    # Generate the Public & Private Keys
    public_key, private_key = generate_rsa_keys(1024)
    print("Public Key: (n, e) =", public_key)
    print("Private Key: d =", private_key)

    # Encrypt and Decrypt the Message using Public Key-Encryption
    message = "Plain Text!"
    ciphertext = rsa_encrypt(public_key, message)
    decrypted_message = rsa_decrypt(private_key, public_key, ciphertext)
    print("Ciphertext:", ciphertext)
    print("Decrypted Message:", decrypted_message)


if __name__ == "__main__":
    main()