import binascii
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from sympy import integer_nthroot

# ciphertext = message^e (mod n)
ciphertext = 0xecdccfdf5abe7b0a028bb2a3d2a000f033973863410294d65e94c104218001dec3c3d8d8bfd7a70b723eb9617fcb5f15
# key_encrypted is RSA encryption of m0 = IV||key
key_encrypted = 0x2060a74412965a430ad1e2f708b42797954dfa1c2365af58d09b087b00ae7605aa955d08e29ac191e98a9ccca349191f3816872c59104ba41f8b8f7e5ca6fb2b181721a32e478417794831fb85b4c1e5cbcf272bb1737111b9f7d3d6a10f53d

# open file public-key.pem then read in the modulus and exponent
f = open('public-key.pem', 'r')
key = RSA.importKey(f.read())
f.close()

# print out the modulus in hex and exponent
print(f"Modulus: {key.n:x}")
print(f"Exponent: {key.e}")

# Low Public Exponent Attack: compute e-th root of key_encrypted (without mod n)
# Since e=3, we can try to compute the cube root
m0_cubed, is_exact = integer_nthroot(key_encrypted, key.e)
if not is_exact:
    # If not exact, try adding multiples of n until we find a perfect root
    found = False
    for k in range(1, 1000):
        m0_cubed, is_exact = integer_nthroot(key_encrypted + k * key.n, key.e)
        if is_exact:
            found = True
            break
    if not found:
        raise ValueError("Could not find exact e-th root")

# Verify the solution
if pow(m0_cubed, key.e, key.n) == key_encrypted:
    print("Found valid m0!")
else:
    raise ValueError("Computed m0 doesn't satisfy m0^e ≡ c (mod n)")

# Convert m0 to hex
m0_hex = hex(m0_cubed)[2:]  # Remove '0x' prefix
print(f"m0: {m0_hex}")

# Pad with leading zeros if necessary to get full length
# The expected length is 256 bits (64 hex chars) for IV (128 bits) + key (128 bits)
if len(m0_hex) < 64:
    m0_hex = m0_hex.zfill(64)

# extract the IV = m0[0...31] and key = m0[32...63]
# where each is 128 bits (32 hex characters)
IV_hex = m0_hex[:32]
key_hex = m0_hex[32:64]

print(f"IV: {IV_hex}")
print(f"key: {key_hex}")
print(f"Key length: {len(key_hex)}")

# Convert the IV and key from hex to bytes
IV = binascii.unhexlify(IV_hex)
key_bytes = binascii.unhexlify(key_hex)

# Convert ciphertext to bytes (it's 256 bytes long)
ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, 'big')

# Decrypt the ciphertext using AES-CBC-128 with the extracted IV and key
cipher = AES.new(key_bytes, AES.MODE_CBC, IV)

# Decrypt the ciphertext
plaintext = cipher.decrypt(ciphertext_bytes)
print("Plaintext:", plaintext)