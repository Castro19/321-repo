import hashlib

def sha256_hash(input_string):
    # Create a SHA256 hash object
    hasher = hashlib.sha256()
    # Encode the input string to bytes and update the hash object
    hasher.update(input_string.encode('utf-8'))
    # Return the digest as a byte array
    return hasher.digest()

def modify_bit(input_string):
    # Modify one bit of the input string
    byte_array = bytearray(input_string, 'utf-8')
    # Flip the LSB of the byte at position 0
    byte_array[0] ^= 0x01
    # Return the modified string
    return byte_array.decode('utf-8', errors='ignore')

def compute_hamming_distance(bytes1, bytes2):
    # Calculate the Hamming distance between two byte arrays
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(bytes1, bytes2))

# Example usage
original_string = "CSC321"
modified_string = modify_bit(original_string)

# Hash both the original and the modified string
original_hash = sha256_hash(original_string)
modified_hash = sha256_hash(modified_string)

# Compute the Hamming distance between the hashes
hamming_distance = compute_hamming_distance(original_hash, modified_hash)

print(f"Hamming Distance: {hamming_distance} bits")
