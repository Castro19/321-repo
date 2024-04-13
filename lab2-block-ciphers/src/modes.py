from Crypto.Cipher import AES
from helpers import apply_pkcs7_padding, perform_xor, create_secret_key_and_iv, binary_to_printable_hex

# ECB Encryption
def encrypt_with_ecb_mode(plain_text, secret_key):
    # ECB mode encryption one block at a time
    cipher_machine = AES.new(secret_key, AES.MODE_ECB)

    ready_text = apply_pkcs7_padding(plain_text)

    encrypted_msg = b''
    for i in range(0, len(ready_text), 16):
        block = ready_text[i:i+16]
        encrypted_msg += cipher_machine.encrypt(block)
    return encrypted_msg

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

#  BMP File Encryption
def encrypt_bmp_img(img_path_input, img_path_output, secret_key, iv, encryption_mode='ECB'):
    # Handles the BMP file encryption
    with open(img_path_input, 'rb') as img_file:
        bmp_header = img_file.read(54)  # BMP header length
        img_body = img_file.read()

    if encryption_mode == 'ECB':
        encrypted_body = encrypt_with_ecb_mode(img_body, secret_key)
    elif encryption_mode == 'CBC':
        encrypted_body = encrypt_with_cbc_mode(img_body, secret_key, iv)
    else:
        raise ValueError("Please choose either 'ECB' or 'CBC' for the encryption mode.")
    img_path_output = img_path_output + f'_{encryption_mode}.bmp'
    with open(img_path_output, 'wb') as encrypted_img_file:
        encrypted_img_file.write(bmp_header)  # Preserve original header
        encrypted_img_file.write(encrypted_body)  # Append encrypted body

    print(f"Encrypted img created at: {img_path_output}")

def decrypt_with_cbc_mode(ciphertext, secret_key, iv):
    cipher_machine = AES.new(secret_key, AES.MODE_ECB)
    previous_cipher_block = iv
    decrypted_msg = b''
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        print(f"\nDecrypting block {i//16}:")
        
        decrypted_block = cipher_machine.decrypt(block)
        plaintext_block = perform_xor(decrypted_block, previous_cipher_block)
        print(f"After XOR with previous cipher block: {binary_to_printable_hex(plaintext_block)}")
        
        decrypted_msg += plaintext_block
        previous_cipher_block = block  # Update previous cipher block to the current ciphertext block

    return decrypted_msg


def main():

    # Define the path to the img being encrypting
    img_path_input = "../imgs/cp-logo.bmp"
    # Assuming you are running file in src folder
    img_path_output = "../imgs/encrypted/cp-logo-encrypted"

    # Generating the secrets
    secret_key, iv = create_secret_key_and_iv()

    # Encrypting the BMP img
    encrypt_bmp_img(img_path_input, img_path_output, secret_key, iv, 'ECB')
    encrypt_bmp_img(img_path_input, img_path_output, secret_key, iv, 'CBC')

if __name__ == "__main__":
    main()
