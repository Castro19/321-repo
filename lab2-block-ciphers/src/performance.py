import matplotlib.pyplot as plt

def AES():
    # Define block sizes and throughput for AES-128-CBC
    block_sizes = [16, 64, 256, 1024, 8192, 16384]  # in bytes
    throughput_128 = [1111957.77, 1423389.47, 1556807.83, 1585678.68, 1601557.92, 1599728.21]  # in kB/s
    throughput_192 = [1024996.04, 1225372.05, 1292279.30, 1303823.93, 1314426.95, 1314299.19]
    throughput_256 = [858591.57, 1060272.36, 1110592.85, 1127918.59, 1136530.04, 1139174.06]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(block_sizes, throughput_128, label='AES-128-CBC', marker='x')
    plt.plot(block_sizes, throughput_192, label='AES-192-CBC', marker='x')
    plt.plot(block_sizes, throughput_256, label='AES-256-CBC', marker='x')

    plt.title('AES Throughput vs. Block Size')
    plt.xlabel('Block Size (bytes)')
    plt.ylabel('Throughput (kB/s)')
    plt.legend()
    plt.grid(True)
    plt.show()

def RSA():
    # Key sizes and their corresponding performances
    key_sizes = ['2048 bits', '4096 bits']
    sign_perfs = [1824.0, 286.2]  # signs per second
    verify_perfs = [72257.8, 19769.9]  # verifies per second

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Sign performance
    ax.bar([x for x in range(len(key_sizes))], sign_perfs, color='r', width=0.4, label='Sign/s')

    # Verify performance
    ax.bar([x + 0.4 for x in range(len(key_sizes))], verify_perfs, color='g', width=0.4, label='Verify/s')

    ax.set_xlabel('RSA Key Size')
    ax.set_ylabel('Operations per Second')
    ax.set_title('RSA Performance: Operations per Second by Key Size')
    ax.set_xticks([x + 0.2 for x in range(len(key_sizes))])
    ax.set_xticklabels(key_sizes)
    ax.legend()

    plt.grid(True)
    plt.show()

def main():
    AES()
    RSA()


if __name__ == "__main__":
    main()

