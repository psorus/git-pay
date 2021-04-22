import sys
from transaction import *

from user import *

from gen_keys import gen_keys

fro=input("Who pays?\n")
too=input("Who gets payed?\n")
value=int(input("How much do you pay\n"))

if value<=0:
    print("nice try, noob")
    exit()

mnemo=input(f"To verify this transaction, please add the mnemonic of {fro}\n")

sk,pk,opk=gen_keys(mnemo)

u=load_user(fro)
if not u.key==opk.hex():
    print("This is not the rigth mnemonic. Canceling...")
    exit()

t=transaction(fro,too,value)
t.signate(sk)

test=t.verify(pk)
if test:
    print("Passed the self test")
else:
    print("Failed the self test")
    exit()

while input("Is this ok?, enter 'y' to save,strg+c to cancel")!="y":pass

t.save()




