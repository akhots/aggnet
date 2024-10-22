#!/usr/bin/env python3
# Aggregation of networks. Written on Python 3.6
print('AggNet 2.0.0c  Developed by Alex Khots\n')

def fNetConv(a):
    if a.count('/') == 0:
        b = a.split()
        if len(b) == 1:
            a = a + '/32'
        elif b.count('host') == 1:
            a = b[1] + '/32'
        elif len(b) == 2:
            a = b[0]
            b = b[1].split(sep='.')
            for one in range(len(b)):
                b[one] = bin(int(b[one])).replace('0b','').zfill(8)
            b = b[0] + b[1] + b[2] + b[3]
            c = 0
            for one in range(len(b) - 1):
                if b[one] != b[one+1]:
                    c += 1
            if c != 1:
                a = 'Bad mask'
            elif b[0] == str(1):
                a = a + '/' + str(b.count('1'))
            else:
                a = a + '/' + str(b.count('0'))
    a = a.split(sep='/')
    a[0] = a[0].split(sep='.')
    try:
        if len(a[0]) != 4:
            a = 'Bad network length'
        elif int(a[0][0]) >= 256 or int(a[0][1]) >= 256 or int(a[0][2]) >= 256 or int(a[0][3]) >= 256:
            a = 'Bad octet value'
        elif int(a[1]) > 32 or len(a) != 2:
            a = 'Bad mask'
        else:
            a[1] = 2**(32 - int(a[1]))
            a[0] = int(a[0][0])*256**3 + int(a[0][1])*256**2 + int(a[0][2])*256 +  int(a[0][3])
        if a[0] % a[1] != 0:
            a = 'Bad network'
    except:
        a = 'Bad value'
    return a


def fNetClearList(a):
    while a.count([0, 0]) > 0:
        a.remove([0, 0])


def fNetReduceList(a):
    for one in range(len(a)-1):
        if a[one][0] + a[one][1] >= a[one+1][0] + a[one+1][1]:
            a[one+1] = [0,0]


def fNetAggList(a):
    for one in range(len(a)-1):
        if a[one][0] + a[one][1] == a[one+1][0]:
            if a[one][1] == a[one+1][1]:
                if a[one][0] / a[one][1] % 2 == 0:
                    a[one][1] *= 2
                    a[one+1] = [0,0]


def fNetConvB(a):
    b = list(a)
    c = b[0] // 256**3
    b[0] = b[0] % 256**3
    d = b[0] // 256**2
    b[0] = b[0] % 256**2
    e = b[0] // 256
    b[0] = b[0] % 256
    f = b[0]
    g = 32
    while b[1] != 1:
        b[1] = b[1] / 2
        g -= 1
    return str(c) + '.' + str(d) + '.' + str(e) + '.' + str(f) + '/' + str(g)


def fNetMask(a,w):
    b = int(a.split(sep='/')[1])
    if b == 32:
        return 'host ' + a.split(sep='/')[0]
    c = []
    while b > 8:
        b = b - 8
        c.append(255)
    c.append(256-2**(8-b))
    while len(c) < 4:
        c.append(0)
    if int(w) == 1:
        for one in range(len(c)):
            c[one] = 255 - c[one]
    c = str(c[0]) + '.' + str(c[1]) + '.' + str(c[2]) + '.' + str(c[3])
    return a.split(sep='/')[0] + ' ' + c


netListC = []

while True:
    net = input('Enter network or IP address: ')
    netC = fNetConv(net)
    if type(netC) == list:
        netListC.append(netC)
    elif net == '':
        break
    else:
        print(netC)
#-------------------------------- input --------------------------------

inLen = len(netListC)

netListC.sort()

for one in range(len(netListC)-1):
    if netListC[one][0] == netListC[one+1][0]:
        netListC[one] = [0,0]

fNetClearList(netListC)

fNetReduceList(netListC)
while netListC.count([0, 0]) > 0:
    fNetClearList(netListC)
    fNetReduceList(netListC)


netList = []
netListMask = []
netListMaskW = []

outLen = len(netListC)

for one in netListC:
    netList.append(fNetConvB(one))

for one in netList:
    netListMask.append(fNetMask(one,0))

for one in netList:
    netListMaskW.append(fNetMask(one,1))



print('\nNetwork                 For ACL with mask                   For ACL with wildcard mask\n')
for one in range(outLen):
    print(netList[one].ljust(24) + netListMask[one].ljust(36) + netListMaskW[one])


if outLen == inLen:
    print('\nThere are no networks to aggregate. Sorry...')
    if inLen > 1:
        print('But at least they were sorted ;)')
else:
    print('\nCongratulations! The networks have been aggregated!')
    print('Amount was reduced from ' + str(inLen) + ' to ' + str(outLen))


print('''
For presenting in ACL form enter 1 (with mask) or 2 (with wildcard mask)
For exit enter "exit"''')

while True:
    theEnd = input('\nEnter: ').lower()
    if theEnd == 'exit':
        quit()
    elif theEnd == '1':
        print('For ACL with mask:\n')
        for one in netList:
            print(fNetMask(one,0))
    elif theEnd == '2':
        print('For ACL with wildcard mask:\n')
        for one in netList:
            print(fNetMask(one,1))
    else:
        print('Incorrect input')
