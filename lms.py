import mysql.connector as sqltor
from datetime import *
import pandas
import getpass
class Member:
    def __init__(self, mem_id, mem_name, mem_addrs, mem_ph, mem_type):
        self.mem_id=mem_id
        self.mem_name=mem_name
        self.mem_addrs=mem_addrs
        self.mem_ph=mem_ph
        self.mem_type=mem_type

class Book:
    def __init__(self, book_id, book_title, book_author, book_genre, book_price, book_quantity):
         self.book_id=book_id
         self.book_title=book_title
         self.book_author=book_author
         self.book_genre=book_genre
         self.book_price=book_price
         self.book_quantity=book_quantity
         
class LibraryManagementSystem:
    def __init__ (self, user, password):
        self.mycon=sqltor.connect(host="localhost",user=user,passwd=password)
        self.cursor=self.mycon.cursor()
        self.dbName = "lms"
        self.create_db()
        self.members()
        self.books()
        self.issues()
        self.submission()
        
    def create_db(self):
        sql1 = "create database if not exists " + self.dbName
        self.cursor.execute(sql1)

    def members(self):
        sql = "create table if  not exists " + self.dbName + ".lib_members(mem_id varchar(40) NOT NULL, \
mem_name varchar(40)NOT NULL, \
mem_addrs varchar(40)NOT NULL,\
mem_ph varchar(40)NOT NULL, \
no_of_books_issued int NOT NULL, \
mem_type varchar(40)NOT NULL)"
        self.cursor.execute(sql)

    def books(self):
        sql = "create table if not exists " + self.dbName + ".books_info(books_id varchar(40)  NOT NULL, \
book_title varchar(40)NOT NULL, \
book_author varchar(40)NOT NULL,\
book_genre varchar(40)NOT NULL, \
book_price varchar(40)NOT NULL, \
book_quantity int  NOT NULL,\
book_status varchar(40)NOT NULL)"
        self.cursor.execute(sql)

    def issues(self):
         sql = "create table if not exists " + self.dbName + ".issues(books_id varchar(40)NOT NULL, \
mem_id varchar(40)NOT NULL, \
issue_dt date NOT NULL, \
issue_status tinyint NOT NULL)"
         self.cursor.execute(sql)

    def submission(self):
         sql = "create table if not exists " + self.dbName + ".submissions(books_id varchar(40)NOT NULL, \
mem_id varchar(40)NOT NULL, \
return_date date NOT NULL)"
         self.cursor.execute(sql)
         

    def add_user(self, member):
        mid = member.mem_id
        name = member.mem_name
        addrs = member.mem_addrs
        phone = member.mem_ph
        typ = member.mem_type
        no_of_books_borrowed = 0
        sql = "insert into " + self.dbName + ".lib_members values(%s, %s, %s, %s, %s, %s)"
        data = (mid, name, addrs, phone, no_of_books_borrowed, typ)
        self.cursor.execute(sql, data)
        self.mycon.commit()

    def auto_generator_mem(self):
        sqlt1 = ("select max(mem_id) from " +self.dbName+ ".lib_members")
        self.cursor.execute(sqlt1)
        tot = self.cursor.fetchone()
        return tot

    def auto_generator_book(self):
        sqlt1 = ("select max(books_id) from " +self.dbName+ ".books_info")
        self.cursor.execute(sqlt1)
        to = self.cursor.fetchone()
        return to

    def check_if_user_has_books(self, mem_id):
        sql1 = "select no_of_books_issued from " + self.dbName + ".lib_members where mem_id=%s"
        data1 = (mem_id, )
        self.cursor.execute(sql1, data1)
        num = self.cursor.fetchall()
        if num == (0,):
            return False
        else:
            return True

    def delete_user(self, mem_id):
        if not self.check_if_user_has_books(mem_id):
            sql = "delete from " + self.dbName + ".lib_members where mem_id=%s"
            mid = (mem_id, )
            self.cursor.execute(sql, mid)
            self.mycon.commit()
        else:
            print("USER STILL HAS BOOKS TO RETURN BEFORE CANCELLING MEMBERSHIP")

    def update_user(self, meid):
        nm = input("ENTER NAME : ")
        ad = input("ENTER ADDRESS : ")
        ph = input("ENTER PHONE NUMBER : ")
        tp = input("ENTER PROFESSION : ")
        memd = Member(meid,nm,ad,ph,tp)
        
        if not self.check_if_user_exists(meid):
            print(f"COULD NOT FIND MEMBER {nm} with id {meid}")
            print(f"CREATING NEW MEMBERSHIP FOR MEMBER {nm} ")
            self.add_user(memd)
        else:
            sql = "update " + self.dbName + ".lib_members set mem_name=%s, mem_addrs=%s, mem_ph=%s, mem_type=%s where mem_id=%s"
            data2 = (nm, ad, ph, tp, meid)
            self.cursor.execute(sql,data2)
            self.mycon.commit()
            print("INFO SUCCESSFULLY UPDATED")#successfully updated
            
    def increment_member_borrowed_book_count(self, mem_id):
        sql1 = "update " + self.dbName + ".lib_members set no_of_books_issued= no_of_books_issued + %s where mem_id = %s"
        data = (1, mem_id )
        self.cursor.execute(sql1, data)
        self.mycon.commit()
        
    def get_member_borrowed_book_count(self, mem_id):
        sql = "select no_of_books_issued from " + self.dbName + ".lib_members where mem_id = %s"
        data = (mem_id, )
        self.cursor.execute(sql, data )
        num_books = self.cursor.fetchone()
        return num_books[0]
        
    def decrement_member_borrowed_book_count(self, mem_id):
        if self.get_member_borrowed_book_count(mem_id) > 0:
            sql1 = "update " + self.dbName + ".lib_members set no_of_books_issued= no_of_books_issued - %s where mem_id = %s"
            data = (1, mem_id )
            self.cursor.execute(sql1, data)
            self.mycon.commit()

    def check_if_user_exists(self, mem_id):
        sql1 = "select count(*) from " + self.dbName + ".lib_members where mem_id = %s";
        data = (mem_id,)
        self.cursor.execute(sql1, data)
        res = self.cursor.fetchone()
        if res != (0,):
            return True
        else:
            return False

    def search_user(self, mem_id):
        if self.check_if_user_exists(mem_id):
            sql1 = "select * from " + self.dbName + ".lib_members where mem_id = %s";
            data = (mem_id, )
            self.cursor.execute(sql1, data)
            res = self.cursor.fetchall()
            print("MEMBER ID : ", res[0][0])
            print("MEMBER NAME : ", res[0][1])
            print("MEMBER ADDRESS : ", res[0][2])
            print("MEMBER PHONE NUMBER : ", res[0][3])
            print("NO. OF BOOKS MEMBER HAS PRESENTLY IN POSSESSION : ", res[0][4])
            print("MEMBER PROFESSION : ", res[0][5])
                
        else:
            print("COULD NOT FIND MEMBER WITH ID {}")

    def search_book(self, book_id):
        if self.check_if_book_exists(book_id):
            sql1 = "select * from " + self.dbName + ".books_info where books_id = %s";
            data = (book_id, )
            self.cursor.execute(sql1, data)
            resf = self.cursor.fetchall()
            print("BOOK ID : ", resf[0][0])
            print("BOOK NAME : ", resf[0][1])
            print("AUTHOR OF BOOK : ", resf[0][2])
            print("BOOK PRICE : ₹", resf[0][3])
            print("BOO GENRE : ", resf[0][4])
            print("NO. OF BOOKS PRESENTLY IN LIBRARY : ", resf[0][5])
        else:
            print("COULD NOT FIND BOOK WITH ID ",book_id)
            

    def check_if_book_exists(self, book_id):
        sql1 = "select count(*) from " + self.dbName + ".books_info where books_id=%s"
        data1 = (book_id, )
        self.cursor.execute(sql1, data1)
        res = self.cursor.fetchone()
        if res != (0,):
            return True
        else:
            return False

    def check_if_book_exists_by_name(self, bname, bauthor):
        sql1 = "select count(*) from " + self.dbName + ".books_info where book_title=%s and book_author=%s"
        data1 = (bname, bauthor)
        self.cursor.execute(sql1, data1)
        res = self.cursor.fetchone()
        if res != (0,):
            return True
        else:
            return False


    def add_books(self, book):
        bid = book.book_id
        title=book.book_title
        author=book.book_author
        genre=book.book_genre
        price=book.book_price
        quantity=book.book_quantity
        
        if self.check_if_book_exists_by_name(title,author):
            self.increment_book_quantity(bid, quantity)
            print("BOOK ALREADY PRESENT. NUMBER OF BOOKS WITH BOOK ID : ",bid," INCREASED BY ",quantity)
        else:
            status="Available"
            sql = "insert into " + self.dbName + ".books_info values(%s, %s, %s, %s, %s, %s, %s)"
            data = (bid, title, author, genre, price, quantity, status)
            self.cursor.execute(sql, data)
            self.mycon.commit()

    def get_book_status(self, book_id):
        if self.check_if_book_exists(book_id):
            sql = "select book_status from " + self.dbName + ".books_info where books_id = %s"
            data = (book_id, )
            self.cursor.execute(sql, data )
            avail = self.cursor.fetchone()
            return avail[0]
        
    def check_book_availability(self, book_id):
        if self.check_if_book_exists(book_id):
            sql = "select book_quantity from " + self.dbName + ".books_info where books_id = %s limit 0,1"
            data = (book_id, )
            self.cursor.execute(sql, data )
            quantity = self.cursor.fetchone()
            if quantity[0] <= 0:
                return False
            else:
                return True
            
    def get_number_of_books_available(self, book_id):
        if self.check_if_book_exists(book_id):
            sql = "select book_quantity from " + self.dbName + ".books_info where books_id = %s"
            data = (book_id, )
            self.cursor.execute(sql, data )
            quantity = self.cursor.fetchone()
            return quantity[0]

    def add_entry_to_issues(self, book_id, mem_id):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql1 = "insert into " + self.dbName + ".issues values(%s, %s, %s, %s)"
        data = (book_id, mem_id, current_time, 1)
        self.cursor.execute(sql1, data)
        self.mycon.commit()
        
    def add_entry_to_submissions(self, book_id, mem_id):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql1 = "insert into " + self.dbName + ".submissions values(%s, %s, %s)"
        data = (book_id, mem_id, current_time)
        self.cursor.execute(sql1, data)
        self.mycon.commit()
        
    def increment_book_quantity(self, book_id, inc):
        sql1 = "update " + self.dbName + ".books_info set book_quantity= book_quantity+%s where books_id = %s"
        data = (inc, book_id )
        self.cursor.execute(sql1, data)
        self.mycon.commit()
        
    def decrement_book_quantity(self, book_id, dec):
        sql1 = "update " + self.dbName + ".books_info set book_quantity= book_quantity-%s where books_id = %s"
        data = (dec, book_id )
        self.cursor.execute(sql1, data)
        self.mycon.commit()
        
    def set_book_status(self, book_id, status):
        sql1 = "update " + self.dbName + ".books_info set book_status= %s where books_id = %s"
        data = (status, book_id )
        self.cursor.execute(sql1, data)
        self.mycon.commit()

    def borrow_book(self, mem_id):
        sql1 = "select books_id from " +self.dbName + ".books_info where book_status='Available'"
        self.cursor.execute(sql1)
        ids=self.cursor.fetchall()
        sql2="select book_title from " +self.dbName + ".books_info where book_status='Available'"
        self.cursor.execute(sql2)
        names=self.cursor.fetchall()
        sql3="select book_author from " +self.dbName + ".books_info where book_status='Available'"
        self.cursor.execute(sql3)
        author=self.cursor.fetchall()
        sql4="select book_genre from " +self.dbName + ".books_info where book_status='Available'"
        self.cursor.execute(sql4)
        genre=self.cursor.fetchall()
        sql5="select book_price from " +self.dbName + ".books_info where book_status='Available'"
        self.cursor.execute(sql5)
        price=self.cursor.fetchall()         
        print ("AVAILABLE BOOKS IN THE LIBRARY : ")
        print("Book id\t\tBook name\t\t\tAuthor\t\t\tGenre\t\t\tPrice")
        for i in range (0,len(ids)):
            print(ids[i][0]+"\t\t"+names[i][0]+"\t\t"+author[i][0]+"\t\t"+genre[i][0]+"\t\t\t₹"+price[i][0])
        print("\n\n\t\t\t\t\t\tBILLING METHOD")
        print("************************************************************************************************************")
        print("\nFIRST 10 DAYS WILL COST ₹30.")
        print("HAVING THE BOOK FOR MORE THAN 10 DAYS WILL COST ₹20 PER DAY AFTER 10 DAY LIMIT.")
        print("IF THE BOOK IS RETURNED IN BAD CONDITION, THE FULL PRICE OF THE BOOK ALONGWITH THE RENT HAS TO BE PAID.")
        bkid=int(input("\n\nEnter book id of book you want to borrow : "))
        self.issue_book(bkid,mem_id)

    def issue_book(self, book_id, mem_id):
        if not self.check_if_user_exists(mem_id):
            print("USER DOES NOT EXIST")
            return
        if self.check_if_book_exists(book_id) and self.check_book_availability(book_id):
            self.add_entry_to_issues(book_id, mem_id)
            if self.get_number_of_books_available(book_id) - 1 == 0:
                self.decrement_book_quantity(book_id, 1)
                self.set_book_status(book_id, "Unavailable")
            else:
                self.decrement_book_quantity(book_id, 1)
            self.increment_member_borrowed_book_count(mem_id)
            print("THE BOOK WITH ID : ", book_id, "HAS BEEN SUCCESSFULLY ISSUED TO MEMBER WITH ID : ",mem_id)
        else:
            print("THE BOOK IS CURRENTLY NOT AVAILABLE")
            
    def check_if_user_was_issued_the_book(self, book_id, mem_id):
        sqlt = "select issue_status from " + self.dbName + ".issues where mem_id = %s and books_id = %s limit 0,1"
        data = (mem_id, book_id, )
        self.cursor.execute(sqlt, data )
        status = self.cursor.fetchone()
        if status == (1,):
            return True
        else:
            return False

        
    
    def update_issue_status(self, book_id, mem_id):
        sql1 = "update " + self.dbName + ".issues set issue_status = %s where books_id = %s and mem_id = %s and issue_status = %s limit 1"
        data = (1, book_id, mem_id, 0 )
        self.cursor.execute(sql1, data)
        self.mycon.commit()
            
    def submit_book(self, book_id, mem_id):
        if not self.check_if_user_exists(mem_id):
            print("USER DOES NOT EXIST")
            return
        if self.get_member_borrowed_book_count(mem_id) <= 0:
            print("USER DOES NOT HAVE ANY BOOK TO RETURN")
            return
        if self.check_if_user_was_issued_the_book(book_id, mem_id): 
            if not self.check_book_availability(book_id):
                self.set_book_status(book_id, "Available")
            self.add_entry_to_submissions(book_id, mem_id)
            self.billing(mem_id, book_id)
            self.increment_book_quantity(book_id, 1)
            self.decrement_member_borrowed_book_count(mem_id)
            self.update_issue_status(book_id, mem_id)
        else:
            print("THE MEMBER WITH ID : ", mem_id , " WAS NOT ISSUED THE BOOK WITH ID : " , book_id )
            return

    def billing(self, mem_id, book_id):
        sql1 = "select issue_dt from " + self.dbName + ".issues where mem_id=%s and books_id=%s limit 0,1"
        data1 = (mem_id, book_id, )
        self.cursor.execute(sql1, data1)
        b = self.cursor.fetchone()
        sql2 = "select return_date from " + self.dbName + ".submissions where mem_id=%s and books_id=%s limit 0,1"
        data2 = (mem_id, book_id, )
        self.cursor.execute(sql2, data2)
        e = self.cursor.fetchone()
        bi = b[0]
        ed = e[0]
        diff = ed - bi
        diff_days = diff.days
        kc = 0
        ch=int(input("CHECK IF BOOK IS DAMAGED : \nPRESS 1 FOR YES\nPRESS 2 FOR NO\nENTER YOUR CHOICE : "))
        if ch == 1:
            sql3 = "select book_price from " + self.dbName + ".books_info where books_id=%s"
            data3 = (book_id, )
            self.cursor.execute(sql3, data3)
            k = self.cursor.fetchone()
            kc = int(k[0])
        if diff_days <= 10:
            bill = 30
        else:
            bill = (20*(diff_days-10))+30
        bill = bill + kc
        print("\nMEMBER WITH ID : ", mem_id , "HAS TO PAY ₹" , bill, " FOR TOTAL OF ", diff_days, " DAYS OF HAVING THE BOOK WITH ID : " , book_id,"\n")
        print("BOOK HAS BEEN SUCCESSFULLY RETURNED")

    def main_menu(self):
        print("\nPLEASE ENTER YOUR DESIGNATION:")
        print("1.ADMINISTRATOR\n2.LIBRARIAN\nPRESS 3 TO EXIT")
        c=input("ENTER 1 OR 2 OR 3 : ")
        valid_selections = ('1', '2', '3')
        if c in valid_selections:
            if c == '3':
                exit()
            
            if c == '1':
                self.admin_login()

            if c == '2':
                self.librarian_login()

        else:
            print("\nWRONG SELECTION. PLEASE TRY AGAIN.\n")
            self.main_menu()

    def change_password(self):
        mfile = open("__adminpass.txt", "w")
        st = input("ENTER NEW PASSWORD : ")
        mfile.write(st)
        mfile.close()
        print("PASSWORD CHANGED SUCCESSFULLY")

    def admin_login(self):
        pasw=getpass.getpass(prompt="PLEASE ENTER YOUR PASSWORD : ")#default password : lms123
        mfile = open("__adminpass.txt", "r")
        pswrd = mfile.read()
        mfile.close()
        if pasw == pswrd:
            print("SUCCESSFULLY LOGGED IN AS ADMIN")
            print("\nAVAILABLE ACTIONS FOR ADMIN : ")
            selections = ('1','2','3','4','5','6','7')
            
            def back():
                x=0
                while True and x == 0:
                    print("\n1.ADD A NEW MEMBER\n2.DELETE AN EXISTING MEMBER\n3.UPDATE MEMBER INFO\n4.SEARCH MEMBER\n5.CHANGE ADMIN PASSWORD\n6.LIBRARIAN ACTIONS\n7.GO BACK")
                    g = input("ENTER YOUR CHOICE : ")
                    if g in selections:
                        x = 1
                    else:
                        print('\nVALUE: {} DID NOT MATCH ANY MENU CHOICE')
                        x = 0
                return g
            p = back()

            def options(q):
                
                if q == '1':
                    nm = input("ENTER NAME : ")
                    ad = input("ENTER ADDRESS : ")
                    ph = input("ENTER PHONE NUMBER : ")
                    tp = input("ENTER PROFESSION : ")
                    t = self.auto_generator_mem()
                    if t == (None,):
                        meid = 1
                    else:
                        ttl = int(t[0])
                        meid = ttl + 1
                    mem = Member(meid,nm,ad,ph,tp)
                    self.add_user(mem)
                    print("MEMBER SUCCESSFULLY ADDED TO RECORDS")
                    p = back()
                    options(p)
                if q == '2':
                    meid = int(input("ENTER MEMBER ID OF MEMBER TO BE DELETED : "))
                    self.delete_user(meid)
                    p = back()
                    options(p)                    
                if q == '3':
                    meid = int(input("ENTER MEMBER ID TO BE UPDATED : "))
                    self.update_user(meid)
                    p = back()
                    options(p)
                if q == '4':
                    meid = int(input("ENTER MEMBER ID TO BE SEARCHED : "))
                    self.search_user(meid)
                    p = back()
                    options(p)
                if q == '5':
                    self.change_password()
                    p = back()
                    options(p)
                if q == '6':
                    self.librarian_login()
                    return
                if q == '7':
                    self.main_menu()
                    return
            
            options(p)
                    
        else:
            print("\nWRONG PASSWORD. PLEASE PRESS 1 TO TRY AGAIN.\nPLEASE PRESS ANY KEY TO GO BACK TO MAIN MENU")
            f = input("ENTER YOUR CHOICE : ")
            if f == '1':
                self.admin_login()
            else:
                self.main_menu()

    def librarian_login(self):
        print("SUCCESSFULLY LOGGED IN AS LIBRARIAN")
        print("\nAVAILABLE ACTIONS FOR LIBRARIAN : ")
        def behind():
            v = 0
            while True and v == 0:
                print("\n1.RENT BOOK\n2.SUBMIT BOOK\n3.ADD BOOKS\n4.SEARCH BOOK\n5.ADMIN ACTIONS\n6.GO BACK")
                selectns = ('1','2','3','4','5','6')
                r = input("ENTER YOUR CHOICE : ")
                if r in selectns:
                    v = 1
                else:
                    print('\nVALUE: ',r,' DID NOT MATCH ANY MENU CHOICE')
                    v = 0
            return r

        d = behind()

        def choices(d):

            if d == '1':
                meid = int(input("ENTER MEMBER ID : "))
                self.borrow_book(meid)
                d = behind()
                choices(d)
            if d == '2':
                meid = int(input("ENTER MEMBER ID : "))
                bokid = int(input("ENTER BOOK ID OF BOOK BEING RETURNED : "))
                self.submit_book(bokid,meid)
                d = behind()
                choices(d)
            if d == '3':
                bnm = input("ENTER NAME OF BOOK : ")
                ath = input("ENTER AUTHOR : ")
                pr = input("ENTER PRICE : ₹")
                gn = input("ENTER GENRE : ")
                qn = int(input("ENTER NUMBER OF BOOKS BEING ADDED : "))
                ts = self.auto_generator_book()
                if ts == (None,):
                    bkid = 1
                else:
                    tt = int(ts[0])
                    bkid = tt + 1
                bookz = Book(bkid,bnm,ath,gn,pr,qn)
                self.add_books(bookz)
                print("BOOK SUCCESSFULLY ADDED TO RECORDS")
                d = behind()
                choices(d)
            if d == '4':
                bkid = int(input("ENTER BOOK ID TO BE SEARCHED : "))
                self.search_book(bkid)
                d = behind()
                choices(d)
            if d == '5':
                self.admin_login()
                return
            if d == '6':
                self.main_menu()
                return

        choices(d)  
        
def main():
    lms = LibraryManagementSystem("root", "qwerty69")
    print("\t\t\t\t\tWELCOME TO THE GREAT LIBRARY\t\t\t")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    lms.main_menu()

if __name__=='__main__':
    main()
            
