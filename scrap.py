import requests
from bs4 import BeautifulSoup as bss

def CountTrends(head):
    if head==None:
        return None
    if head.next==None or head.next.next==None:
        return 0
    l=[]
    temp = head.next
    while(temp.next!=None):
        l.append((temp.y-head.y,temp.x-head.x))
        head=head.next
        temp=temp.next
    return len(set(l))-1

    