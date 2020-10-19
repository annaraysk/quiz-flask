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
    c.execute('insert into scienceQst values(?,?,?,?,?,?,?);',l)
    con.commit()


def updateQuestions(urllink):
    s=requests.get(urllink)
    soup = bss(s.text, features='html.parser')
    l=soup.findAll('p')
    fl=0
    for i in l:
        if re.search('\d[\.][ ]',i.text):
            if fl==1:
                updateDB([q,o1,o2,o3,o4,ans,''])
                q=''
                o1=''
                o2=''
                o3=''
                o4=''
                ans=''
                fl=0
            q=str(i.text)
            q=q[q.index(' ')+1:]
            if ('A.' in q and 'Ans. ' in q):
                q,abcd=q.split('A. ')
                o1,bcd=abcd.split('B. ')
                o2,cd=bcd.split('C. ')
                o3,d=cd.split('D. ')
                o4,ans=d.split('Ans. ')
                if 'Expla' in ans:
                    ans,exp=ans.split('Explanation: ')
                    updateDB([q,o1,o2,o3,o4,ans,exp])
                    q=''
                    o1=''
                    o2=''
                    o3=''
                    o4=''
                    ans=''
                    exp=''
                    fl=0
                    #print('q',q)
        elif str(i.text).startswith('Ans.'):
            ans=str(i.text)
            ans=ans[ans.index(' ')+1:]
            fl=1
            #print('ans',ans)
        elif str(i.text).startswith('A.'):
            o1=str(i.text)
            o1=o1[o1.index(' ')+1:]
            #print('o1',o1)
        elif str(i.text).startswith('B.'):
            o2=str(i.text)
            o2=o2[o2.index(' ')+1:]
            #print('o2',o2)
        elif str(i.text).startswith('C.'):
            o3=str(i.text)
            o3=o3[o3.index(' ')+1:]
            #print('o3',o3)
        elif str(i.text).startswith('D.'):
            o4=str(i.text)
            o4=o4[o4.index(' ')+1:]
            #print('o4',o4)
        elif str(i.text).startswith('Expla') :
            exp = str(i.text)
            fl=0
            exp=exp[exp.index(' ')+1:]
            #print(exp)
            #print('exp',exp)
            updateDB([q,o1,o2,o3,o4,ans,exp])
            q=''
            o1=''
            o2=''
            o3=''
            o4=''
            ans=''
            exp=''
        
        
        

f = open('q links refined.txt','r')
j=f.readline()
while(j):
    try:
        updateQuestions(j)
    except:
        print('Fail')
    j=f.readline()
f.close()
con.close()
print('total',count,'questions added')