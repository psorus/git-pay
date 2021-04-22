from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from time import time

import random

random.seed(12)

t0=time()



private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

pubyte=public_key.public_numbers()

print(pubyte)

exit()




t1=time()


print(private_key)
print(public_key)


print(t1-t0)
