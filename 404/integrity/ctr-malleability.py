from Crypto.Cipher import AES
from Crypto.Util import Counter
from pwn import xor

def print_hex_wrapped(text, label, line_length=16):
    # Split the hex string into chunks of 2 characters (representing each byte)
    hex_pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    
    # Join the hex pairs with spaces, and split them into chunks of line_length bytes (2 chars per byte)
    wrapped_hex = [ ''.join(hex_pairs[i:i+line_length]) for i in range(0, len(hex_pairs), line_length)]
    
    # Print the label and each chunk on a new line
    print(f"{label}\t: ")
    print("\n".join(wrapped_hex))


# Read the message from the file and ensure it's in byte format
message = "Transfer $25 from Alex's account into Alice's".encode() # transform the string to bytes
goal_message = "Transfer $500 from Alex's account to mine".encode()

print(f"Original message\t: {message.decode()}")
print_hex_wrapped(message.hex(), "Original message (hex)")
print(f"Goal message\t: {goal_message.decode()}")
print_hex_wrapped(goal_message.hex(), "Goal message (hex)")


# AES key and IV need to be in bytes
key = bytes.fromhex("FFEEDDCCBBAA99887766554433221100")
iv = bytes.fromhex("62745DE0A968B977EC184579C42D9054")

# Counter setup: Using the IV as the starting point for the counter
counter = Counter.new(128)

# Create AES cipher in CTR mode
cipher = AES.new(key, AES.MODE_CTR, counter=counter)

# Encrypt the message
ciphertext = bytes.fromhex("3915FEBFB3EF4D62DFE2714703E85E4B4803584659F9DD81AB7A407BF47477AA2D932D87DE74E6EF7CF5AAE1A8")

# Print the encrypted ciphertext
print_hex_wrapped(ciphertext.hex(), "Ciphertext1 (hex)")

# xor two messages
xor_message = xor(message, goal_message)
print_hex_wrapped(xor_message.hex(), "XOR message (hex)")
# xor the xor message with the ciphertext
modified_ciphertext = xor(ciphertext, xor_message)
required_length = len(goal_message)
trimmed_modified_ciphertext = modified_ciphertext[:required_length]

print_hex_wrapped(trimmed_modified_ciphertext.hex(), "Modified ciphertext (hex)")

# Decrypt the modified ciphertext
cipher = AES.new(key, AES.MODE_CTR, counter=counter)
decrypted = cipher.decrypt(trimmed_modified_ciphertext)
print(f"Decrypted message\t: {decrypted.decode()}")
