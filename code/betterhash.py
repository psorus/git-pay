import hashlib as h


def bhash(q):
  return int(h.sha256(str(q).encode('ASCII')).hexdigest(),16)



import sys

if __name__=="__main__":
    ac="test"
    if len(sys.argv)>1:
        ac=sys.argv[1]
    ac=ac+"supersecretkey"
    ha=bhash(ac)
    print(ha)
