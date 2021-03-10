import sys
from user import *



who=input("Who do you want to add?\n")
id=input("Please enter the corresponding id\n")

u=user(who,id)

print(u)

while input("Is this ok?, enter 'y' to save,strg+c to cancel")!="y":pass

u.save()




