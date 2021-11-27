import sys
f=open(sys.argv[1],'r',encoding='utf-8')
ff=open('tests/out/temp.txt','w',encoding='utf-8')
res=[]
for line in f:
    res+=[line]
ff.write(''.join(sorted(res)))
f.close()
ff.close()


