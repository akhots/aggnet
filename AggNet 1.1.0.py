# Aggregation of networks. Written on Python 3.6
print('AggNet 1.1.0  Developed by AKhotsyanovskiy\r\n')

def fNetConv(a):
	if a.count('/') == 0:
		b = a.split()
		if len(b) == 1:
			a = a + '/32'
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


def fNetClear(a):
	while a.count([0, 0]) > 0:
		a.remove([0, 0])


def fNetReduce(a):
	for one in range(len(a)-1):
		if a[one][0] + a[one][1] >= a[one+1][0] + a[one+1][1]:
			a[one+1] = [0,0]


def fNetAgg(a):
	for one in range(len(a)-1):
		if a[one][0] + a[one][1] == a[one+1][0]:
			if a[one][1] == a[one+1][1]:
				if a[one][0] / a[one][1] % 2 == 0:
					a[one][1] *= 2
					a[one+1] = [0,0]


def fNetConvB(a):
	c = a[0] // 256**3
	a[0] = a[0] % 256**3
	d = a[0] // 256**2
	a[0] = a[0] % 256**2
	e = a[0] // 256
	a[0] = a[0] % 256
	f = a[0]
	g = 32
	while a[1] != 1:
		a[1] = a[1] / 2
		g -= 1
	return str(c) + '.' + str(d) + '.' + str(e) + '.' + str(f) + '/' + str(g)


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

fNetClear(netListC)

fNetReduce(netListC)
while netListC.count([0, 0]) > 0:
	fNetClear(netListC)
	fNetReduce(netListC)


fNetAgg(netListC)
while netListC.count([0, 0]) > 0:
	fNetClear(netListC)
	fNetAgg(netListC)


netList = []

for one in range(len(netListC)):
	netList.append(fNetConvB(netListC[one]))

print('\r\n')
for one in netList:
	print(one)


outLen = len(netList)

if outLen == inLen:
	print('\r\nThere are no networks to aggregate. Sorry...')
	if inLen > 1:
		print('But they were sorted ;)')
else:
	print('\r\nCongratulations! The networks has been aggregated!')
	print('Amount was reduced from ' + str(inLen) + ' to ' + str(len(netList)))


while exit != 'exit':
	exit = input('\r\nEnter "exit" to exit... ').lower()
quit()
