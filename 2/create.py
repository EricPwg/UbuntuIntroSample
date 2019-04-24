t = ['a', 'b', 'c']
for i in range(30):
    print(i)
    for j in range(len(t)):
        f = open(str(i)+t[j]+'.txt', 'w')
        f.write('sample file\n')
        f.write(str(i)+t[j]+'\n')
        f.close()
