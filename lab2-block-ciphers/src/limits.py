import urllib.parse
from helpers import  create_secret_key_and_iv
from modes import encrypt_with_cbc_mode, decrypt_with_cbc_mode

def submit(userdata, key, iv):
    # 1.
    encoded_userdata = urllib.parse.quote(userdata)
    # 2.
    formatted_data = f"userid=456;userdata={encoded_userdata};session-id=31337"
    # 3. 
    formatted_data = formatted_data.encode('utf-8')
    # 4.
    ciphertext = encrypt_with_cbc_mode(formatted_data, key, iv)

    return ciphertext

def verify(ciphertext, key, iv):
    try:
        # 1.
        decrypted_data = decrypt_with_cbc_mode(ciphertext, key, iv)
        print(f"Decrypted data: {decrypted_data}")
        # 2. Directly search for the byte pattern of ';admin=true;'
        return b';admin=true;' in decrypted_data
    except Exception as e:
        print(f"Unexpected error during decryption: {str(e)}")
    return False

def test(key, iv):
    # Test data
    test_input = "0000000000;admin=true;"
    ciphertext = submit(test_input, key, iv)
    is_admin = verify(ciphertext, key, iv)

    print("Ciphertext:", ciphertext)
    print("Is admin:", is_admin)  # Should print False 

def attack(key, iv):
    target_string = "000000000000sadminetrue"

    ciphertext = submit(target_string, key, iv)
    print(f"Original Cipher: {ciphertext}")

    cipher_array = bytearray(ciphertext)
    
# Correct masks based on the XOR differences calculated
    mask1 = 0x73 ^ 0x3b  # 's' to ';'
    mask6 = 0x65 ^ 0x3d  # 'e' to '='

    # Applying the masks to the appropriate positions in the first block of ciphertext
    # which influences the second block's decryption
    cipher_array[16] ^= mask1  # Apply mask at the start of the second block
    cipher_array[16 + 6] ^= mask6  # Apply mask at the sixth position of the second block

    print(f"Modified Cipher Array: {cipher_array}")

    # Verify if the attack was successful
    is_admin = verify(cipher_array, key, iv)
    print("Modified ciphertext is admin:", is_admin)

def main():
    # Generating the secrets
    secret_key, iv = create_secret_key_and_iv()
    print("Generated Secret Key:", secret_key.hex())
    print("-------------------------------------")
    print("TESTING SECURITY!!!")
    test(secret_key, iv)
    print("-------------------------------------")
    print("Attacking!!!")
    attack(secret_key, iv)


if __name__ == "__main__":
    main()
