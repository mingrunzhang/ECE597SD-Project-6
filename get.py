import binascii
import numpy
import matplotlib.pyplot as plt
f = open(r'./kk.txt', 'r')
str_arry =[]

data_arry =[]

line =f.readline()

sign = line

line =line.split(', ')

print str(line)

for str1 in line:

       str_arry.append(str1)

while   sign!='': 

       line = f.readline()

       sign = line 

       line = line.split(', ')

       for str1 in line:

              str_arry.append(str1)

f.close()

str_arry =str_arry[1:-2]

data_arry =str_arry

n =len(str_arry)

for i in range(n):

       if data_arry[i] == '1':

              data_arry[i] = 1

       if data_arry[i] == '0':

              data_arry[i] = 0

       if data_arry[i] == '-1':

              data_arry[i] = -1


data = []

data.append(data_arry[0])

for i in range(1,n):

       if data_arry[i] != data[-1]:

                     data.append(data_arry[i])

data = data[20:-1]

serialnumber= [1,0,-1,0,1,0,1,0,-1,0,1,0,-1,0,-1,0]

serialnumber= serialnumber*2

m =len(serialnumber)

index = 0

for i in range(n-m):

       sign = 0

       for j in range(m):

              if data[i+j] != serialnumber[j]:

                     sign = 1

       if sign == 0:

              index = i+32

              break

print'i='+str(index)

data =data[index:-1]

print'ss'+str(len(data))

new_data =[]

for i in range(len(data)):

       if i%2==0:

              new_data.append(data[i])

for i in range(len(new_data)):

       if new_data[i] == -1:

              new_data[i] = 0

sizeofdata = ''

for i in range(8):

   sizeofdata = sizeofdata+str(new_data[i])

sizeofdata =int(sizeofdata,2)

print str(sizeofdata)

new_data =new_data[8:-1]

rec_string = ''

for i in range(sizeofdata):

       index= i*8

       temp=''

       for i in range(8):

              temp= temp+str(new_data[index+i])

       rec_string= rec_string+chr(int(temp,2))

print 'receive:'+rec_string

f = open(r'./decode.txt','wb')

f.write(rec_string)
