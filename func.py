def new_book():
    import mysql.connector
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    bid=input('Enter book id :')
    nm=input('Enter book name :')
    author=input("Enter author's name :")
    genre=input('Genre of the book :')
    str="'"+bid+"','"+nm+"','"+author+"','"+genre+"'"
    query='insert into books(bid,bname,author,genre) values('+str+')'
    print(query)
    dcursor.execute(query)
    dcursor.execute('commit')
    
def unsubscribe(mail):
    import mysql.connector
    import libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    if lf.userready(mail)==None:
        ans=input('Are you sure uou want to unsubscribe to the library?(y/n)')
        if ans=='y' or ans=='Y':
            query="delete from userdb where email='"+mail+"'"
            dcursor.execute(query)
            print('Successfully unsubscribed!')
        else:
            print('Okay!!')
    else:
        print('You have not returned all the books yet!!')
    dcursor.execute('commit')
       
def twoday_reminder():    #sends an email 2 days prior to the return date as a reminder
    import mysql.connector
    import libraryfunc as lf
    import datetime
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    dcursor.execute('select email from userdb')
    for i in dcursor:
        if lf.userready(i[0])!=None:
            query="select borrowed_book, book_borrow_date from userdb where email='"+i[0]+"'"
            dcursor.execute(query)
            for x in dcursor:
                a=x[1]+datetime.timedelta(days=13)
                today=datetime.date.today()
                if a==today:
                    text='''Dear Sir/Madam,

REMINDER!!!!!!  You have only 2 days left to return the book "'''+lf.bookdata(x[0],'bname')+'''". Last date to return the book is '''+str(a+datetime.timedelta(days=2))+"""

Regards,
Novelish Library"""
                    lf.mail(i[0],text)
    
def requests():     #all the requested books will be listed 
    import mysql.connector
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    f=open('requested_books.txt','r+')
    d=f.readlines()
    print('Requested books by customers:')
    for i in d:
        i=i.split()
        print(i[0],'\t',i[1])   
    f.close()

def request_book(bid,mail):     #to request for a book
    global email
    email=mail
    import mysql.connector
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    query="select * from books where bid='"+bid+"'"
    dcursor.execute(query)
    for x in dcursor:
        if x[3]!="Available":
            f=open('requested_books.txt','a+')
            f.write(x[0])
            f.write('\t')
            f.write(x[1])
            f.write('\t')
            f.write(email)
            f.write('\n')
            f.close()
            print('Book requested')

def book_availability():    #to check whether the requested book is available or not
    import mysql.connector
    import libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    f=open('requested_books.txt','r+')
    d=f.readlines()
    str=""
    c=0
    for i in d:
        a=i.split('\t')
        query="select book_status from books where bid='"+a[0]+"'"
        dcursor.execute(query)
        for x in dcursor:
            if x[0]=="Available":
                text="""Dear Sir/Madam,

The book that you requested for i.e. """+a[1]+""" is now Available for you to read.

Regards,
Novelish Library"""
                lf.mail(a[2],text)
            else:
                c=c+1
                str=str+i
    f.close()
    if c!=0:
        f=open('requested_books.txt','w')
        f.write(str)
        f.close()


import schedule
schedule.every().day.at("00:00").do(twoday_reminder)
schedule.every().day.at('00:00').do(book_availability)
while True:
    schedule.run_pending()

            
