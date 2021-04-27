from simulate import *


def gen_readme():

    inv,k=calculate()


    #| Attempt | #1 | #2 |
    #| :---: | :---: | :---: |
    #| Seconds | 301 | 283 |

    ret="#git-pay\n\n(Found "+str(inv)+" invalid transactions)\n"


    ret+="| User | Worth |"
    nl="\n| :---: | :---: |\n"

    sam="| #a# | #b#€ |"

    ret+=nl

    for key,val in k.items():

        ret+=sam.replace("#a#",str(key)).replace("#b#",str(val/100))+"\n"



    with open("../README.md","w") as f:
        f.write(ret)
    
    return inv,k



if __name__=="__main__":gen_readme()



