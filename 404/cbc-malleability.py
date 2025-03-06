from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import xor

# Define plaintext messages
message1 = b"Pay Ann $25"
message2 = b"Pay me $900"

print(f"Original message\t: {message1.decode()}")
print(f"Message (hex)\t\t: {message1.hex()}")
#message size


print(f"Goal message\t\t: {message2.decode()}")
print(f"Goal message (hex)\t: {message2.hex()}")

print(f"Message size\t\t: {len(message1)}")


# AES key and IV (16 bytes for AES-128)
key = bytes.fromhex("FFEEDDCCBBAA99887766554433221100")
iv = bytes.fromhex("373AEE2B9862A0C683E40E5380E368EC")

# Ensure the message is padded (AES block size is 16 bytes)
padded_message1 = pad(message1, AES.block_size)
padded_message2 = pad(message2, AES.block_size)
#padded message size
print(f"Padded message \t\t: {padded_message1.decode()}")
print(f"Padded message (hex)\t: {padded_message1.hex()}")
print(f"Padded message size\t: {len(padded_message1)}")

# Encrypt using AES-CBC
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ciphertext = cipher.encrypt(padded_message1)

# Print original message and encrypted ciphertext

print(f"Ciphertext (hex)\t: {ciphertext.hex()}")
# Compute the XOR difference needed for modification
msg_xor = xor(padded_message1, padded_message2)
print(f"XOR difference (hex)\t: {msg_xor.hex()}")

# Modify the IV by XORing it with the XOR difference between the two messages
modified_iv = xor(iv, msg_xor)

print(f"Original IV (hex)\t: {iv.hex()}")
print(f"Modified IV (hex)\t: {modified_iv.hex().upper()}")

# Decrypt using the modified IV
cipher = AES.new(key, AES.MODE_CBC, iv=modified_iv)
decrypted = cipher.decrypt(ciphertext)
print(f"Decrypted (hex)\t\t: {decrypted.decode()}")

# Attempt to unpad it
try:
    decrypted = unpad(decrypted, AES.block_size)
    print(f"Decrypted (unpad)\t: {decrypted.decode()}")
except ValueError as e:
    print(f"Error during unpadding: {e}")
