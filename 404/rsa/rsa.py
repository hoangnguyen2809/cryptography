import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sympy import factorint

# Factorizing n
n = 52053189568186346997978125119
factors = factorint(n)
p, q = list(factors.keys())

# Euler's totient function
euler = (p - 1) * (q - 1)

# Private key
d = 25229957129306522909562292399

# Find public key e
e = pow(d, -1, euler)

# Encrypted message
y = 0x5CB5FA00CE9BBA65A5E37CAB
x = pow(y, d, n)

# Hashing and AES key
k = hashlib.sha256("88838556408486262277100".encode()).hexdigest()
aes_key = bytes.fromhex(k)[:32]

# AES parameters
iv = bytes([0] * 16)
ciphertext = 0x265785538BB59DBDAD51F83AA67A2A1B27A9330B8E36F8C0AE6CAA2385B202F5AFEDF9B16CFD6884A3F7E3B93616DFC2

# Convert ciphertext to bytes
ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, byteorder='big')

# Decrypt
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext_bytes), AES.block_size)

# Output
print(f"p = {p}")
print(f"q = {q}")
print(f"n = {n}")
print(f"euler = {euler}")
print(f"d = {d}")
print(f"e = {e}")
print(f"x = {x}")
print(f"Plaintext: {plaintext.decode('utf-8')}")
