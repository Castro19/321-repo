---
title: "April 12, 2024"
bio: "LAEP Advisor Meeting and Mentoring"
priority1: "LAEP Advisor Meeting"
priority2: "Intro to SWE Lecture"
priority3: "Mentoring"
---

# Symmetric Key Cryptography Implementation

## Overview

- In this lab assignment, I utilized the PyCryptodome cryptography package in python to build the following two symmetric key cryptography security modes.

  - Electronic Codebook Mode (ECB)
  - Cipher Block Chaining Mode (CBC)

- I also explored vulnerabilities of block ciphers, notably in the CBC mode through byte flipping.

- Finally I studied the performance between Public vs Symmetric key algorithms.

---

## Task 1: Modes of Operation:

- In this task, I implemented my own versions of ECB and CBC modes of encryption that encrypts the body of an image into a newly encrypted .bmp file.

- **ECB:** Each 128 bit block of plain text is encrypted independently

  1. Initialize a cipher object:

  ```
  cipher_machine = AES.new(secret_key, AES.MODE_ECB)

  ```

  - This object will be used to encrypt blocks of data 128 bits at a time.

    2. **Apply Padding** to the data we are encrypting: Since, AES only allows us to encrypt 128 bits at a time, we must apply padding to ensure that the length of our data is divisible by 128 bits / 16 bytes.

    ```
    def apply_pkcs7_padding(msg):
    # Padding is necessary for msgs not a multiple of block size
    block_length = 16  # AES block size in bytes
    padding_amount = block_length - len(msg) % block_length
    if padding_amount == 0:
        padding_amount = block_length
    padding = bytes([padding_amount] * padding_amount)
    return msg + padding
    ```

    **Usage:**

    ```
    ready_text = apply_pkcs7_padding(plain_text)
    ```

    3. Loop through 128 bits at a time and encrypt the block.

    ```
    encrypted_msg = b''
    for i in range(0, len(ready_text), 16):
        block = ready_text[i:i+16]
        encrypted_msg += cipher_machine.encrypt(block)
    return encrypted_msg
    ```

- **CBC:** Each 128 bit block of plain text will now be encrypted based on the result of its previous encrypted block XOR with its current plain text block. This introduces dependencies between blocks.

  1. **Initialize a cipher object**
  2. **Apply Padding**
  3. **Initialization Vector (IV):** Set the initial previous block to begin at the IV generated with AES.
  4. Loop through 128 bits at a time and encrypt the block based on the result of the XOR.

  ```
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
          # e. Assign our new previous block to the cipher block just created to prepare for the next iterations
          previous_cipher_block = cipher_block
      return encrypted_msg
  ```

  - **Observations:** I used both of these modes to encrypt the following image

    - The following image represents the EBC Mode:

      - Notice how the EBC mode doesn't do a good job at encrypting this data as the the same type of byte (a white pixel) will map to the same encrypted data leading to a pattern the human eye can easily distinguish and notice the pattern instantly.

    - The following image represent CBC Mode:

      - The CBC does a much better job at introducing noise to the image making the visual picture look unrecognizable due to the fact that each cipher block encrypted is entirely dependent on the previous cipher text block allowing for new encryption mapping.

---

## Task 2: Limits of confidentiality

- This task was split up into 3 different parts where I began to test the limits of block ciphers.

- **Part1: Submit Implementation**

  - This function will take as input a string provided by the user and do the following:
    1. URL Encode the user data
    2. Format the string by prepending and appending given substr values.
    3. Apply padding.
    4. Encrypt with the cbc function created in task 1.

  ```
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

  ```

  - The goal for thisd function is to make it impossible for a user to provide a string that will result in `verify()` returning true.

- **Part 2: Verify Implementation**

  - This function should take as input the resulting cipher text of the submit function and do the following:

    1. Decrypt the cipher text string.
    2. Parse the bit string for the substring **';admin=true;'**
    3. Return true or false on whether the string exists.

    ```
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
    ```

- **Part 3: Byte Flip Attack**

  - This was by far the most difficult part in the lab as it took a strong understanding of how you can modify the next ciphertext block by flipping a bit in the current ciphertext block by strategically using xor.
  - **Difficulties:** Since the user text, always encodes chars ";" and "=", it is not feasible to just send the target string as **";admin=true;"**
  - **Solution:** I set my string to be the following target string: `target_string = "000000000000sadminetrue"`

    - This resulted in the following cipher blocks:
      Block 0: userid=456;userd
      Block 1: ata=000000000000
      Block 2: sadminetrue;sess
    - So the goal, was to flip 2 of the bits in block 1 using XOR to result in the following
      1. Flip the "s" in block 2 to ";"
      2. Flip "e" in between "admin" and "true" to "="
    - The result of this would be the correct formatted string, which would cause verify to return true.

  - Code:

  ```
    def attack(key, iv):
        target_string = "000000000000sadminetrue"

        ciphertext = submit(target_string, key, iv)
        print(f"Original Cipher: {ciphertext}")

        cipher_array = bytearray(ciphertext)

        mask1 = 0x73 ^ 0x3b  # 's' to ';' #  Correct masks based on the XOR differences calculated
        mask6 = 0x65 ^ 0x3d  # 'e' to '='

        # Applying the masks to the appropriate positions in the first block of ciphertext
        # which influences the second block's decryption
        cipher_array[16] ^= mask1  # Apply mask at the start of the second block
        cipher_array[16 + 6] ^= mask6  # Apply mask at the sixth position of the second block

        print(f"Modified Cipher Array: {cipher_array}")

        # Verify if the attack was successful
        is_admin = verify(cipher_array, key, iv)
        print("Modified ciphertext is admin:", is_admin)
  ```

## Task 3: Performance comparison

---

## QnA

1. For task 1, looking at the resulting cipher texts, what do you observe? Are you able to derive any useful information about either of the encrypted images? What are the causes for what you observe?

   - **Answer:**

2. For task 2, why this attack possible? What would this scheme need in order to prevent such attacks?

   - **Answer:**

3. For task 3, how do the results compare? Make sure to include the plots in your report.

   - **Answer:**
