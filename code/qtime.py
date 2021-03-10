from datetime import datetime,timedelta
import math


reference_time=datetime(1940,1,1)
timeformat="%d.%m.%Y %H:%M:%S.%f"
class qtime(object):

    def __init__(s,q=None):
        if q is None:q=0
        if type(q) is datetime:q=(q-reference_time).total_seconds()
        s.q=float(q)

    def totime(s,reference_time=reference_time):
        return reference_time+timedelta(seconds=s.q)
    
    def __str__(s):
        return s.totime().strftime(timeformat)

    def __repr__(s):
        return str(s)

    def __float__(s):
        return s.q

    def __add__(a,b):
        return qtime(float(a)+float(b))

    def __mul__(a,b):
        return qtime(float(a)*float(b))
    __rmul__=__mul__

    def __le__(a,b):
        return float(a)<float(b)
    def __gt__(a,b):
        return float(a)>float(b)



#oneyear=qtime(reference_time+timedelta(years=1))#not every year is the same
oneweek=qtime(reference_time+timedelta(days=7))
oneday=qtime(reference_time+timedelta(days=1))
#oneleap=oneyear+oneday
onehour=qtime(reference_time+timedelta(hours=1))
onemin=qtime(reference_time+timedelta(minutes=1))
onesec=qtime(reference_time+timedelta(seconds=1))



class everyn(object):
    """represents a repeatable timeframe. rep is also a timeframe"""
    def __init__(s,rep,tim,shift=0):
        s.rep=rep
        s.tim=tim
        s.shift=shift

    def last_before(s,t0):
        whole=int(math.ceil((float(t0)-float(s.shift))/float(s.rep)))
        whole*=float(s.rep)
        whole+=float(s.shift)
        ret=whole+float(s.tim)
        while ret>float(t0):
            ret-=float(s.rep)
        #while ret<float(t0):
        #    ret+=float(s.rep)
        #ret-=float(s.rep)
        return qtime(ret)
    def next_after(s,t0):
        whole=int(math.floor((float(t0)-float(s.shift))/float(s.rep)))
        whole*=float(s.rep)
        whole+=float(s.shift)
        ret=whole+float(s.tim)
        while ret<float(t0):
            ret+=float(s.rep)
        #while ret>float(t0):
        #    ret-=float(s.rep)
        #ret+=float(s.rep)
        return qtime(ret)

class everydelta(object):
    """like everyn, but incompassing a whole range"""
    def __init__(s,rep,tim1,tim2,shift=0):
        #s.a=everyn(rep,tim1,shift=shift)
        s.b=everyn(rep,tim2,shift=shift)
        s.len=float(tim2)-float(tim1)

    def bynextend(s,t0):
        nextend=s.b.next_after(t0)
        lastone=float(nextend)-s.len
        return qtime(lastone),nextend

    def inrange(s,t0):
        mint,maxt=s.bynextend(t0)
        return mint<=t0 # and maxt>=t0#this should be trivially fullfilled


def now():
    return qtime(datetime.now())
def read_time(q):
    return qtime(datetime.strptime(q,timeformat))



class multitimer:
    """multiple ranges, each have to be fullfilled for a date to be valid"""
    def __init__(s,*q):
        s.q=[]
        for zw in q:
            s.add(zw)
    def add(s,q):
        if type(q) is list:
            for zw in q:
                s.add(zw)
            return
        s.q.append(q)

    def valid(s,t0):
        for zw in s.q:
            if not zw.inrange(t0):return False
        return True

    def validshift(s,t0,dt,motio=1.0):#ignores milliseconds, can thus be around 1sec wrong. Also not that smart of an algorithm
        motio=float(motio)
        t=float(t0)
        delt=float(dt)
        while delt>0:
            t+=motio
            if s.valid(t):delt-=motio
        return qtime(t)


if __name__=="__main__":
    everyweek=everyn(2*oneweek,0,shift=oneweek)
    inntheweek=everydelta(oneweek,0*oneday,oneday*5)
    tradingtime=everydelta(oneday,9*onehour,17.5*onehour)
    timer=multitimer(inntheweek,tradingtime)
    print(timer.valid(now()))

    print(timer.validshift(now(),50*oneweek,onehour))
    print(timer.validshift(now(),50*oneweek,onemin))


