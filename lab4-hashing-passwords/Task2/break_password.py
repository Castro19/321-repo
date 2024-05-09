import bcrypt
import time
import nltk
from nltk.corpus import words
import concurrent.futures

# Ensure the word corpus is downloaded
nltk.download('words')

# Prepare the word list from nltk corpus
word_list = []
for word in words.words():
    if 6 <= len(word) <= 10:
        word_list.append(word)


# User data
users = {
    "Bilbo":"$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq"
}

def test_password(stored_hash, passwords):
    # Helper function to test each password against the stored hash.
    start_time = time.time()
    for password in passwords:
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return password, time.time() - start_time
    return None, time.time() - start_time

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


if __name__ == "__main__":
    main()

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