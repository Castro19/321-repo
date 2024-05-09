import hashlib
import random
import string
import time
import matplotlib.pyplot as plt

def hash_input(input_string):
    # 1. Create a SHA256 hash
    hasher = hashlib.sha256()
    
    # 2. Update hash object w/ the bytes of the input string encoded
    hasher.update(input_string.encode('utf-8'))
    
    # 3. Get the hexdigest of the hash
    hex_digest = hasher.hexdigest()
    
    # Print the hex digest
    return hex_digest

def modify_bit(input_string):
    # Modify one bit of the input string.
    byte_array = bytearray(input_string, 'utf-8')
    
    # Choose a byte position to modify
    byte_pos = 0  

    # Flip the LSB of the byte at byte_pos
    byte_array[byte_pos] ^= 0x01

    # Create the modified byte array
    modifed_btye_array = byte_array.decode('utf-8')
    
    return modifed_btye_array

def truncate_digest(hex_digest, bit_length):
    # Convert hex digest to an int 
    full_digest = int(hex_digest, 16)
    # Truncate to bit length
    truncated_digest = full_digest >> (256 - bit_length)
    return truncated_digest

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def find_collision(bit_length):
    hash_table = {}
    attempts = 0
    start_time = time.time()
    
    while True:
        random_string = generate_random_string()
        hex_digest = hash_input(random_string)
        truncated_digest = truncate_digest(hex_digest, bit_length)
        
        if truncated_digest in hash_table:
            end_time = time.time()
            time_taken = end_time - start_time
            return attempts, time_taken
        else:
            hash_table[truncated_digest] = random_string
            attempts += 1

#
if __name__ == "__main__":
    bit_lengths = range(8, 51, 2)  # From 8 to 50 bits, inclusive
    collision_attempts = []
    collision_times = []

    for bits in bit_lengths:
        attempts, time_taken = find_collision(bits)
        collision_attempts.append(attempts)
        collision_times.append(time_taken)
        print(f"Bits: {bits}, Attempts: {attempts}, Time: {time_taken:.2f} seconds")

    # Plotting Digest Size vs. Number of Inputs
    plt.figure(figsize=(10, 5))
    plt.plot(bit_lengths, collision_attempts, marker='o')
    plt.title('Digest Size vs. Number of Inputs to Find a Collision')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Time spent')
    plt.grid(True)
    plt.show()