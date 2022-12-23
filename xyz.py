def libcard(mail):   #  to open the library card of user
    import mysql.connector, libraryfunc as lf
    import csv
    import datetime
    import os
    fname=lf.cardname(mail)+'.csv'
    f=open(fname,'w',newline='')
    wr=csv.writer(f)
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    query="select*from "+lf.cardname(mail)+";"
    dcursor.execute(query)
    lst=[['Book Name','Borrow Date','Return Date','Number of late days']]
    for x in dcursor:
        l=list(x)
        l[1]=str(l[1].strftime('%d/%m/%y')).replace('/','|')
        if l[2]!=None:
            l[2]=str(l[2].strftime('%d/%m/%y')).replace('/','|')
        else:
            l[2]='----'
        lst.append(l)
    wr.writerows(lst)
    print(lst)
    f.close()
