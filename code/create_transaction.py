import sys
from transaction import *



fro=input("Who pays?\n")
too=input("Who gets payed?\n")
value=input("How much do you pay\n")

t=transaction(fro,too,value)

print(t)

while input("Is this ok?, enter 'y' to save,strg+c to cancel")!="y":pass

t.save()




