#all functions required for project1

def mail(user_email,msg):
    body='Subject: Notification from Novelish Library\n\n'+msg+'\n\nAny queries? Mail us at novelishlibrary@outlook.com.'
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
    
def otp(email_):
    import random
    num=random.randint(10000,99999)
    text=str(num)+' is your OTP for email verification of Novelish Library.'
    mail(email_,text)
    return num
def encryptt(data):
    from cryptography.fernet import Fernet
    f=open(r'key.txt')
    key=f.read()
    f.close()
    encoded=data.encode()#data converted to bytes
    vl=Fernet(key)
    encrypted=vl.encrypt(encoded)   
    return str(encrypted)[2:-1]

def decryptt(data):
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
def adduser(name,mail,password):
    if '@' in mail and '.com' in mail:
        while len(password)<5:
            print('Password is too short. Password should contain atleast 6 characters')
            password=input('Enter new password')
        import mysql.connector, libraryfunc as lf
        val=str((str(name),str(mail),str(lf.encryptt(password))))
        text=str('insert into userdb(uname,email,password) values'+str(val)+';')
        db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
        dcursor=db.cursor()
        dcursor.execute(text)
        query="create table if not exists "+lf.cardname(mail).lower()+" (book_id varchar(10) not null, borrow_date date not null, return_date date , Number_of_late_days integer);"
        dcursor.execute(query)
        db.commit()
        dcursor.close()
    else:
        print('Enter valid email')
        return 'Enter valid email'

def login_user(userid,password):#checks username and password and returns user's email for further work
    userid=userid.lower()
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='183461',database='library')
    dcursor=db.cursor()
    dcursor.execute('select email,password from userdb;')
    if userid != 'novelishlibrary@gmail.com':
        for x in dcursor:
            if x[0]==userid and lf.decryptt(x[1])==password:
                return x[0]
                break
        else:
                print('Invalid credentials')
    else:
        print('This is an admin id.')

def login_admin(userid,password):
    userid=userid.lower()
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='183461',database='library')
    dcursor=db.cursor()
    dcursor.execute('select email,password from userdb;')
    if userid == 'novelishlibrary@gmail.com':
        for x in dcursor:
            if x[0]==userid and lf.decryptt(x[1])==password:
                return x[0]
                break
        else:
                print('Invalid credentials')
    else:
        print('This is not an admin id.')



 
def userdata(user_email,column_name):
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    query="select "+column_name+" from userdb where email='"+user_email.lower()+"';"
    dcursor.execute(query)
    for x in dcursor:
        return x[0]
        break
def bookdata(bid,coloumn_name):
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    query="select "+coloumn_name+" from books where bid='"+bid.lower()+"';"
    dcursor.execute(query)
    ans=[]
    for x in dcursor:
        return x[0]
        break
def userready(user_email):
    coloumn_name='borrowed_book'
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    query="select "+coloumn_name+" from userdb where email='"+user_email.lower()+"';"
    dcursor.execute(query)
    for x in dcursor:
        return x[0]
        break
def bookready(bid):
    coloumn_name='book_status'
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
    query="select "+coloumn_name+" from books where bid='"+bid.lower()+"';"
    dcursor.execute(query)
    ans=[]
    for x in dcursor:
        ans.append(x)
    return ans

def order(list):
    output=[]
    for i in range(len(list),1,-1):
        for elt in list:
            if list.count(elt)==i:
                if elt not in output:
                    output.append(elt)
    return output


def rating():
    import mysql.connector, libraryfunc as lf
    db=mysql.connector.connect(user='root',host='Localhost',password='123456',database='library')
    dcursor=db.cursor()
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
