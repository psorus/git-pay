import sys
from user import *

from gen_mnemonic import gen_mnemonic
from gen_keys import gen_keys


who=input("Who do you want to add?\n")
#id=input("Please enter the corresponding id\n")

u=user(who)

print(u)

while input("Is this ok?, enter 'y' to continue generating keys,strg+c to cancel")!="y":pass

mn=gen_mnemonic()
print("I generated your mnemonic. Remember it, it is not recoverable and you need it to sign all your transactions!")
print("The mnemonic is:")
print("")
print(mn)
print("")

_,_,key=gen_keys(mn)

u.key=key.hex()


u.save()




