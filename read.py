def intTo2Str(x, k):
	try:
		x = long(x)
	except:
		x = 0
	try:
		k = int(k)
	except:
		k = 0
	if(k < 1):
		k = 1
	if(x < 0):
		fh = 1
		x = -x
	else:
		fh = 0
	a = [0 for j in xrange(0, k)]
	j = k - 1
	while(j>=0) and (x>0):
		y = x % 2
		x = x / 2
		a[j] = y
		j = j - 1
	if fh == 1:
		for j in xrange(0, k):
			if a[j] == 1:
				a[j] = 0
			else:
				a[j] = 1
		j = k - 1
		while j >= 0:
			a[j] = a[j] + 1
			if a[j] <= 1:
				break
			a[j] = 0
			j = j - 1
	return "".join([chr(j+48) for j in a])

f = open(r'./code.txt', 'wb')
send = 'AB'
print send
length = len(send)

serial = [1,0,1,1,0,1,0,0]
serial = serial * 2
print serial
for i in serial:
	f.write(chr(i))

str1 = intTo2Str(length, 8)
for i in range(8):
	temp = str1[i]
	temp = int(temp)
	f.write(chr(temp))

for i in range(length):
	str1 = intTo2Str(ord(send[i]), 8)
	for i in range(8):
		temp = str1[i]
		temp = int(temp)
		f.write(chr(temp))

serial = [1,1,1,1,1,1,1,1]
for i in serial:
	f.write(chr(i))
f.close()
