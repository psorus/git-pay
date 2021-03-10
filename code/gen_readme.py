from simulate import *


inv,k=calculate()


#| Attempt | #1 | #2 |
#| :---: | :---: | :---: |
#| Seconds | 301 | 283 |

ret="#git-pay\n\n(Found "+str(inv)+" invalid transactions)\n"


ret+="| User | Worth |"
nl="\n| :---: | :---: |\n"

sam="| #a# | #b#€ |"

for key,val in k.items():

    ret+=nl+sam.replace("#a#",str(key)).replace("#b#",str(val/100))



with open("../README.md","w") as f:
    f.write(ret)

