from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Step 1: Key and IV Generation
def create_secret_key_and_iv():
    # This will generate the secrets we need: a key and an IV
    secret_key = get_random_bytes(16)  # 128 bits are equal to 16 bytes
    iv = get_random_bytes(16)
    return secret_key, iv

# Step 2: PKCS#7 Padding
def apply_pkcs7_padding(msg):
    # Padding is necessary for msgs not a multiple of block size
    block_length = 16  # AES block size in bytes
    padding_amount = block_length - len(msg) % block_length
    if padding_amount == 0:
        padding_amount = block_length
    padding = bytes([padding_amount] * padding_amount)
    return msg + padding

# Step 3: XOR Operation for CBC Mode
def perform_xor(a, b):
    # Useful for CBC mode where we need to XOR the plaintext with the previous ciphertext
    return bytes(x ^ y for x, y in zip(a, b))

# Step 4: ECB Encryption
def encrypt_with_ecb_mode(plain_text, secret_key):
    # ECB mode encryption one block at a time
    cipher_machine = AES.new(secret_key, AES.MODE_ECB)
    ready_text = apply_pkcs7_padding(plain_text)
    encrypted_msg = b''
    for i in range(0, len(ready_text), 16):
        block = ready_text[i:i+16]
        encrypted_msg += cipher_machine.encrypt(block)
    return encrypted_msg

# Step 5: CBC Encryption
def encrypt_with_cbc_mode(plain_text, secret_key, iv):
    # CBC mode encryption, where each block depends on the previous one
    cipher_machine = AES.new(secret_key, AES.MODE_ECB)
    ready_text = apply_pkcs7_padding(plain_text)
    previous_cipher_block = iv
    encrypted_msg = b''
    for i in range(0, len(ready_text), 16):
        block = ready_text[i:i+16]
        block_for_encryption = perform_xor(previous_cipher_block, block)
        cipher_block = cipher_machine.encrypt(block_for_encryption)
        encrypted_msg += cipher_block
        previous_cipher_block = cipher_block
    return encrypted_msg

# Step 6: BMP File Encryption
def encrypt_bmp_img(img_path, secret_key, iv, encryption_mode='ECB'):
    # Handles the BMP file encryption
    with open(img_path, 'rb') as img_file:
        bmp_header = img_file.read(54)  # BMP header length
        img_body = img_file.read()

    if encryption_mode == 'ECB':
        encrypted_body = encrypt_with_ecb_mode(img_body, secret_key)
    elif encryption_mode == 'CBC':
        encrypted_body = encrypt_with_cbc_mode(img_body, secret_key, iv)
    else:
        raise ValueError("Please choose either 'ECB' or 'CBC' for the encryption mode.")

    encrypted_img_path = f"../imgs/encrypted/_{encryption_mode.lower()}.bmp"
    with open(encrypted_img_path, 'wb') as encrypted_img_file:
        encrypted_img_file.write(bmp_header)  # Preserve original header
        encrypted_img_file.write(encrypted_body)  # Append encrypted body

    print(f"Encrypted img created at: {encrypted_img_path}")

def main():
    # Define the path to the img you're encrypting
    img_path = "../imgs/cp-logo.bmp"

    # Generating the secrets
    secret_key, iv = create_secret_key_and_iv()
    print("Generated Secret Key:", secret_key.hex())
    print("Generated IV:", iv.hex())

    # Testing with a sample msg
    msg = b"Symmetric Encryption Rocks!"
    print("\nOriginal msg:", msg)

    encrypted_msg_ecb = encrypt_with_ecb_mode(msg, secret_key)
    print("ECB Encrypted msg:", encrypted_msg_ecb.hex())

    encrypted_msg_cbc = encrypt_with_cbc_mode(msg, secret_key, iv)
    print("CBC Encrypted msg:", encrypted_msg_cbc.hex())

    # Encrypting the BMP img
    encrypt_bmp_img(img_path, secret_key, iv, 'ECB')
    encrypt_bmp_img(img_path, secret_key, iv, 'CBC')

if __name__ == "__main__":
    main()
