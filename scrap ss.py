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
    c.execute('insert into ssQst(qstn,o1,o2,o3,o4,ans,exp) values(?,?,?,?,?,?,?);',l)
    con.commit()
    print('[+] added ',count,l[1])

def updateQuestions(urllink):
    s=requests.get(urllink)
    soup = bss(s.text, features='html.parser')
    l=soup.findAll('p')
    fl=0
    i=0
    for j,i in enumerate(l):
        try:
            if re.search('\d[\.][ ]',i.text):
                q=str(i.text)
                q=q[q.index(' ')+1:]
                q,abcd=q.split('(a) ')
                o1,bcd=abcd.split('(b) ')
                o2,cd=bcd.split('(c) ')
                o3,o4=cd.split('(d) ')
            if str(i.text).startswith('Answer: '):
                ans=str(i.text)
                ans=ans[ans.index(' ')+1:]
                updateDB([q,o1,o2,o3,o4,ans,''])
        except:
            continue
            


f = open('links ss.txt','r')
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