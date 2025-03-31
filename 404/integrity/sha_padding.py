def sha256_padding(message):
    # Step 1: Convert the message to binary (for both string and binary input)
    if isinstance(message, str):  # If the message is a string
        binary_message = ''.join(format(ord(c), '08b') for c in message)
    elif isinstance(message, bytes):  # If the message is already in bytes (like from a binary file)
        binary_message = ''.join(format(byte, '08b') for byte in message)
    else:
        raise ValueError("Message must be a string or bytes.")
    
    # Step 2: Append a '1' bit
    binary_message += '1'
    
    # Step 3: Append '0' bits until the message length is congruent to 448 mod 512
    message_len = len(binary_message)
    zero_bits_to_add = (448 - (message_len % 512)) % 512
    binary_message += '0' * zero_bits_to_add
    
    # Step 4: Append the original length of the message (in bits) as a 64-bit integer
    original_length = len(message) * 8  # Length in bits
    binary_message += format(original_length, '064b')
    
    # Return the padded binary message
    return binary_message

# Example usage with a binary file
input_file = "71f3aab8e4a4.binary"
message = open(input_file, 'rb').read()  # Read the binary data from the file

# Compute the padded message
padded_message = sha256_padding(message)

# Print the padding part in hexadecimal
padding_part = padded_message[len(''.join(format(byte, '08b') for byte in message)):]
print(hex(int(padding_part, 2)))
