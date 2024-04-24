from Crypto.Random import get_random_bytes

# Step 1: Key and IV Generation
def create_secret_key_and_iv():
    # This will generate the secrets we need: a key and an IV
    secret_key = get_random_bytes(16)  # 128 bits are equal to 16 bytes
    iv = get_random_bytes(16)
    return secret_key, iv

# Step 2: PKCS#7 Padding
def apply_pkcs7_padding(msg):
    # Ensure msg is in bytes
    if isinstance(msg, str):
        msg = msg.encode('utf-8')

    # Padding is necessary for msgs not a multiple of block size
    block_length = 16  # AES block size in bytes
    padding_amount = block_length - len(msg) % block_length
    padding = bytes([padding_amount] * padding_amount)
    return msg + padding

def remove_pkcs7_padding(padded_msg):
    padding_amount = padded_msg[-1]  # Get the padding amount from the last byte
    if not 1 <= padding_amount <= 16:  # Check if padding amount is within the valid range
        raise ValueError("Invalid padding amount.")
    # Check if all padding bytes have the correct value
    if padded_msg[-padding_amount:] != bytes([padding_amount] * padding_amount):
        raise ValueError("Invalid padding bytes.")
    return padded_msg[:-padding_amount]


# Step 3: XOR Operation for CBC Mode
def perform_xor(bytes1, bytes2):
    # Useful for CBC mode where we need to XOR the plaintext with the previous ciphertext
    return bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))

# bit_flips = 0x98 ^ 0x3B
# print(bit_flips)

def binary_to_printable_hex(binary_data):
    printable = ""
    for byte in binary_data:
        if 32 <= byte <= 126:  # Printable ASCII range
            printable += chr(byte)
        else:
            printable += "\\x{:02x}".format(byte)
    return printable
