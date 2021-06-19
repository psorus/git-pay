from flask import Flask
app=Flask(__name__)
app.config.from_mapping(SECRET_KEY="*** you")

from flask import request,session,redirect# import args


from simulate import *

from transaction import *
from user import *

from gen_mnemonic import gen_mnemonic
from gen_keys import gen_keys
from gen_readme import gen_readme
from erbsunde import erbsunde

from webhelper import *

import json
import os

from aes import encrypt,decrypt
from store import *

def push():
    gen_readme()
    os.system("../send.sh")




@app.route("/")
def central():
    add=""
    if "user" in session.keys():
        add=f"<h1>Hi {session['user']}</h1>" 
    return add+'''<h1>Welcome to this git-pay instance</h1><br>
<p>To make a new entry click here <a href="/easy">here</a> (only do this if you trust the host)</p>
<p>To view the current balances click <a href="/watch">here</a></p>
<p>To register a new user click <a href="/new">here</a></p>
<p>To add a transaction file directly (much safer than using the online guide) click <a href="/upload">here</a></p>
<p>To add a user file directly (much safer than using the online guide) click <a href="/upload_user">here</a></p>
<br>
<p><a href="/login">Login</a></p>
<p><a href="/reg">Register</a></p>


'''

def with_go_back(t):
    return '<p><a href="/">Go Back<a></p>'+t

def form_add_easy():
    val=""
    if "user" in session.keys():
        val=session["user"]
    return generateform("easy",[
        {"name":"fro","desc":"Who are you?","value":val},
        {"name":"too","desc":"Who do you want to pay?"},
        {"name":"value","desc":"How much (whole number ct)?"},        {"name":"mne","desc":"Please add your mnemonic","value":"auto" if len(val)>0 else ""}

        ],"Save")#.replace("POST","GET")

@app.route("/easy",methods=["POST","GET"])
def add_easy():
    args=request.form
    if not ("fro" in args.keys()):return form_add_easy()
    if not ("too" in args.keys()):return form_add_easy()
    if not ("value" in args.keys()):return form_add_easy()
    if not ("mne" in args.keys()):return form_add_easy()

    fro,too,value,mne=[args[zw] for zw in ["fro","too","value","mne"]]
    
    if len(mne)<10 or mne=="auto":
        if "mne" in session.keys():
            mne=session["mne"]


    value=int(value)
    if value<=0:
        return with_go_back("Nice try noob. Setting your Balance to -1 Million Euros. Please pay up as soon as you are able to.<br><br>Measuring your worth....<br><br>Estimation suggests that you wont be able to pay this back....<br><br>Contacting credit institutes.....<br><br>Not enough. Require Payback.....<br>Contacting dark net hitman...<br><br>Positive Confirmation...<br><br>In case of succesful assasination, your death will be billed to your closest Relative...<br><br><br>Good bye. Hope you are happy with our service.")

    try:
        sk,pk,opk=gen_keys(mne)
    except:
        return with_go_back("This is not a valid mnemonic. Please try again or contact your nodes host")
    
    #u=load_user(fro)
    try:
        u=load_user(fro)
    except:
        return with_go_back(f"The user {fro} was not found and can thus not pay anything")

    if not u.key==opk.hex():
        return with_go_back(f"This is not the rigth mnemonic for the user {fro}. Sadly, mnemonics can not be reconstructed, but maybe you just try again.")

    t=transaction(fro,too,value)
    t.signate(sk)
    if not t.verify(pk):
        return with_go_back(f"This transaction did not pass the self test. Contact your nodes host.")

    t.save()



    push()


    return with_go_back(f"Gratulations! This worked and you are now {value} ct poorer")




@app.route("/watch",methods=["POST","GET"])
def watch_balance():
    inv,k=calculate()#this is not the best implementation, since all actions are always calculcated
   

    if inv:
        return with_go_back('Found invalid transaction. Aborting. Please contact the host of this Instance')

    base="<p>#a# has a balance of #b# €</p>"

    ret=''
    for key,val in k.items():
        ret+="\n"+base.replace("#a#",str(key)).replace("#b#",str(val/100))

    return with_go_back(ret)


def form_create_user():
    return generateform("new",[
        {"name":"who","desc":"Who do you want to create?"},

        ],"Register")#.replace("POST","GET")


@app.route("/new",methods=["POST","GET"])
def create_user():
    args=request.form
    if not ("who" in args.keys()):return form_create_user()

    who=args["who"]#[args[zw] for zw in ["who"]]

    who=who.strip()

    try:
        u=load_user(who)
        return with_go_back(f"The user {who} already exists")
    except:pass

    u=user(who)
    mn=gen_mnemonic()

    _,_,key=gen_keys(mn)
    u.key=key.hex()
    u.save()

    return with_go_back(f"Created the user {who}.<br>Your mnemonic is<br><p>{mn}</p><br>About mnemonics: This combination of words is more secure and easier to remember than most passwords and not stored on our servers (if you can trust the host that is). This means that we absolutely cannot recover lost mnemonics and every transaction has to be signed with this mnemonic. So please store it somewhere you can be sure you wont loose it.<br>On the other hand, everybody who has the mnemonic can trade your mnemonic, so also make sure, nobody sees this mnemonic. The best way of storing a mnemonic is: Write it on a piece of paper and stick it into a save. <br><br>For more advanced users: You can use the same mnemonic to do (most) blockchain stuff")


def form_upload():
    return generateform("upload",[
        {"name":"what","desc":"Which transaction (json format) do you want to upload?"},
        ],"upload")#.replace("POST","GET")
    

@app.route("/upload",methods=["POST","GET"])
def upload():
    args=request.form
    if not ("what" in args.keys()):return form_upload()

    q=args["what"]#[args[zw] for zw in ["what"]]

    try:
        t=transaction_from_dict(json.loads(q))
    except:
        return with_go_back("Could not understand this json file as transaction")
    try:
    #for loop in range(1):
        t.save_no_overwride()
    except:
        return with_go_back("This transaction already exists. Doing nothing")
    push()
    return with_go_back("This worked!")


def form_upload_user():
    return generateform("upload_user",[
        {"name":"what","desc":"Which user (json format) do you want to upload?"},
        ],"upload")#.replace("POST","GET")
    

@app.route("/upload_user",methods=["POST","GET"])
def upload_user():
    args=request.form
    if not ("what" in args.keys()):return form_upload_user()

    q=args["what"]#[args[zw] for zw in ["what"]]

    try:
        t=user_from_dict(json.loads(q))
    except:
        return with_go_back("Could not understand this json file as user")
    try:
        t.save_no_overwride()
    except:
        return with_go_back("This user already exists. Doing nothing")
    push()
    return with_go_back("This worked!")


def form_erbsunde_values(fro,too,value,nam):
    print("called form")
    return generateform("erbsunde",[
        {"name":"fro","desc":"Who pays?","value":fro},
        {"name":"too","desc":"Who profits?","value":too},
        {"name":"value","desc":"How much?","value":value},
        {"name":"nam","desc":"Name this repeating transaction","value":nam},
        {"name":"mne","desc":"Please enter your mnemonic!"},
        ],"upload")

def form_erbsunde():
    return form_erbsunde_values("","","","").replace("POST","GET")

@app.route("/erbsunde",methods=["POST","GET"])
def view_erbsunde():
    args=dict(request.form)
    args.update(dict(request.args))
    if not ("fro" in args.keys()):return form_erbsunde()
    if not ("too" in args.keys()):return form_erbsunde()
    if not ("value" in args.keys()):return form_erbsunde()
    if not ("nam" in args.keys()):return form_erbsunde()
    fro,too,value,nam=[args[zw] for zw in ["fro","too","value","nam"]]

    if not ("mne" in args.keys()):return form_erbsunde_values(fro,too,value,nam)

    mne=args["mne"]#[args[zw] for zw in ["what"]]

    value=int(value)
    if value<=0:
        return with_go_back("Nice try noob. Setting your Balance to -1 Million Euros. Please pay up as soon as you are able to.<br><br>Measuring your worth....<br><br>Estimation suggests that you wont be able to pay this back....<br><br>Contacting credit institutes.....<br><br>Not enough. Require Payback.....<br>Contacting dark net hitman...<br><br>Positive Confirmation...<br><br>In case of succesful assasination, your death will be billed to your closest Relative...<br><br><br>Good bye. Hope you are happy with our service.")

    try:
        sk,pk,opk=gen_keys(mne)
    except:
        return with_go_back("This is not a valid mnemonic. Please try again or contact your nodes host")
    
    try:
        u=load_user(fro)
    except:
        return with_go_back(f"The user {fro} was not found and can thus not pay anything (Nobody has no sins)")

    if not u.key==opk.hex():
        return with_go_back(f"This is not the rigth mnemonic for the user {fro}. Sadly, mnemonics can not be reconstructed, but maybe you just try again.")

    try:
        erbsunde(fro,too,value,sk,nam)
    except:
        return with_go_back("This did not work for for some reason. Erbsunden are complicated, but most likely is the given name already taken. Modify it sligtly please. If this does not work, maybe just talk your nodes host")

    push()

    return with_go_back("This erbsunde was created. Enjoy paying for a century")



def form_login():
    return generateform("login",[
        {"name":"user","desc":"Who are you?"},
        {"name":"pass","typ":"password","desc":"Your Password"}

        ],"Login")#.replace("POST","GET")


@app.route("/login",methods=["POST","GET"])
def create_login():
    args=request.form
    if not ("user" in args.keys()):return form_login()
    if not ("pass" in args.keys()):return form_login()

    user=args["user"]#[args[zw] for zw in ["who"]]
    pwd=args["pass"]#[args[zw] for zw in ["who"]]

    user=user.strip()

    mne,val=load_store(user,pwd)
    if not val:
        return "This Password is wrong!"

    session["user"]=user
    session["mne"]=mne


    return redirect("/")




def form_reg():
    return generateform("reg",[
        {"name":"user","desc":"Who are you?"},
        {"name":"pass","typ":"password","desc":"Your Password"},
        {"name":"pass2","typ":"password","desc":"Please repeat this Password"},
        {"name":"mne","desc":"Your Mnemonic"}

        ],"Store")#.replace("POST","GET")


@app.route("/reg",methods=["POST","GET"])
def create_reg():
    args=request.form
    if not ("user" in args.keys()):return form_reg()
    if not ("pass" in args.keys()):return form_reg()
    if not ("pass2" in args.keys()):return form_reg()
    if not ("mne" in args.keys()):return form_reg()

    user=args["user"]#[args[zw] for zw in ["who"]]
    pwd=args["pass"]#[args[zw] for zw in ["who"]]
    pwd2=args["pass2"]#[args[zw] for zw in ["who"]]
    mne=args["mne"]#[args[zw] for zw in ["who"]]

    user=user.strip()

    if not pwd==pwd2:
        return "Those passwords are not equal"

    if has_store(user):
        return f"Already stored {user}"

    save_store(user,mne,pwd)


    session["user"]=user
    session["mne"]=mne


    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")











