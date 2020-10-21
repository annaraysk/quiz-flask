import requests
from bs4 import BeautifulSoup as bss
import re
import sqlite3

con=sqlite3.connect('creds.db')
c = con.cursor() 
count = 0

def updateDB(l):
    global c
    global count
    global con
    count+=1
    c.execute('insert into mathsQst(qstn,o1,o2,o3,o4,ans,exp) values(?,?,?,?,?,?,?);',l)
    con.commit()
    print('[+] added ',count,l[1])

def updateQuestions(urllink):
    s=requests.get(urllink)
    soup = bss(s.text, features='html.parser')
    l=soup.findAll('p')
    fl=0
    i=0
    while(i<len(l)):
        try:
            if re.search('\d[\.][ ]\w+',l[i].text):
                q=str(l[i].text)
                q=q[q.index(' ')+1:]
                i+=1
                while(True):
                    if str(l[i].text).startswith('(A) '):
                        o1=str(l[i].text)
                        o1=o1[o1.index(' ')+1:]
                        i+=1
                        break
                    else:
                        i+=1
                while(True):
                    if str(l[i].text).startswith('(B) '):
                        o2=str(l[i].text)
                        o2=o2[o2.index(' ')+1:]
                        i+=1
                        break
                    else:
                        i+=1
                while(True):
                    if str(l[i].text).startswith('(C) '):
                        o3=str(l[i].text)
                        o3=o3[o3.index(' ')+1:]
                        i+=1
                        break
                    else:
                        i+=1
                while(True):
                    if str(l[i].text).startswith('(D) '):
                        o4=str(l[i].text)
                        o4=o4[o4.index(' ')+1:]
                        i+=1
                        break
                    else:
                        i+=1
                while(True):
                    if str(l[i].text).startswith('Answer: '):
                        ans=str(l[i].text)
                        ans=ans[ans.index(' ')+1:]
                        i+=1
                        break
                    else:
                        i+=1
                while(True):
                    if str(l[i].text).startswith('Expl'):
                        exp=str(l[i].text)
                        exp=exp[exp.index(' ')+1:]
                        i+=1
                        break
                    else:
                        i+=1
                updateDB([q,o1,o2,o3,o4,ans,exp])

            else:
                i+=1
        except:
            i+=1

f = open('links maths.txt','r')
j=f.readline()
while(j):
    try:
        print('[+] adding ',j)
        updateQuestions(j)
    except:
        print('Fail')
    j=f.readline()
f.close()
con.close()
print('total',count,'questions added')