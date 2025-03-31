import sympy
import random

def generate_384_bit_prime():
    # Generate a random 384-bit number
    bit_length = 384
    while True:
        rand_num = random.getrandbits(bit_length)
        # Ensure the number is odd to increase the likelihood of it being prime
        rand_num |= 1
        if sympy.isprime(rand_num):
            return rand_num

# Generate a random 384-bit long number

p = 0x00c82abd603ac5cb120ae480763a8cc36bc10d715e5053126e25a876a1bef78a15b6e856079e566315fc3da8bec328bbf3

g = 0x02

#create a random 384 bits prime number which is alice's private key
a = generate_384_bit_prime()

print(a)

# calculate A = g^a mod p
A = pow(g, a, p)
