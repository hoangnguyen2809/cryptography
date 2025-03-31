# Meet-in-the-Middle Attack
# In Diffie-Hellman cryptography and ElGamal encryption, the discrete logarithm problem is the problem of finding an integer x given g, h, and p where h = g^x mod p. 
# This problem is believed to be computationally difficult. However, if someone is not careful enough and picks 
# which is not too large, then it is possible to perform a so-called Discrete Log Meet-in-the-Middle attack.
# In this example, x is a 40-bit number. We can split x into two 20-bit numbers x0 and x1 such that x = x0 * 2^20 + x1.
# We can then calculate g^x0 mod p for all possible values of x0 and store them in a hash map.
# Next, we can calculate h * (g^-A)^x0 mod p for all possible values of x0 and check if the result is in the hash map.
# If we find a match, we can recover x as x = x0 * 2^20 + x1.

p = 156359275633201089885748260026650426151573557981562388015948993660059100008470225662869866906872016643709374234216966617548140295348776569464946235907635663518308529506117413413505795044214597465795842338687568048427717397062395253524160806628008698098087491030882452609939920197952524777835414437954038474539

g = 8397476121833791627775181592466348716868228211881716057561473758738847453438665416435167319630528724025849218324621565184581446222539874857917943082005696198898670904553536036404957395868399893388550505261375190475690525468545193488975476056387826532082325480387049937308194849710161030362723480809575661

h = 152819244085190339815590951586913796715487655162221556586067984679911205170793183670482162302508037376782869430499690931140384049382929673164822054918466399163938370512096291090332532859280948434893354468770132509669689092575778187275297391759784030014071000704470850655644155167512962115593431272298686208997
# let A = 2^20
A = pow(2, 20)

# calculate g^A mod p
g_A = pow(g, A, p)

# x can be represented as x = Ax0 + x1
# 0 <= x0, x1 <= 2^20
# construct a hash map of all values of g^x1 mod p
g_x1 = {}
for x1 in range(2**20):
    g_x1[pow(g, x1, p)] = x1

# try all possible values of x0
# for each x0, calculate (g^A)^x0 mod p and check if
# we can find h/(g^A)^x0 in the hash map
for x0 in range(2**20):
    val = (h * pow(g_A, -x0, p)) % p
    if val in g_x1:
        x1 = g_x1[val]
        x = x0 * 2**20 + x1
        print(f"x = {x}")
        break

# check if the result is correct
print(pow(g, x, p))
print(h)
