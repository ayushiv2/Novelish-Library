from tkinter import *
from PIL import ImageTk,Image
from tkinter.ttk import Treeview
from tkinter.ttk import Scrollbar
import os
import schedule
import socket

socket.getaddrinfo('localhost',8080)


'----------------------------------------------------------------------------------------------------------------------------------------------------------'




def mail(user_email,msg):     # function to send mail
    body='Subject: Notification from Novelish Library\n\n'+msg+'\n\nAny queries? Mail us at novelishlibrary@outlook.com .'
    import smtplib
    try:
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    except Exception as e:
        smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
    #type(smtpObj) 
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('novelishlibrary@outlook.com', "Backtocsproject") 
    smtpObj.sendmail('novelishlibrary@outlook.com',user_email,body) # Or recipient@outlook
    smtpObj.quit()
    
def otp(email_):    #  to generate otp
    import random
    num=random.randint(10000,99999)
    text=str(num)+' is your OTP for email verification of Novelish Library.'
    mail(email_,text)
    global otpex
    otpex=str(num)
    
def encryptt(data):   #  for encryption of password
    from cryptography.fernet import Fernet
    f=open(r'key.txt')
    key=f.read()
    f.close()
    encoded=data.encode()#data converted to bytes
    vl=Fernet(key)
    encrypted=vl.encrypt(encoded)   
    return str(encrypted)[2:-1]

def decryptt(data):   #  for decryption of password
    from cryptography.fernet import Fernet
    f=open(r'key.txt')
    key=f.read()
    f.close()
    vl=Fernet(key)
    data=bytes(data,'utf-8')
    decrypted=vl.decrypt(data)
    return str(decrypted)[2:-1] #done to convert data to pure string from bytes
def cardname(mail): #because we cant use @ and . in table name
    mail=mail.replace('@','_a_')
    mail=mail.replace('.','_dot_')
    return mail.lower()

def rating():     #  to update the rating of a book
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    dcursor.execute('select ratingcalc from books;')
    rtc=[]
    for x in dcursor:
        rtc.append(eval(x[0]))
    for lst in rtc:
        r=0
        for i in lst:
            r=r+i
        rating=round(r/len(lst),1)
        query="update books set rating="+str(rating)+" where ratingcalc='"+str(lst)+"';"
        dcursor.execute(query)
        db.commit()


def bookdata(bid,coloumn_name):    #  to see a particular book's data
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query="select "+coloumn_name+" from books where bid='"+bid.lower()+"';"
    dcursor.execute(query)
    ans=[]
    for x in dcursor:
        return x[0]
        break
def userready(user_email):   # helping function - to see the borrowed book
    coloumn_name='borrowed_book'
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query="select "+coloumn_name+" from userdb where email='"+user_email.lower()+"';"
    dcursor.execute(query)
    for x in dcursor:
        return x[0]
        break
def bookready(bid):   #  helping function - to see book status 
    coloumn_name='book_status'
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query="select "+coloumn_name+" from books where bid='"+bid.lower()+"';"
    dcursor.execute(query)
    ans=[]
    for x in dcursor:
        ans.append(x)
    return ans

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

REMINDER!!!!!!  You have only 2 days left to return the book "'''+lf.bookdata(x[0],'bname')+'''". Last date to return the book is '''+str(a+datetime.timedelta(days=2))+""".

Regards,
Novelish Library"""
                    lf.mail(i[0],text)


def book_availability():    #to check whether the requested book is available or not
    import mysql.connector
    import libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    f=open('requested_books2.txt','r+')
    d=f.readlines()
    str1=""
    c=0
    for i in d:
        a=i.split('\t')
        query="select book_status from books where bid='"+a[0]+"'"
        dcursor.execute(query)
        for x in dcursor:
            if x[0]=="Available":
                text="""Dear Sir/Madam,

The book that you wanted to read i.e. """+a[1]+""" is now Available for you to read.

Regards,
Novelish Library"""
                lf.mail(a[2],text)
            else:
                c=c+1
                str1=str1+i
    f.close()
    if c!=0:
        f=open('requested_books2.txt','w')
        f.write(str1)
        f.close()


'----------------------------------------------------------------------------------------------------------------------------------------------------------'





def order(list1):   # to arrange the books in order
    output=[]
    for i in range(len(list1),1,-1):
        for elt in list1:
            if list1.count(elt)==i:
                if elt not in output:
                    output.append(elt)
    for i in output:
        Label(recommend_screen,text=i).pack()


def most_read():    #returns list of most read books by all users
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    mails=[]
    books=[]
    final=[]
    dcursor.execute('select*from userdb;')
    for x in dcursor:
        m=lf.cardname(x[1])
        mails.append(m)
    for i in mails:
        query=("select book_id from "+i+";")
        dcursor.execute(query)
        for x in dcursor:
            books.append(x[0])
    return lf.order(books)




def genre_books(mail):  #returns list of recommended books by genre      
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    mail=lf.cardname(mail)
    query="select book_id from "+mail+';'
    dcursor.execute(query)  #see which books the user has read
    books=[]
    k=[]
    genrelist=[]
    for x in dcursor:
        books.append(x[0])
    for bookid in books:
        genre=lf.bookdata(bookid,'genre')
        genrelist.append(genre)
    genrelist=lf.order(genrelist)
    for genre in genrelist:
        query="select bid, bname, genre from books where genre='"+genre+"';"
        dcursor.execute(query)
        for x in dcursor:
            finx=str(x[0])+'\t'+x[1]
            Label(recommend_screen,text=str(finx), anchor='w', bg='#D7D7D7').pack(fill=X)
    if len(genrelist)==0:
        Label(recommend_screen,text="We don't have any recommendations for you", bg='#D7D7D7').pack()



def author_books(mail):    # to recommend books based on author
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    mail=lf.cardname(mail)
    query="select book_id from "+mail+';'
    dcursor.execute(query)
    books=[]
    genrelist=[]
    for x in dcursor:
        books.append(x[0])
    for bookid in books:
        genre=lf.bookdata(bookid,'author')
        genrelist.append(genre)
    genrelist=lf.order(genrelist)
    for genre in genrelist:
        query="select bid, bname,author from books where author='"+genre+"';"
        dcursor.execute(query)
        for x in dcursor:
            if x[0] not in books:
                finx=str(x[0])+'\t'+x[2]+'\t'+x[1]
                Label(recommend_screen,text=str(finx), anchor='w', bg='#D7D7D7').pack(fill=X)
    if len(genrelist)==0:
            Label(recommend_screen,text="We don't have any recommendations for you", bg='#D7D7D7').pack()


def recommendex2():
    genre_books(impmail)


def recommendex1():
    author_books(impmail)


def guirecommend():        
    global recommend_screen
    recommend_screen = Toplevel(main_screen)
    recommend_screen.title("Recommendation")
    recommend_screen.geometry("800x500")
    recommend_screen.config(bg='#D7D7D7')

    Label(recommend_screen,text='', bg='#D7D7D7').pack()
    Label(recommend_screen,text='Recommendation Based On Author :', anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(recommend_screen,text='', bg='#D7D7D7').pack()
    recommendex1()
    Label(recommend_screen,text='', bg='#D7D7D7').pack()
    Label(recommend_screen,text='', bg='#D7D7D7').pack()
    Label(recommend_screen,text='Recommendation Based On Genre :', anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(recommend_screen,text='', bg='#D7D7D7').pack()
    recommendex2()
    Label(recommend_screen,text='', bg='#D7D7D7').pack()
    Label(recommend_screen,text='', bg='#D7D7D7').pack()
    most_read()
    Label(recommend_screen,text='',bg='#D7D7D7').pack()







'----------------------------------------------------------------------------------------------------------------------------------------------------------'


def unsubscribe(mail):     #  to unsubscribe to the membership
    import mysql.connector
    import libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    if lf.userready(mail)==None:
        ans='y'
        if ans=='y' or ans=='Y':
            query="delete from userdb where email='"+mail+"'"
            dcursor.execute(query)
            Label(profile_screen,text='Successfully unsubscribed', bg='#D7D7D7').pack()
            prof_screen.after(2000, lambda:prof_screen.destroy())
            home_screen.after(3000, lambda:home_screen.destroy())
            
    else:
        Label(profile_screen , text='You have not returned all the books yet', bg='#D7D7D7').pack()
    dcursor.execute('commit')



def book_mail(mail):  #  sends mail to the user for borrowing a book
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query="select borrowed_book, book_borrow_date from userdb where email='"+mail+"'"
    dcursor.execute(query)
    for x in dcursor:
        text="""Dear Sir/ Ma'am,

Successfully borrowed the book.
Enjoy your reading!!!


Regards
Novelish Library"""
        lf.mail(mail,text)


def borrow_book(user_email,book_id):  #  to borrow a book
    book_id=str(book_id)
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query='select bid from books'
    dcursor.execute(query)
    l=[]
    for x in dcursor:
        l.append(x[0])
    if book_id not in l:
        Label(profile_screen, text='Invalid book ID', bg='#D7D7D7').pack()
    else:
        if lf.bookready(book_id)[0][0]!='Available':
            Label(profile_screen,text='The Book Is Currently Unavailable', bg='#D7D7D7').pack()
            f=open('requested_books2.txt','a+')
            f.write(book_id)
            f.write('\t')
            book=lf.bookdata(x[0],'bname')
            f.write(book)
            f.write('\t')
            f.write(user_email)
            f.write('\n')
            f.close()
        if lf.userready(user_email)!=None:
            Label(profile_screen,text='You have already borrowed one book.', bg='#D7D7D7').pack()
        if lf.bookready(book_id)[0][0]=='Available' and lf.userready(user_email)==None:
            book_mail(impmail)
            query="update userdb set book_borrow_date=(curdate()), borrowed_book='"+book_id+"' where email='"+user_email.lower()+"';"
            import mysql.connector, libraryfunc as lf
            db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
            dcursor=db.cursor(buffered=True)
            dcursor.execute(query)
            query="update books set book_status='"+user_email.lower()+"', expected_return_date=ADDDATE(curdate(), INTERVAL 15 day) where bid='"+book_id+"';"
            dcursor.execute(query)
            query="insert into "+lf.cardname(user_email)+"(book_id,borrow_date)values('"+book_id+"',curdate());"
            dcursor.execute(query)
            Label(profile_screen,text='Book issued successfully', bg='#D7D7D7').pack()
            db.commit()
            dcursor.close()
            


def return_mail(mail):   #  sends mail to the user for returming the book
    import libraryfunc as lf
    text="""Dear Sir/Ma'am,

You have successfully returned your book.
Thanks for reading!!!

Regards,
Novelish Library"""
    lf.mail(mail,text)
        
def return_book(mail,rating):  #  to return a book
    mail=mail.lower()
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    book_id=str(lf.userdata(mail,'borrowed_book'))
    rtc=eval(lf.bookdata(book_id,'ratingcalc'))         #to convert str into list
    if book_id=='None':
        Label(profile_screen,text='You have not issued any book', bg='#D7D7D7').pack()
    else:
        if rating>5 or rating<0:
            Label(profile_screen,text='Enter a valid rating.', bg='#D7D7D7').pack()
        else:
            rtc.append(rating)
            query1="select adddate((select book_borrow_date from userdb where borrowed_book='"+book_id+"' and email='"+mail+"'),interval 15 day);"
            dcursor.execute(query1)
            for x in dcursor:
                dat1=x[0]
            dcursor.execute('select curdate();')
            for x in dcursor:
                dat2=x[0]
            if dat2>dat1:
                query="update "+lf.cardname(mail)+" set return_date=curdate(),Number_of_late_days=(datediff(adddate((select book_borrow_date from userdb where book_id='"+book_id+"' and email='"+mail+"'),interval 15 day), curdate())) where book_id='"+book_id+"';"
            else:
                query="update "+lf.cardname(mail)+" set return_date=curdate(),Number_of_late_days=0 where book_id='"+book_id+"';"
            dcursor.execute(query)
            query="update books set book_status='Available',expected_return_date=NULL,ratingcalc='"+str(rtc)+"' where bid='"+book_id+"';"
            dcursor.execute(query)
            db.commit()
            query="update userdb set borrowed_book=NULL, book_borrow_date=NULL, Number_of_late_days=(select sum(Number_of_late_days) from "+lf.cardname(mail)+" )  where email='"+mail+"';"
            db.commit()
            dcursor.execute(query)
            
            db.commit() 
            Label(profile_screen,text='Book returned successfully', bg='#D7D7D7').pack()
            lf.rating()








def userdata(user_email,column_name):   #  helping function - to find user's particular data
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query="select "+column_name+" from userdb where email='"+user_email.lower()+"';"
    dcursor.execute(query)
    for x in dcursor:
        return x[0]
    

def guiprofileex5():
    unsubscribe(impmail)

def gui_profileex5():
    global guip_screen
    guip_screen = Toplevel(main_screen)
    guip_screen.title("Unsubscribe?")
    guip_screen.geometry("250x100+100+500")
    guip_screen.config(bg='#D7D7D7')

    Label(guip_screen, text='', bg='#D7D7D7').pack()
    Label(guip_screen, text='Are you sure?', bg='#D7D7D7').pack()

    def yes():
        guiprofileex5()
        guip_screen.after(1000, lambda:guip_screen.destroy())
    
    def no():
        guip_screen.after(2000, lambda:guip_screen.destroy())


    Button(guip_screen, text='Yes', justify='left', command=yes).pack()
    Button(guip_screen, text='No', justify='right', command=no).pack()
    

def guiprofileex4():
    request_book(impmail,profborrow1)


def guiprofileex3():
    global profborrow1
    profborrow1 = profborrow.get()
    profborrowentry.delete(0, END)
    borrow_book(impmail,profborrow1)
    


def guiprofileex2():
    profrating1 = profrating.get()
    profratingentry.delete(0, END)
    return_book(impmail,int(profrating1))
    return_mail(impmail)

def guiprofileex():     #  changed
    userdataans=userdata(impmail,'uname')
    global profname
    global profmail
    global profbookborrowed
    global profborroweddate
    global proflatedays
    profname='Name : '+str(userdataans)
    profmail='Email : '+impmail
    borrowed_book=userdata(impmail,'borrowed_book')
    profbookborrowed='Book Borrowed : '+str(borrowed_book)
    bbdate=userdata(impmail,'book_borrow_date')
    profborroweddate='Book Borrow Date : '+str(bbdate)
    latedays=userdata(impmail,'Number_of_late_days')
    proflatedays='No. Of Late Days : '+str(latedays)
    



def guiprofile():     #   changed
    from tkinter import ttk
    global profile_screen
    global prof_screen
    prof_screen = Toplevel(main_screen)
    prof_screen.title("Profile")
    prof_screen.geometry("600x650")
    prof_screen.config(bg='#D7D7D7')

    main_frame=Frame(prof_screen)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas=Canvas(main_frame)

    my_scrollbar=ttk.Scrollbar(main_frame, orient=VERTICAL)
    my_scrollbar.pack(side=RIGHT, fill=Y )
    my_scrollbar.config(command=my_canvas.yview)

    my_canvas.config(scrollregion=my_canvas.bbox('all'))
    my_canvas.config(yscrollcommand=my_scrollbar.set)
    my_canvas.config(bg='#D7D7D7')
    my_canvas.pack(side=LEFT, fill=BOTH ,expand=1)

    profile_screen=Frame(my_canvas)
    profile_screen.config(bg='#D7D7D7')

    profile_screen.bind(
        "<Configure>",
        lambda e: my_canvas.configure(
            scrollregion=my_canvas.bbox("all")
        )
    )

    my_canvas.create_window((0,0),window=profile_screen, anchor="nw")

    guiprofileex()

    Label(profile_screen, text="Please Scroll Down for further Details", bg='#D7D7D7', justify='center').pack()
    Label(profile_screen, text=profname ,anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(profile_screen, text="", bg='#D7D7D7').pack()
    Label(profile_screen, text=profmail ,anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(profile_screen, text="", bg='#D7D7D7').pack()
    Label(profile_screen, text=profbookborrowed ,anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(profile_screen, text="", bg='#D7D7D7').pack()
    Label(profile_screen, text=profborroweddate ,anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(profile_screen, text="", bg='#D7D7D7').pack()
    Label(profile_screen, text=proflatedays ,anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(profile_screen, text="", bg='#D7D7D7').pack()
    Label(profile_screen, text="", bg='#D7D7D7').pack()
    Label(profile_screen, text="In Order To Return Your Borrowed Book" ,anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(profile_screen, text=" Enter Rating (1-5) And Press Return " ,anchor='w', bg='#D7D7D7').pack(fill=X)

    global profrating
     
    profrating = StringVar()
     
    global profratingentry
     
    profratingentry = Entry(profile_screen, textvariable=profrating)
    profratingentry.pack()
    Label(profile_screen, text="", bg='#D7D7D7').pack()

    Button(profile_screen, text="Return Book",command=guiprofileex2,anchor='w').pack(fill=X)
    Label(profile_screen, text="", bg='#D7D7D7').pack()
    Label(profile_screen, text="", bg='#D7D7D7').pack()


    Label(profile_screen, text="In Order To Borrow Book",anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(profile_screen, text="  Enter It's Book Id  ",anchor='w', bg='#D7D7D7').pack(fill=X)

    global profborrow
     
    profborrow = StringVar()
     
    global profborrowentry
     
    profborrowentry = Entry(profile_screen, textvariable=profborrow)
    profborrowentry.pack()

    Button(profile_screen, text="Borrow Book",command=guiprofileex3,anchor='w').pack(fill=X)

    Label(profile_screen, text="", bg='#D7D7D7').pack()
    Label(profile_screen, text="", bg='#D7D7D7').pack()
    
    Label(profile_screen, text='To Unsubscibe From The Membership',anchor='w', bg='#D7D7D7').pack(fill=X)
    Label(profile_screen, text='  Press The Unsubscribe Button  ',anchor='w', bg='#D7D7D7').pack(fill=X)
    Button(profile_screen, text=' Unsubscribe ',command=gui_profileex5,anchor='w').pack(fill=X)
    






'----------------------------------------------------------------------------------------------------------------------------------------------------------'




def search_book(name):      # to search a book
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query="select bid,bname from books where bname like '%"+name+"%'"
    dcursor.execute(query)
    matches=[]
    for x in dcursor:
        str=''+x[0]+'\t'+x[1]+''
        matches.append(str.title())  
    return matches

def search_genre(genre):   # to search a book based on genre
    genre=genre.upper()
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query="select bid,bname from books where genre like '%"+genre+"%';"
    dcursor.execute(query)
    matches=[]
    for x in dcursor:
        str=''+x[0]+'\t'+x[1]
        matches.append(str.title())
    return matches


def all_genre():    #  to print all genres
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    query="select distinct genre from books"
    dcursor.execute(query)
    matches=[]
    c=0
    for x in dcursor:
        str=''+x[0]
        matches.append(str.title())
        c=c+1
    return matches,c

def netreview(bid):   # to check for a book's review on net
    import mysql.connector, libraryfunc as lf, webbrowser
    text=lf.bookdata(bid,'bname').title()+' reviews'
    webbrowser.open('https://www.google.com/search?q='+text+'&rlz=1C1CHBF_enIN924IN924&oq=hiiii&aqs=chrome..69i57j0l3j0i395l5j0i10i395.1131j1j9&sourceid=chrome&ie=UTF-8')




def netreview2():    
    bid_entry_get= bid_entry.get()
    netreview(bid_entry_get)

def bookreview():    #  to make book review screen
    global bookreview_screen

    bookreview_screen = Toplevel(main_screen)
    bookreview_screen.title("Book Review")
    bookreview_screen.geometry("500x500")
    bookreview_screen.config(bg='#D7D7D7')

    Label(bookreview_screen, text="Please enter the Book ID for review", bg='#D7D7D7').pack()
    Label(bookreview_screen,text='', bg='#D7D7D7').pack()

    global bid_verify
    bid_verify = StringVar()
    global bid_entry
    bid_entry= Entry(bookreview_screen, textvariable=bid_verify)
    bid_entry.pack()
    Label(bookreview_screen, text='', bg='#D7D7D7').pack()

    Button(bookreview_screen, text='Review', height=1, width=15, command=netreview2).pack()

    
    

    

def allgenre():   #  to display all genres on the screen
    global allgenre_screen

    allgenre_screen = Toplevel(main_screen)
    allgenre_screen.title("All Genres")
    allgenre_screen.geometry("500x500")
    allgenre_screen.config(bg='#D7D7D7')
        
    matches,c=all_genre()
    str1='Total '+str(c)+' Genres'
    Label(allgenre_screen,text=str1, bg='#D7D7D7').pack()
    Label(allgenre_screen,text='________________________________________________________', bg='#D7D7D7').pack()
    for i in range(0,len(matches)):
        Label(allgenre_screen,text=matches[i] ,anchor='w', bg='#D7D7D7').pack(fill=X)

def booklist():    #   to display all the book's data
    from tkinter import ttk
    import mysql.connector

    global booklist_screen
    bookl_screen = Toplevel(main_screen)
    bookl_screen.title("Book List")
    bookl_screen.geometry("800x500+300+150")
    bookl_screen.config(bg='#D7D7D7')
    
    main_frame=Frame(bookl_screen)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas=Canvas(main_frame)

    my_scrollbar=ttk.Scrollbar(main_frame, orient=HORIZONTAL)
    my_scrollbar.pack(side=BOTTOM, fill=X )
    my_scrollbar.config(command=my_canvas.xview)

    my_canvas.config(scrollregion=my_canvas.bbox('all'))
    my_canvas.config(xscrollcommand=my_scrollbar.set)
    my_canvas.pack(side=TOP, fill=BOTH ,expand=1)

    booklist_screen=Frame(my_canvas)


    booklist_screen.bind(
        "<Configure>",
        lambda e: my_canvas.configure(
            scrollregion=my_canvas.bbox("all")
        )
    )

    my_canvas.create_window((0,0),window=booklist_screen, anchor="nw")



    table = Treeview(booklist_screen, show='headings', column=('a','b','c','d','e','f'), height=21)

    vbar = Scrollbar(booklist_screen, orient="vertical", command=table.yview)

    table.configure(yscroll=vbar.set)
    table.grid(row=2, columnspan=10)
    vbar.grid(row=2, column=10, sticky='NS')
    table.column('a', width=200, anchor="center")
    table.column('b', width=200, anchor="center")
    table.column('c', width=200, anchor="center")
    table.column('d', width=200, anchor="center")
    table.column('e', width=200, anchor="center")
    table.column('f', width=200, anchor="center")

    table.heading('a', text='BOOK ID')
    table.heading('b', text='BOOK NAME')
    table.heading('c', text='AUTHOR')
    table.heading('d', text='BOOK STATUS')
    table.heading('e', text='RATING')
    table.heading('f', text='GENRE')

    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    dcursor.execute('select bid,bname,author,book_status,rating,genre from books')

    for x in dcursor:
        a=x[3]
        if a!='Available':
            a='Unavailable'
        table.insert("", 'end', text ="L1",  
                 values =(x[0], x[1],x[2],a,x[4],x[5]))





def searchgenre():  
    from tkinter import ttk
    global searchgenre_screen

    searchtag1 = searchtag.get()
    if len(searchtag1)==0:
        Label(search_screen, text="Please enter text to search!!", bg='#D2BFC2').pack()
    else:
        searchg_screen = Toplevel(main_screen)
        searchg_screen.title("Search By Genre")
        searchg_screen.geometry("500x500")
        searchg_screen.config(bg='#D7D7D7')
        
        main_frame=Frame(searchg_screen)
        main_frame.pack(fill=BOTH, expand=1)

        my_canvas=Canvas(main_frame)

        my_scrollbar=ttk.Scrollbar(main_frame, orient=VERTICAL)
        my_scrollbar.pack(side=RIGHT, fill=Y )
        my_scrollbar.config(command=my_canvas.yview)

        my_canvas.config(scrollregion=my_canvas.bbox('all'))
        my_canvas.config(yscrollcommand=my_scrollbar.set)
        my_canvas.config(bg='#D7D7D7')
        my_canvas.pack(side=LEFT, fill=BOTH ,expand=1)

        searchgenre_screen=Frame(my_canvas)


        searchgenre_screen.bind(
            "<Configure>",
            lambda e: my_canvas.configure(
                scrollregion=my_canvas.bbox("all")
            )
        )

        my_canvas.create_window((0,0),window=searchgenre_screen, anchor="nw")
        
        searchtag_entry.delete(0, END)
        matches=search_genre(searchtag1)
        if matches==[]:
            Label(searchgenre_screen, text="No match found!!", bg='#D7D7D7').pack()
        else:
            for i in range(0,len(matches)):
                Label(searchgenre_screen,text=matches[i] ,anchor='w', bg='#D7D7D7').pack(fill=X)

def searchbook():     
    from tkinter import ttk
    global searchbook_screen
    
    searchtag1 = searchtag.get()
    if len(searchtag1)==0:
        Label(search_screen, text="Please enter text to search!!", bg='#D2BFC2').pack()
    else:
        searchb_screen = Toplevel(main_screen)
        searchb_screen.title("Search By Book Name")
        searchb_screen.geometry("500x500")
        searchb_screen.config(bg='#D7D7D7')

        main_frame=Frame(searchb_screen)
        main_frame.pack(fill=BOTH, expand=1)

        my_canvas=Canvas(main_frame)

        my_scrollbar=ttk.Scrollbar(main_frame, orient=VERTICAL)
        my_scrollbar.pack(side=RIGHT, fill=Y )
        my_scrollbar.config(command=my_canvas.yview)

        my_canvas.config(scrollregion=my_canvas.bbox('all'))
        my_canvas.config(yscrollcommand=my_scrollbar.set)
        my_canvas.config(bg='#D7D7D7')
        my_canvas.pack(side=LEFT, fill=BOTH ,expand=1)

        searchbook_screen=Frame(my_canvas)


        searchbook_screen.bind(
            "<Configure>",
            lambda e: my_canvas.configure(
                scrollregion=my_canvas.bbox("all")
            )
        )

        my_canvas.create_window((0,0),window=searchbook_screen, anchor="nw")

        searchtag_entry.delete(0, END)
        matches=search_book(searchtag1)
        if matches==[]:
            Label(searchbook_screen, text="No match found!!", bg='#D7D7D7').pack()
        else:
            for i in range(0,len(matches)):
                Label(searchbook_screen,text=matches[i] ,anchor='w', bg='#D7D7D7').pack(fill=X)

def searchauthor():   
    from tkinter import ttk
    global searchauthor_screen
    import mysql.connector

    searchtag1 = searchtag.get()
    if len(searchtag1)==0:
        Label(search_screen, text="Please enter text to search!!", bg='#D2BFC2').pack()
    else:
        searcha_screen = Toplevel(main_screen)
        searcha_screen.title("Search By Author Name")
        searcha_screen.geometry("600x500")
        searcha_screen.config(bg='#D7D7D7')

        main_frame=Frame(searcha_screen)
        main_frame.pack(fill=BOTH, expand=1)

        my_canvas=Canvas(main_frame)

        my_scrollbar=ttk.Scrollbar(main_frame, orient=HORIZONTAL)
        my_scrollbar.pack(side=BOTTOM, fill=X )
        my_scrollbar.config(command=my_canvas.xview)

        my_canvas.config(scrollregion=my_canvas.bbox('all'))
        my_canvas.config(xscrollcommand=my_scrollbar.set)
        my_canvas.config(bg='#D7D7D7')
        my_canvas.pack(side=TOP, fill=BOTH ,expand=1)

        searchauthor_screen=Frame(my_canvas)


        searchauthor_screen.bind(
            "<Configure>",
            lambda e: my_canvas.configure(
                scrollregion=my_canvas.bbox("all")
            )
        )

        my_canvas.create_window((0,0),window=searchauthor_screen, anchor="nw")
    
        searchtag_entry.delete(0, END)
        table = Treeview(searchauthor_screen, show='headings', column=('a','b','c'), height=21)

        vbar = Scrollbar(searchauthor_screen, orient="vertical", command=table.yview)

        table.configure(yscroll=vbar.set)
        table.grid(row=2, columnspan=10)
        vbar.grid(row=2, column=10, sticky='NS')
        table.column('a', width=200, anchor="center")
        table.column('b', width=200, anchor="center")
        table.column('c', width=200, anchor="center")
        
        table.heading('a', text='BOOK ID')
        table.heading('b', text='BOOK NAME')
        table.heading('c', text='AUTHOR')

        db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
        dcursor=db.cursor(buffered=True)
        query="select bid,bname,author from books where author like'%"+searchtag1+"%'"
        dcursor.execute(query)

        for x in dcursor:
            table.insert("", 'end', text ="L1",  
                     values =(x[0], x[1],x[2]))







def guisearch():    
    global search_screen
    search_screen = Toplevel(main_screen)
    search_screen.title("Search")
    search_screen.geometry("800x500+300+150")
    search_screen.config(bg='#D2BFC2')
    Label(search_screen, text="Please enter Name To Search", bg='#D2BFC2').pack()
    Label(search_screen, text="", bg='#D2BFC2').pack()

    global searchtag
    global searchtag_entry
    searchtag = StringVar()

    searchtag_entry = Entry(search_screen, textvariable=searchtag)
    searchtag_entry.pack()
    Label(search_screen, text="", bg='#D2BFC2').pack()

    Button(search_screen, text="Search By Author Name",command=searchauthor, width=20, height=1).pack()
    Label(search_screen, text="", bg='#D2BFC2').pack()
    Button(search_screen, text="Search By Book Name",command=searchbook, width=20, height=1).pack()
    Label(search_screen, text="", bg='#D2BFC2').pack()
    Button(search_screen, text="Search By Genre",command=searchgenre, width=20, height=1).pack()
    Label(search_screen, text="", bg='#D2BFC2').pack()
    Button(search_screen, text="Book list",command=booklist, width=20, height=1).pack()
    Label(search_screen, text="", bg='#D2BFC2').pack()
    Button(search_screen, text="All Genre",command=allgenre, width=20, height=1).pack()
    Label(search_screen, text="", bg='#D2BFC2').pack()
    Button(search_screen, text="Book Review",command=bookreview, width=20, height=1).pack()
    


def help():     #   to save helping instructions in text file
    f=open('help.txt','w')
    str='''General Instructions:
You are allowed to borrow a book for 14 days.
Only one book can be borrowed at a time.
Messages are displayed at the bottom of the screen.

How to:

1. Search a Book?
    -Go to Search
    -Press 'Book List' for the whole list of books
    -If you want to search a Book based on Author, Book Name, or Genre type
    your search query in the text area given and press the corresponding button
    -Look for the Book ID of the book you want to borrow and remember it

2. Borrow a Book?
    -Go to search and look for the Book ID
    -Then go to Profile and Enter the Book ID under the 'Borrow Book' section
    and press 'Borrow Book'
    
3. Return a Book?
    -Go to Profile
    -Tell us how did you like the Book out of 5 and press 'Return Book'

4. Unsubscribe to your Membership?
    -Go to Profile
    -After returning all the Books that you have borrowed press 'Unsubscribe'


For any other queries write to us at novelishlibrary@gmail.com :)'''

    f.write(str)
    f.close()

    f=open('help.txt','r')
    d=f.read()
    f.close()
    return d

def guihelp():    #  to display help instructions
    global help_screen
    help_screen = Toplevel(main_screen)
    help_screen.title("Help")
    help_screen.geometry("900x700+200+100")
    help_screen.config(bg='#D7D7D7')

    h=help()
    Label(help_screen, text=h ,justify='left', bg='#D7D7D7').pack()

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
    f.close()
    path='G:\\AYUSHI\\python programs\\cs project 2020-21\\PROGRAM\\final program\\'+fname
    os.startfile(path)

def gui_lc():
    libcard(impmail)



    


'----------------------------------------------------------------------------------------------------------------------------------------------------------'





def guihome():
    global home_screen
    home_screen = Toplevel(main_screen)
    home_screen.title("Dashboard")
    home_screen.geometry("800x500+300+150")
    home_screen.config(bg='#D2BFC2')
    Label(home_screen,text="NOVELISH LIBRARY", width="300", height="2", font=("Calibri", 13), bg='#D2BFC2').pack()
    Label(home_screen,text="", bg='#D2BFC2').pack()
    Button(home_screen,text="Profile", height="2", width="30",command=guiprofile).pack()
    Label(home_screen,text="", bg='#D2BFC2').pack()
    Button(home_screen,text="Recommendation", height="2", width="30",command=guirecommend).pack()
    Label(home_screen,text="", bg='#D2BFC2').pack()
    Button(home_screen,text="Search", height="2", width="30",command=guisearch).pack()
    Label(home_screen,text="", bg='#D2BFC2').pack()
    Button(home_screen,text="Library Card", height="2", width="30",command=gui_lc).pack()
    
    
    Button(home_screen,text="Help?", height='2', width='15', command=guihelp).place(relx=1.0,rely=1.0, anchor='se')



'----------------------------------------------------------------------------------------------------------------------------------------------------------'


def remove_book(bid):   #   to remaove a book
    import mysql.connector
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    query="delete from books where bid='"+bid+"'"
    dcursor.execute(query)
    dcursor.execute('commit')
    Label(remove_screen,text='Book removed succesfuly', bg='#D7D7D7').pack()


def removebookex2():   
    bookidr1 = bookidr_verify.get()
    bookidr_entry.delete(0, END)

    remove_book(bookidr1)


def removebookex():   
    global remove_screen
    remove_screen = Toplevel(main_screen)
    remove_screen.title("Remove Book")
    remove_screen.geometry("500x500")
    remove_screen.config(bg='#D7D7D7')
    Label(remove_screen, text="Please Enter Book Id To Remove Book", bg='#D7D7D7').pack()
    Label(remove_screen, text="", bg='#D7D7D7').pack()
 
    global bookidr_verify
 
    bookidr_verify = StringVar()
 
    global bookidr_entry
    
    bookidr_entry = Entry(remove_screen, textvariable=bookidr_verify)
    bookidr_entry.pack()
    Label(remove_screen, text="", bg='#D7D7D7').pack()
    Button(remove_screen, text="Remove", width=10, height=1,command=removebookex2).pack()




'----------------------------------------------------------------------------------------------------------------------------------------------------------'



def new_book(bid,nm,author,genre):   #  to add new book
    import mysql.connector
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    l=[0]
    str1="'"+bid+"','"+nm.upper()+"','"+author.upper()+"','"+genre.upper()+"','"+str(l)+"'"
    query='insert into books(bid,bname,author,genre,ratingcalc) values('+str1+')'
    dcursor.execute(query)
    dcursor.execute('commit')


    
def newbookex2():  
    newbookid_info = newbookid.get()
    newbookname_info = newbookname.get()
    newauthor_info = newauthor.get()
    newgenre_info = newgenre.get()
     
    newbookid_entry.delete(0, END)
    newbookname_entry.delete(0, END)
    newauthor_entry.delete(0, END)
    newgenre_entry.delete(0, END)

    new_book(newbookid_info,newbookname_info,newauthor_info,newgenre_info)

    Label(newbook_screen, text="Book Added", bg='#D7D7D7').pack()

    
    
            
    
def newbookex ():         # new book screen
    global newbook_screen
    newbook_screen=Toplevel(main_screen)
    newbook_screen.title('Add New Book')
    newbook_screen.geometry("500x500")
    newbook_screen.config(bg='#D7D7D7')
    
    Label(newbook_screen,text='', bg='#D7D7D7').pack()

    global newbookid
    global newbookname
    global newbookid_entry
    global newbookname_entry
    global newauthor
    global newgenre
    global newauthor_entry
    global newgenre_entry
    newbookid = StringVar()
    newbookname = StringVar()
    newauthor = StringVar()
    newgenre = StringVar()
 
    Label(newbook_screen, text="Please enter details below", bg='#D7D7D7').pack()
    Label(newbook_screen, text="", bg='#D7D7D7').pack()

    Label(newbook_screen, text="Book Id * ", bg='#D7D7D7').pack()
    newbookid_entry = Entry(newbook_screen, textvariable=newbookid)
    newbookid_entry.pack()

    Label(newbook_screen, text="Book Name * ", bg='#D7D7D7').pack()
    newbookname_entry = Entry(newbook_screen, textvariable=newbookname)
    newbookname_entry.pack()

    Label(newbook_screen, text="Author Name * ", bg='#D7D7D7').pack()
    newauthor_entry = Entry(newbook_screen, textvariable=newauthor)
    newauthor_entry.pack()

    Label(newbook_screen, text="Genre * ", bg='#D7D7D7').pack()
    newgenre_entry = Entry(newbook_screen, textvariable=newgenre)
    newgenre_entry.pack()
    
    Label(newbook_screen, text="", bg='#D7D7D7').pack()
    Button(newbook_screen, text="Add Book", width=10, height=1,command=newbookex2).pack()

def guiuserdata():   #  to display user's data
    import mysql.connector
    from tkinter import ttk
    
    global userd_screen
    userd_screen =  Toplevel(main_screen)
    userd_screen.title("User's Data")
    userd_screen.geometry('600x350')
    userd_screen.config(bg='#D7D7D7')

    main_frame=Frame(userd_screen)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas=Canvas(main_frame)

    my_scrollbar=ttk.Scrollbar(main_frame, orient=HORIZONTAL)
    my_scrollbar.pack(side=BOTTOM, fill=X )
    my_scrollbar.config(command=my_canvas.xview)

    my_canvas.config(scrollregion=my_canvas.bbox('all'))
    my_canvas.config(xscrollcommand=my_scrollbar.set)
    my_canvas.pack(side=TOP, fill=BOTH ,expand=1)

    userdata_screen=Frame(my_canvas)


    userdata_screen.bind(
        "<Configure>",
        lambda e: my_canvas.configure(
            scrollregion=my_canvas.bbox("all")
        )
    )

    my_canvas.create_window((0,0),window=userdata_screen, anchor="nw")



    table = Treeview(userdata_screen, show='headings', column=('a','b','c','d','e'), height=16)
    
    table.grid(row=2, columnspan=10)
    table.column('a', width=200, anchor="center")
    table.column('b', width=200, anchor="center")
    table.column('c', width=200, anchor="center")
    table.column('d', width=200, anchor="center")
    table.column('e', width=200, anchor="center")

    table.heading('a', text='NAME')
    table.heading('b', text='EMAIL ID')
    table.heading('c', text='BORROWED BOOK')
    table.heading('d', text='BOOK BORROW DATE')
    table.heading('e', text='NO. OF LATE DAYS')

    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    dcursor.execute('select uname,email,borrowed_book,book_borrow_date,Number_of_late_days from userdb')

    for x in dcursor:
        table.insert("", 'end', text ="L1",  
                 values =(x[0], x[1],x[2],x[3],x[4]))


def guibookdata():  #  to display book's data
    import mysql.connector
    from tkinter import ttk
    
    global bookd_screen
    bookd_screen =  Toplevel(main_screen)
    bookd_screen.title("Book Data")
    bookd_screen.geometry('800x500+300+150')
    bookd_screen.config(bg='#D7D7D7')

    main_frame=Frame(bookd_screen)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas=Canvas(main_frame)

    my_scrollbar=ttk.Scrollbar(main_frame, orient=HORIZONTAL)
    my_scrollbar.pack(side=BOTTOM, fill=X )
    my_scrollbar.config(command=my_canvas.xview)

    my_canvas.config(scrollregion=my_canvas.bbox('all'))
    my_canvas.config(xscrollcommand=my_scrollbar.set)
    my_canvas.pack(side=TOP, fill=BOTH ,expand=1)

    bookdata_screen=Frame(my_canvas)


    bookdata_screen.bind(
        "<Configure>",
        lambda e: my_canvas.configure(
            scrollregion=my_canvas.bbox("all")
        )
    )

    my_canvas.create_window((0,0),window=bookdata_screen, anchor="nw")



    table = Treeview(bookdata_screen, show='headings', column=('a','b','c','d','e','f','g'), height=21)

    vbar = Scrollbar(bookdata_screen, orient="vertical", command=table.yview)

    table.configure(yscroll=vbar.set)
    table.grid(row=2, columnspan=10)
    vbar.grid(row=2, column=10, sticky='NS')
    table.column('a', width=200, anchor="center")
    table.column('b', width=200, anchor="center")
    table.column('c', width=200, anchor="center")
    table.column('d', width=200, anchor="center")
    table.column('e', width=200, anchor="center")
    table.column('f', width=200, anchor="center")
    table.column('g', width=200, anchor="center")

    table.heading('a', text='BOOK ID')
    table.heading('b', text='BOOK NAME')
    table.heading('c', text='AUTHOR')
    table.heading('d', text='BOOK STATUS')
    table.heading('e', text='EXPECTED RETURN DATE')
    table.heading('f', text='RATING')
    table.heading('g', text='GENRE')

    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    dcursor.execute('select bid,bname,author,book_status,expected_return_date,rating,genre from books')

    for x in dcursor:
        table.insert("", 'end', text ="L1",  
                 values =(x[0], x[1],x[2],x[3],x[4],x[5],x[6]))






'----------------------------------------------------------------------------------------------------------------------------------------------------------'


def guiowner():
    global owner_screen
    owner_screen = Toplevel(main_screen)
    owner_screen.title("Owner-Dashboard")
    owner_screen.geometry("800x500+300+150")
    owner_screen.config(bg='#D2BFC2')

    Label(owner_screen,text='', bg='#D2BFC2').pack()
    Button(owner_screen,text='Add New Book', height="2", width="30", command=newbookex).pack()
    Label(owner_screen,text='', bg='#D2BFC2').pack()
    Button(owner_screen,text='Remove Book', height="2", width="30", command=removebookex).pack()
    Label(owner_screen,text='', bg='#D2BFC2').pack()
    Button(owner_screen,text="User's Data", height="2", width="30", command=guiuserdata).pack()
    Label(owner_screen,text='', bg='#D2BFC2').pack()
    Button(owner_screen,text="Book list", height="2", width="30", command=guibookdata).pack()
    

'----------------------------------------------------------------------------------------------------------------------------------------------------------'


def adduser(name,mail,password):   #  to add user
    if '@' in mail and '.com' in mail:
        import mysql.connector, libraryfunc as lf
        val=(str(name),str(mail),str(lf.encryptt(password)))
        text=str('insert into userdb(uname,email,password) values'+str(val)+';')
        db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
        dcursor=db.cursor(buffered=True)
        dcursor.execute(text)
        query="create table if not exists "+lf.cardname(mail).lower()+" (book_id varchar(10) not null, borrow_date date not null, return_date date , Number_of_late_days integer);"
        dcursor.execute(query)
        db.commit()
    else:
        return 'Enter valid email'


def registerex():   #  to send mail for registering
    import libraryfunc as lf
    regotp1=regotp.get()
    if regotp1==otpex:
        adduser(regname_info,regmail_info,password_info)
        Label(register_screen, text="Registration Success", bg='#D7D7D7').pack()
        guihome()
        text='''Dear Sir/Ma'am,

Thank you for subscribing to Novelish Library. For any queries feel free to contact us at novelishlibrary@gmail.com.

Regards,
Novelish Library'''
        lf.mail(impmail,text)
        



def register_user():    

    global password_info
    global regmail_info
    global regname_info 
    password_info = gpassword.get()
    regmail_info = regmail.get()
    regname_info = regname.get()
    global impmail
    impmail=regmail_info
 
    password_entry.delete(0, END)
    regmail_entry.delete(0, END)
    regname_entry.delete(0, END)

    
    otp(regmail_info)

    Label(register_screen, text="Please Enter OTP Sent To Your Mail", bg='#D7D7D7').pack()

    global regotp
    global regotp_entry
    Label(register_screen, text="", bg='#D7D7D7').pack()

    regotp=StringVar()
    regotp_entry = Entry(register_screen, textvariable=regotp)
    regotp_entry.pack()

    Label(register_screen, text="", bg='#D7D7D7').pack()

    Button(register_screen, text="Enter", command = registerex).pack()



    
def register():    # register screen
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("800x500+300+150")
    register_screen.config(bg='#D7D7D7')
 
    global gpassword
    global password_entry
    global regmail
    global regname
    global regmail_entry
    global regname_entry

    gpassword = StringVar()
    regmail = StringVar()
    regname = StringVar()
 
    Label(register_screen, text="Please enter details below", bg='#D7D7D7').pack()
    Label(register_screen, text="", bg='#D7D7D7').pack()
    
    regmail_lable = Label(register_screen, text="Email Id * ", bg='#D7D7D7')
    regmail_lable.pack()
    regmail_entry = Entry(register_screen, textvariable=regmail)
    regmail_entry.pack()
    
    regname_lable = Label(register_screen, text="Name * ", bg='#D7D7D7')
    regname_lable.pack()
    regname_entry = Entry(register_screen, textvariable=regname)
    regname_entry.pack()
    
    password_lable = Label(register_screen, text="Password * ", bg='#D7D7D7')
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=gpassword, show='*')
    password_entry.pack()
    
    Label(register_screen, text="", bg='#D7D7D7').pack()
    Button(register_screen, text="Register", width=10, height=1, command = register_user).pack()



'----------------------------------------------------------------------------------------------------------------------------------------------------------'

def resetpass(mail,newpass):  #  to reset password
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    ps=str(lf.encryptt(newpass))
    test="update userdb set password='"+ps+"' where email='"+mail+"';"
    dcursor.execute(test)
    db.commit()

def guiresetpass():  #  reset password screen
    
    global reset_screen
    reset_screen = Toplevel(main_screen)
    reset_screen.title("Forgot Password")
    reset_screen.geometry("500x500")
    reset_screen.config(bg='#D7D7D7')

    global email_verify
    global email_entry

    email_verify = StringVar()
    
    Label(reset_screen, text="Please enter your Email ID", bg='#D7D7D7').pack()
    email_entry = Entry(reset_screen, textvariable=email_verify)
    email_entry.pack()
    Button(reset_screen, text="Submit", width=10, height=1, command=gui_rp).pack()
    Label(reset_screen, text="", bg='#D7D7D7').pack()

def gui_rp3():
    otp(email1)
    

def gui_rp2():
    p=p_verify.get()
    p1=p1_verify.get()
    otp1=otp_verify.get()

    if p==p1 and otp1==otpex:
        resetpass(email1,p)
        p_entry.delete(0,END)
        p1_entry.delete(0,END)
        otp_entry.delete(0,END)
        text_p='''Password changed
Please go back to Login screen to login to your Dashboard'''
        Label(reset_screen, text=text_p, bg='#D7D7D7').pack()
        
    elif p==p1 and otp1!=otpex:
        Label(reset_screen, text="Invalid otp!!!", bg='#D7D7D7').pack()
        Button(reset_screen, text="Resend otp", bg="#D7D7D7", command=gui_rp3).pack()
        p_entry.delete(0,END)
        p1_entry.delete(0,END)
        otp_entry.delete(0,END)
    elif p!=p1 and otp1==otpex:
        Label(reset_screen, text="Passwords don't match...Please enter again", bg='#D7D7D7').pack()
        p_entry.delete(0,END)
        p1_entry.delete(0,END)
        otp_entry.delete(0,END)


def gui_rp():  # password resetting continued....
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    dcursor.execute('select email from userdb;')

    global email1
    email1=email_verify.get()
    global cz
    cz=0
    for x in dcursor:
        if x[0]==email1:
            cz=1
            break
    if cz==1:
        Label(reset_screen, text='________________________________', bg='#D7D7D7').pack()
        Label(reset_screen, text='', bg='#D7D7D7').pack()
        Label(reset_screen, text="Enter new password", bg='#D7D7D7').pack()
        global p_verify
        global p_entry
        global p1_verify
        global p1_entry
        global otp_verify
        global otp_entry
        
        p_verify = StringVar()
        p_entry = Entry(reset_screen, textvariable=p_verify, show='*')
        p_entry.pack()
        Label(reset_screen, text="", bg='#D7D7D7').pack()

        Label(reset_screen, text="Confirm new password", bg='#D7D7D7').pack()
        p1_verify = StringVar()
        p1_entry = Entry(reset_screen, textvariable=p1_verify, show='*')
        p1_entry.pack()

        Label(reset_screen, text='', bg='#D7D7D7').pack()
        otp(email1)
        Label(reset_screen, text='Enter otp', bg='#D7D7D7').pack()
        otp_verify = StringVar()
        otp_entry = Entry(reset_screen, textvariable=otp_verify)
        otp_entry.pack()
        
        Button(reset_screen, text='Set', command=gui_rp2).pack()
        Label(reset_screen, text="", bg='#D7D7D7').pack()

    elif cz!=1:
        Label(reset_screen, text="Invalid Email ID", bg='#D7D7D7').pack()
        email_entry.delete(0,END)


        

 



'----------------------------------------------------------------------------------------------------------------------------------------------------------'




def login(userid,password):    #  to check whether the user exists or  not
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor(buffered=True)
    dcursor.execute('select email,password from userdb;')
    c=0
    for x in dcursor:
        if x[0]==userid and lf.decryptt(x[1])==password:
            guihome()
            c=c+1
    if c==0:
        Label(login_screen, text='Invalid Details!!', bg='#D7D7D7').pack()

def guiloginex():
    username1 = username_verify.get()
    password1 = password_verify.get()           
    global impmail
    impmail=username1
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    
    if impmail=='novelishlibrary@gmail.com' and password1=='boardproject' :
        guiowner()
    else :
        login(username1,password1)

def guilogin():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("800x500+300+150")
    login_screen.config(bg='#D7D7D7')
    Label(login_screen, text="Please enter details below to login", bg='#D7D7D7').pack()
    Label(login_screen, text="", bg='#D7D7D7').pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Email Id * ", bg='#D7D7D7').pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="", bg='#D7D7D7').pack()
    Label(login_screen, text="Password * ", bg='#D7D7D7').pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Button(login_screen, text='forgot password?', width=15, height=1, command=guiresetpass).pack()
    Label(login_screen, text="", bg='#D7D7D7').pack()
    Label(login_screen, text='', bg='#D7D7D7').pack()
    Button(login_screen, text="Login", width=15, height=2,command=guiloginex).pack()
          


'----------------------------------------------------------------------------------------------------------------------------------------------------------'



def main_account_screen():   # main screen (main program function)
    global main_screen
    main_screen = Tk()
    main_screen.geometry("800x500+300+150")
    main_screen.configure(bg='#7EC4FF')
    main_screen.title(" Welcome ")
    icon=PhotoImage(file='novelish_icon.png')
    main_screen.iconphoto(True,icon)
    Label(text="NOVELISH LIBRARY", width="300", height="2", font=("Calibri", 13), bg='#7EC4FF').pack()

    logo=Image.open("novelish_logo.jpg")
    logo_r=logo.resize((300,225), Image.ANTIALIAS)

    my_img=ImageTk.PhotoImage(logo_r)
    Label(image=my_img).pack()

    Label(text="" ,bg='#7EC4FF').pack()
    Button(text="Login", height="2", width="30",command=guilogin).pack()
    Label(text="", bg='#7EC4FF').pack()
    Button(text="Register", height="2", width="30",command=register).pack()
 
    main_screen.mainloop()

main_account_screen()

# checks for reminding the user to return the book two days prior to the return date everyday at 12 am
schedule.every().day.at("00:00").do(twoday_reminder)
# checks for book availability everyday at 12 am
schedule.every().day.at('00:00').do(book_availability)
while True:
    schedule.run_pending()



