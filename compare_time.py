def timeTrans(a):
    if '201' not in a:
        lista = list(a)
        lista.insert(0, '2017-')
        lista.insert(17, ':00')
        a = "".join(lista)
        a = a.replace('月', '-')
        a = a.replace('日', '')
    return a

""":return true means a later than b,like a=2017,b=2016,return true"""
def timeCompare(a, b):
    a = timeTrans(a)
    b = timeTrans(b)
    a_struct = time.strptime(a, '%Y-%m-%d %H:%M:%S')
    b_struct = time.strptime(b, '%Y-%m-%d %H:%M:%S')
    return a_struct > b_struct
