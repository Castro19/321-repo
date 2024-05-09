# Lab Assignment: Cryptographic Hash Functions

## Objectives

- To explore Pseudo-randomness and Collision Resistance.

- To break real hashes (To crack a password file)

- **Technologies used**: Python, PyCryptodome, Bcrypt

## Task 1: Explore Pseudo-Randomness and Collision Resistance

- Investigate the pseudorandom and collision resistant properties
  of cryptographic hash functions

### Part A: Use SHA256 to hash arbitrary inputs

```
def hash_input(input_string):
    # 1. Create a SHA256 hash
    hasher = hashlib.sha256()

    # 2. Update hash object w/ the bytes of the input string encoded
    hasher.update(input_string.encode('utf-8'))

    # 3. Get the hexdigest of the hash
    hex_digest = hasher.hexdigest()

    # Print the hex digest
    print(f"Input: {input_string}\nSHA256 Digest: {hex_digest}")
    return hex_digest
```

### Part B: Hash Two strings that differ in only 1 bit

```
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
```

### Part C: Find a collision

#### Limit the 256-bit output to a domain between 8-50 inputs:

```
def truncate_digest(hex_digest, bit_length):
    # Convert hex digest to an int
    full_digest = int(hex_digest, 16)
    # Truncate to bit length
    truncated_digest = full_digest >> (256 - bit_length)
    return truncated_digest
```

#### Leveraging the Birthday Problem to find a collision

```

def find_collision(bit_length):
    hash_table = {} # Birthday Hash
    attempts = 0

    while True:
        random_string = generate_random_string()
        digest = hash_input(random_string)
        truncated_digest = truncate_digest(digest, bit_length)

        if truncated_digest in hash_table:
            print(f"Collision found after {attempts} attempts!")
            print(f"String 1: {hash_table[truncated_digest]} => Digest: {truncated_digest}")
            print(f"String 2: {random_string} => Digest: {truncated_digest}")
            break
        else:
            hash_table[truncated_digest] = random_string
            attempts += 1
```

- Here is a graph that measure the number of attempts and total time for a collision to be found for multiple of 2 in the range of 2 bits to 50 bits.

![](https://live.staticflickr.com/65535/53693934163_96d1a853a7.jpg)

![](https://live.staticflickr.com/65535/53693728646_4fe812b3fa.jpg)

- Notice how the time it takes, for the most part this grows exponentially, however there can be some instances where we get lucky and find a collision fast. For example, in the drop when the bits were 48.

## Task 2: Breaking Real Hashes

- In this task, I created a custom script to crack user's password usign the `nltk` word corupus for wors between 6 & 10 letters.

- Initially I created an algorithm to crack the password using a simplified approach. However, due to bcrypt running very slow, I wanted to leveraged Python's ability to use multiprocessing.

  - In the code belowe, I am running the hashing in parallel 7 individual cores.

1. Download the word corpus from `nltk` & get the words between 6 and 10 characters

   ```
    nltk.download('words')
    word_list = []
    for word in words.words():
        if 6 <= len(word) <= 10:
            word_list.append(word)
   ```

2. Create a Helper Function to test each password against the stored hash.

   ```
   def test_password(stored_hash, passwords):
       # Helper function to
       start_time = time.time()
       for password in passwords:
           if bcrypt.checkpw(password.encode(), stored_hash.encode()):
               return password, time.time() - start_time
       return None, time.time() - start_time
   ```

3. Create a helper function to split the list into `n` sublists

   ```
   def split_list(lst, n):
    # Split the list into n chunks.
    def split_list(lst, n):
        base_length, extra = divmod(len(lst), n)

        # Loop through each part index to create the sublists
        for i in range(n):
            # Start index of the sublist
            start = i * base_length + min(i, extra)
            # End index of the sublist; not inclusive
            end = (i + 1) * base_length + min(i + 1, extra)
            # Yield the sublist from start to end
            yield lst[start:end]

   ```

4. Create the multiprocessing approach:

   ```
   def main():
        num_processes = 6  # Number of processes to use
        chunks = list(split_list(word_list, num_processes))

        # Create a process pool with the specified number of workers
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
            for user, stored_hash in users.items():
                # Initialize an empty list to hold future objects
                futures = []
                # Submit tasks to the executor and store the future objects
                for chunk in chunks:
                    future = executor.submit(test_password, stored_hash, chunk)
                    futures.append(future)

                # Wait for the futures to complete and process results as they become available
                for future in concurrent.futures.as_completed(futures):
                    result, duration = future.result()
                    if result:
                        print(f"{user}'s password is: {result}.\nFound in {duration:.2f} seconds")
                        break  # Stop other processes if one finds the password
                else:
                    print(f"Failed to find {user}'s password.")
   ```

### Passwords:

```
# Password for Bilbo is: welcome, found in 296.44 seconds
# Password for Gandalf is: wizard, found in 318.50 seconds
# Password for Thorin is: diamond, found in 192.23 seconds
# Password for Fili is: desire, found in 365.86 seconds
# Password for Kili is: ossify, found in 584.86 seconds
# Password for Balin is: hangout, found in 687.27 seconds
# Password for Dwalin is: drossy, found in 922.11 seconds
# Password for Oin is: ispaghul, found in 1151.24 seconds
# Password for Gloin is: oversave, found in 168.42 seconds
# Password for Dori is: indoxylic, found in 2625.90 seconds
# Password for Nori is: swagsman, found in 1284.38 seconds
# Password for Ori is: airway, found in 658.55 seconds
# Password for Bifur is: corrosible, found in 6345.86 seconds
# Password for Bofur is: libellate, found in 6899.47 seconds
# Password for Durin is: purrone, found in 11213.16 seconds
```

## Questions & Answers

**I will finish up the questions this week and submit the final version**

1.  What do you observe based on Task 1b? How many bytes are different between the two digests?

- In this task, I flipped the LSB of the first byte in the input string. However, the resulting hashing were very different. When I calculated the bytes between the two digest for the input string of `CSC321`, I got 128 bits.

2.  What is the maximum number of files you would ever need to hash to find a collision on an n-bit digest? Given the birthday bound, what is the expected number of hashes before a collision on an n-bit digest? Is this what you observed? Based on the data you have collected, speculate on how long it might take to find a collision on the full 256-bit digest.

- The max number of files to hash to find a collision on an n-bit digest would be `2^n`. Given the birthday bound, the expeced number of hashes before a collision would be `sqrt(2 * n * ln(2))`. This would take a lot less hashes on average resulting in less time spent searching for a collision which is what I observed. Finding a collision on the full 256-bit digest would take about 2^128 attempts which seems impossible and the amount of time it would take to find a collision, on average, would be hundreds of years.

3.  Given an 8-bit digest, would you be able to break the one-way property (i.e. can you find any pre-image)? Do you think this would be easier or harder than finding a collision? Why or why not?

- Finding a pre-image would be possible through a brute-force search. It would be O(2^2) where n in this case would be 8 (the number of bits in the digest). However, finding a collision would be faster and easier because it only needs a single pair to match and does not care which specific values create the collision allowing for more combinations of a collision occurring.

4.  For Task 2, given your results, how long would it take to brute force a password that uses the format word1:word2 where both words are between 6 and 10 characters? What about word1:word2:word3? What about word1:word2:number where number is between 1 and 5 digits? Make sure to sufficiently justify your answers.

- Given my results, and assuming the following:
  - I ran 5 process in parallel
  - bcrypt's cost factor took about 0.5 second
  - NLTK word corpus dictionary contains 135,00 words

these would be my results:

- **word1:word2**: (135000^2 \* 0.5 seconds) / 5 = 1,822,500,000 seconds of ~21 years

- **word1:word2:word3**: (135000^3 \* 0.5 seconds) / 5 = 1,230,187,500,000,000 seconds of ~7.8 million years

- **word1:word2:number**: (135000^2 \* 99999 \* 0.5 seconds) / 5 = 911,181,432,500,000 seconds seconds of ~5.7 million years
