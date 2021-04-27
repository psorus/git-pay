

def fieldset(q):
    return "<fieldset>"+q+"</fieldset>"

def generateradio(name,desc,choices,**kw):
    return f'''
  <p>{desc}</p>'''+''.join([f'''
    <input type="radio" id="{key}" name="{name}" value="{key}">
    <label for="{key}"> {val}</label> ''' for key,val in choices.items()])
def generateboxes(name,desc,choices,**kw):
    return f'''
  <p>{desc}</p>'''+''.join([f'''
    <input type="checkbox" id="{key}" name="{name}_{key}" value="{key}">
    <label for="{key}"> {val}</label> ''' for key,val in choices.items()])

def generatenumber(name,desc,value=0,min=0,max=100,**kw):
    return f'''<label for="{name}">{desc}:</label><br>
    <input type="number" id="{name}" name="{name}" value="{value}" min="{min}" max="{max}"><br>'''

def generateinfo(name,desc,**kw):
    return f'''<h3>{desc}</h3>'''
def generatetinfo(name,desc,**kw):
    return f'''<p>{desc}</p>'''

def generateelem(name,desc,value="",typ="text",field=False,**kw):
    if field:
        return fieldset(generateelem(name,desc,value,typ,field=False,**kw))

    if typ=="radio":
        return generateradio(name,desc,**kw)
    if typ=="boxes":
        return generateboxes(name,desc,**kw)
    if typ=="number":
        return generatenumber(name,desc,value=value,**kw)
    if typ=="info":
        return generateinfo(name,desc,**kw)
    if typ=="tinfo":
        return generatetinfo(name,desc,**kw)

    return f'''<label for="{name}">{desc}:</label><br>
    <input type="{typ}" id="{name}" name="{name}" value="{value}"><br>'''

def generateform(callfunc,t,submit="Submit"):
    return f'''<form action="/{callfunc}" method="POST">
{"<br>".join([generateelem(**ac) for ac in t])}
<br><br>
    <input type="submit" value="{submit}">
</form> '''

def generatelink(link,text):
    return f'''<a href="{link}">{text}</a>'''

