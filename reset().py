def reset():
    import mysql.connector, libraryfunc as lf, random
    db=mysql.connector.connect(user='root',host='Localhost',password='123456')
    dcursor=db.cursor()
    dcursor.execute('drop database if exists library')
    dcursor.execute('create database library')
    dcursor.execute('use library')
    dcursor.execute('drop table if exists books')
    dcursor.execute('''create table books
                        (bid char(4) primary key,
                        bname varchar(50), 
                        author char(25),
                        book_status varchar(50) default'Available',
                        expected_return_date date default NULL,
                        rating float(10),
                        ratingcalc varchar(1000),
                        genre char(25));''')
    dcursor.execute('''insert into books(bid,bname,author,genre)
    values('b01','THE DIARY OF A YOUNG GIRL','ANNE FRANK','BIOGRAPHY'),
    ('b02','EINSTEIN:HIS LIFE AND UNIVERSE','WALTER ISAACSON','BIOGRAPHY'),
    ('b03','BENJAMIN FRANKLIN: AN AMERICAN LIFE','WALTER ISAACSON','BIOGRAPHY'),
    ('b04','LEONARDO DA VINCI','WALTER ISAACSON','BIOGRAPHY'),
    ('b05','NIGHT','ELIE WIESEL','BIOGRAPHY'),
    ('b06','BECOMING','MICHELLE OBAMA','BIOGRAPHY'),
    ('b07','THE STORY OF MY EXPERIMENTS WITH TRUTHS','MAHATMA GANDHI','BIOGRAPHY'),
    ('b08','BATMAN : THE KILLING JOKE','ALAN MOORE','COMICS'),
    ('b09','CHACHA CHAUDHARY','PRAN KUMAR SHARMA','COMICS'),
    ('b10','BIILU','PRAN KUMAR SHARMA','COMICS'),
    ('b11','PINKI','PRAN KUMAR SHARMA','COMICS'),
    ('b12','SAGA SERIES','BRIAN K VAUGHAN','COMICS'),
    ('b13','THE SECRET WARS','JIM SHOOTER','COMICS'),
    ('b14','AVENGERS VS X MEN','BRIAN K VAUGHAN','COMICS'),
    ('b15','INFINITY COUNTDOWN SERIES','GERRY DUGGAN','COMICS'),
    ('b16','DEADPOOL KILLS THE MARVEL UNIVERSE','CULLEN BUNN','COMICS'),
    ('b17',"HARRY POTTER :THE SORCERER'S STONE",'J.K. ROWLING','FANTASY'),
    ('b18','HARRY POTTER AND THE CHAMBER OF SECRETS','J.K. ROWLING','FANTASY'),
    ('b19','HARRY POTTER AND THE PRISONER OF ASKABAN','J.K. ROWLING','FANTASY'),
    ('b20','HARRY POTTER AND THE GOBLET OF FIRE','J.K. ROWLING','FANTASY'),
    ('b21','HARRY POTTER AND THE ORDER OF PHEONIX','J.K. ROWLING','FANTASY'),
    ('b22','HARRY POTTER AND THE HALF BLOOD PRINCE','J.K. ROWLING','FANTASY'),
    ('b23','HARRY POTTER AND THE DEATHLY HALLOWS','J.K. ROWLING','FANTASY'),
    ('b24','HARRY POTTER AND THE CURSED CHILD ','J.K. ROWLING','FANTASY'),
    ('b25','HOBBIT','J.R.R. TOLKEIN','FANTASY'),
    ('b26','GAME OF THRONES','GEORGE R.R. MARTIN','FANTASY'),
    ('b27','THE CHRONICALS OF NARNIA','C.S. LEWIS','FANTASY'),
    ('b28','THE HUNGER GAMES','SUZANNE COLLINS','FANTASY'),
    ('b29','THE ALCHEMIST','PAULO COELHO','FICTION'),
    ('b30','FIVE POINT SOMEONE','CHETAN BHAGAT','FICTION'),
    ('b31','THE THREE MISTAKES OF MY LIFE','CHETAN BHAGAT','FICTION'),
    ('b32','REVOLUTION 2020','CHETAN BHAGAT','FICTION'),
    ('b33','THE SILENT WIDOW','SIDNEY SHELDON','FICTION'),
    ('b34','THE ACCIDENTAL APPRENTICE','VIKAS SWARUP','FICTION'),
    ('b35','SHERLOCK HOLMES SERIES','ARTHUR CONAN DOYLE','FICTION'),
    ('b36','A SUITABLE BOY','VIKRAM SETH','FICTION'),
    ('b37','GUNS , GERMS AND STEEL','JARED DIAMOND','HISTORY'),
    ('b38','SAPIENS : A BRIEF HISTORY OF HUMANKIND','YUVAL NOAH HARARI','HISTORY'),
    ('b39',"A PEOPLE'S HISTORY OF UNITED STATES",'HOWARD ZINN','HISTORY'),
    ('b40','1776 : SEVENTEEN SEVENTY SIX','DAVID MCCULLOUGH','HISTORY'),
    ('b41','THE RISE AND FALL OF THE THIRD REICH','WILLIAM L. SHIRER','HISTORY'),
    ('b42','IN THE GARDEN OF BEASTS','ERIK LARSON','HISTORY'),
    ('b43','CARRIE','STEPHAN KING','HORROR'),
    ('b44','THE SHINING','STEPHAN KING','HORROR'),
    ('b45','IT','STEPHAN KING','HORROR'),
    ('b46','PET SEMATARY','STEPHAN KING','HORROR'),
    ('b47','WORLD WAR Z','MAX BROOKS','HORROR'),
    ('b48','THE EXORCIST','WILLIAM PETER BLATTY','HORROR'),
    ('b49','HEART SHAPED BOX','JOE HILL','HORROR'),
    ('b50','THE PRINCESS BRIDE','WILLIAM GOLDMAN','HUMOR'),
    ('b51','SO LONG, AND THANKS FOR ALL THE FISH','DOUGLAS ADAMS','HUMOR'),
    ('b52','LIFE, THE UNIVERSE AND EVERYTHING','DOUGLAS ADAMS','HUMOR'),
    ('b53',"LET'S EXPLORE DIABETES WITH OWLS",'DAVID SEDARIS','HUMOR'),
    ('b54','THE COLOUR OF MAGIC','TERRY PRATCHETT','HUMOR'),
    ('b55','FIVE POINT SOMEONE','CHETAN BHAGAT','HUMOR'),
    ('b56','ONE NIGHT AT THE CALL CENTRE','CHETAN BHAGAT','HUMOR'),
    ('b57','AND THEN THERE WERE NONE','AGATHA CHRISTLE','MYSTREY'),
    ('b58',"MURDER ON THE ORIENT EXPRESS",'AGATHA CHRISTLE','MYSTREY'),
    ('b59','THE GIRL ON THE TRAIN','PAULA HAWKINS','MYSTREY'),
    ('b60','THE ADVENTURES OF SHERLOCK HOLMES','ARTHUR CONAN DOYLE','MYSTREY'),
    ('b61','THE COMPANION','KATIE ALENDER','MYSTREY'),
    ('b62','THE GIRL IN ROOM 105','CHETAN BHAGAT','MYSTREY'),
    ('b63','THE ACCIDENTAL APPRENTICE','VIKAS SWARUP','MYSTREY'),
    ('b64','WHERE THE CRAWDADS SING','DELLA OWENS','LITERARY FICTION'),
    ('b65','STATION ELEVEN','EMILY ST. JOHN HANDEL','LITERARY FICTION'),
    ('b66','EVERYTHING I NEVER TOLD YOU','CELESTE NG','LITERARY FICTION'),
    ('b67','A GENTLEMEN IN MOSCOW','AMOR TOWLES','LITERARY FICTION'),
    ('b68','TROUBLED BLOOD','J.K. ROWLING','LITERARY FICTION'),
    ('b69','A FURIOUS SKY','ERIC JAY DOLIN','NON FICTION'),
    ('b70','INTO THIN AIR','JON KRAKAUKER','NON FICTION'),
    ('b71','THE FIXED STARS','MOLLY WIZENBERG','NON FICTION'),
    ('b72','IT WAS ALL A LIE','STUART STEVENS','NON FICTION'),
    ('b73','PARADISE LOST','JOHN MILTON','POETRY'),
    ('b74','THE SUN AND HER FLOWERS','RUPI KAUR','POETRY'),
    ('b75','A LIGHT IN THE ATTIC','SHEL SILVERSTEIN','POETRY'),
    ('b76','POEMS OF WILLIAM BLAKE','WILLIAM BLAKE','POETRY'),
    ('b77','A WALK IN THE RAIN','UDAI YADLA','ROMANCE NOVEL'),
    ('b78','ONE INDIAN GIRL','CHETAN BHAGAT','ROMANCE NOVEL'),
    ('b79','2 STATES: THE STORY OF MY MARRIAGE','CHETAN BHAGAT','ROMANCE NOVEL'),
    ('b80','PRIDE AND PREJUDICE','JANE AUSTON','ROMANCE NOVEL'),
    ('b81','TWILIGHT','STEPHENIE MEYER','ROMANCE NOVEL'),
    ('b82','THE FAULT IN OUR STARS','JOHN GREEN','ROMANCE NOVEL'),
    ('b83','FIFTY SHADES OF GREY','E.L. JAMES','ROMANCE NOVEL'),
    ('b84','ROMEO AND JULIET','WILLIAM SHAKESPEARE','ROMANCE NOVEL'),
    ('b85','HALF GIRLFRIEND','CHETAN BHAGAT','ROMANCE NOVEL'),
    ('b86','NINETEEN EIGHTY FOUR','GEORGE ORWELL','SCIENCE FICTION'),
    ('b87','THE TIME MACHINE','H.G. WELLS','SCIENCE FICTION'),
    ('b88',"ENDER'S GAME",'ORSON SCOTT CARD','SCIENCE FICTION'),
    ('b89','THE MARTIAN','ANDY WEIR','SCIENCE FICTION'),
    ('b90','DIVERGENT TRILOGY','VERONICA ROTH','SCIENCE FICTION'),
    ('b91','DECEPTION POINT','DAN BROWN','SCIENCE FICTION'),
    ('b92','ONE ARRANGED MURDER','CHETAN BHAGAT','THRILLER'),
    ('b93','THE SILENT WIFE','KARIN SLAUGHTER','THRILLER'),
    ('b94','THE DA VINCI CODE','DAN BROWN','THRILLER'),
    ('b95','ANGELS AND DEMONS','DAN BROWN','THRILLER'),
    ('b96','GONE GIRL','GILLIAN FLYNN','THRILLER'),
    ('b97','YOU','CAROLINE KEPNES','THRILLER'),
    ('b98','THE WOMEN IN CABIN 10','RUTH WARE','THRILLER'),
    ('b99',"ALICE'S ADVENTURE IN WONDERLAND",'LEWIS CARROLL',"CHILDREN'S LITERATURE"),
    ('b100','A WRINKLE IN TIME',"MADELEINE L'ENGLE","CHILDREN'S LITERATURE"),
    ('b101','THE LION THE WITCH AND THE WARDROBE','C.S. LEWIS',"CHILDREN'S LITERATURE"),
    ('b102','MATILDA','ROALD DAHL',"CHILDREN'S LITERATURE"),
    ('b103','THE JUNGLE BOOK','RUDYARD KIPLING',"CHILDREN'S LITERATURE"),
    ('b104','THE CLOUD CASTLE','THEA STILTON',"CHILDREN'S LITERATURE"),
    ('b105','MATHEMATICS(CLASS 9-12)','RD SHARMA','EDUCATION'),
    ('b106','NEW SIMPLIFIED PHYSICS(CLASS 11 -12)','SL ARORA','EDUCATION'),
    ('b107',"PRADEEP'S NEW COURSE CHEMISTRY(CLASS 11-12)",'S N DHAWAN','EDUCATION'),
    ('b108','ALL IN ONE(CLASS 9-12)','ARIHANT EXPRESS','EDUCATION'),
    ('b109','CBSE QUESTION BANK(CLASS 9-12)','OSWAAL BOOKS','EDUCATION'),
    ('b110','MATHEMATICS(CLASS 6-12)','RS AGGARWAL','EDUCATION'),
    ('b111','CONCEPTS OF PHYSICS(CLASS 11-12)','HC VERMA','EDUCATION'),
    ('b112',"PRADEEP'S NEW COURSE PHYSICS(CLASS 11-12)",'S N DHAWAN','EDUCATION'),
    ('b113','COMPUTER SCIENCE TEXTBOOK(CLASS 11-12)','SUMITA ARORA','EDUCATION'),
    ('b114','COMPUTER SCIENCE WITH PYTHON(CLASS 11-12)','PREETI ARORA','EDUCATION')''')


    dcursor.execute('commit')
    dcursor.execute('select bid from books;')
    bookid=[]
    for x in dcursor:
        bookid.append(x[0])
    for bid in bookid:
        n=random.randint(0,5)
        rt=[n]
        query="update books set ratingcalc='"+str(rt)+"' where bid='"+bid+"';"
        dcursor.execute(query)
    db.commit()




    dcursor.execute('drop table if exists userdb')
    dcursor.execute('''create table userdb
    (uname varchar(20),
    email varchar(50) unique not null primary key,
    password varchar(200),
    borrowed_book varchar(20) default NULL,
    book_borrow_date date,
    Number_of_late_days integer);''')
    lf.adduser('Aditya Satope','adityasatope@gmail.com','Supplemented1')
    lf.adduser('Ayushi Verma','ayushiverma1503@gmail.com','Magnetism')
    lf.adduser('Amaan Dhamaskar','amaan.dhamaskar11@gmail.com','RealtekAudio1')
    lf.adduser('Admin','novelishlibrary@gmail.com','backtocsproject')
    lf.rating()
    dcursor.execute('commit')
    dcursor.close()
reset()
