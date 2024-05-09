import matplotlib.pyplot as plt

# Data provided
bit_lengths = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
collision_times = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.03, 0.11, 0.18, 0.71, 0.44, 0.40, 3.54, 8.27, 9.39, 28.72, 55.82, 22.12, 76.76]

# Creating the plot
plt.figure(figsize=(10, 6))
plt.plot(bit_lengths, collision_times, marker='o', linestyle='-', color='red')
plt.title('Digest Size vs. Collision Time')
plt.xlabel('Digest Size (bits)')
plt.ylabel('Collision Time (seconds)')
plt.grid(True)
plt.show()
