from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from helpers import apply_pkcs7_padding, perform_xor, create_secret_key_and_iv, binary_to_printable_hex

# CBC Encryption
def encrypt_with_cbc_mode(plain_text, secret_key, iv):
    # CBC mode encryption, where each block depends on the previous one
    cipher_machine = AES.new(secret_key, AES.MODE_ECB)
    ready_text = apply_pkcs7_padding(plain_text)
    previous_cipher_block = iv
    encrypted_msg = b''
    for i in range(0, len(ready_text), 16):
        # a. Set the current block as the next sub array
        block = ready_text[i:i+16]
        # b. XOR our current block with the previous encryped block
        block_for_encryption = perform_xor(previous_cipher_block, block)
        # c. Encrypt this block now as our new cipher block
        cipher_block = cipher_machine.encrypt(block_for_encryption)
        # d. Append the cipher block to our encrypted message
        encrypted_msg += cipher_block
        # e. Assign our new previous block to the cipher block just created to prepare for the next interations
        previous_cipher_block = cipher_block
    return encrypted_msg

def decrypt_with_cbc_mode(cipher_text, secret_key, iv):
    """Decrypt a message encrypted using CBC mode."""
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return plain_text