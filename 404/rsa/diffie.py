import sympy
import random
from Crypto.Cipher import AES
import binascii
from hashlib import sha256

def generate_384_bit_prime():
    """Generate a random 384-bit prime number."""
    bit_length = 384
    while True:
        rand_num = random.getrandbits(bit_length)
        rand_num |= 1  # Ensure the number is odd
        if sympy.isprime(rand_num):
            return rand_num

# Parameters
p = 0x0094d949516c329b83504812dceac39a38bcb125c8e91b39a19d4027ef36b20217483f7a0c7e4d8f420cd7068f556ff46b
g = 0x02

# Generate Alice's private key
#a = generate_384_bit_prime()
a = 0xb596cb9052e1656664047ee8adf644d5d428272cbaae430177abb2682ce7451182d5a768a9b884c2d88a8a3164d4b22b
print(f"Alice's private key (a): {hex(a)}")

# Calculate A = g^a mod p
A = pow(g, a, p)
print(f"A: {hex(A)}")

# Ciphertext and g^b mod p from the other party
ciphertext = 0xda3890e0d02b2886b5f1095d453674609a195ad8eb7dec7727f333744bcceeb2e70a7e9c9ed68f7f11818015e1b297cfb3ad394e19a9d29a3e80fab2f0cd288751a7b8ea17ce73ac95728104b3a08232
g_b = 0x021a3a127eabd337faab30d83bda874114a588c3b08957c4aebee272a7449572f73c5162e46ecd0bcf5483ee4f24054c

# Calculate the shared secret
shared_secret = pow(g_b, a, p)
print(f"Shared secret: {hex(shared_secret)}")

# Convert the shared secret to bytes
shared_secret_bytes = shared_secret.to_bytes(48, byteorder='big')

# Derive IV and key
iv = shared_secret_bytes[:16]  # First 128 bits
key = shared_secret_bytes[16:]  # Last 256 bits

print(f"IV: {binascii.hexlify(iv)}")
print(f"Key: {binascii.hexlify(key)}")

# Convert ciphertext to bytes and pad it to 16 bytes
ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, byteorder='big')

# Add padding if needed
padding_length = 16 - (len(ciphertext_bytes) % 16)
if padding_length != 16:
    ciphertext_bytes += b'\x00' * padding_length  # Padding with null bytes

# Decrypt the ciphertext using AES-CBC-256
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext_bytes)

# Remove potential padding (PKCS7)
try:
    pad_len = plaintext[-1]
    if 1 <= pad_len <= 16:
        plaintext = plaintext[:-pad_len]
except IndexError:
    pass

print(f"Decrypted plaintext: {plaintext.decode('utf-8', errors='ignore')}")
