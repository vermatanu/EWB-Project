from tkinter import *
from tkinter import messagebox
import mysql.connector as sql
import re
import pandas as pd
from tabulate import tabulate
from pandastable import Table, TableModel
from PIL import ImageTk,Image

con = sql.connect(host="localhost", user="root", passwd="mysql@4", database="ewb")
mycursor = con.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS Students (Id INT AUTO_INCREMENT PRIMARY KEY, Roll_No VARCHAR(255) , "
                 "Name VARCHAR(255), Email VARCHAR(255),Contact_Number VARCHAR(10), Total_Hours INT Default 0)")
mycursor.execute("CREATE TABLE IF NOT EXISTS PASSWORD (Id INT AUTO_INCREMENT PRIMARY KEY, PASS VARCHAR(20));")


# ******LOGIN PAGE******
class Login(object):
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)

        self.save_pass()

        self.bg = PhotoImage(file="ewblogin.png")
        self.bg_image = Label(self.root, image=self.bg).place(relx=0, rely=0, relwidth=1, relheight=1)

        # setting up frame
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(relx=0.677, rely=0.295, relheight=0.633, relwidth=0.278)

        # Login heading
        Label(Frame_login, text="Login ", font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(relx=0.5,
                                                                                                       rely=0.07,
                                                                                                       anchor='n')
        # Username heading
        Label(Frame_login, text="Username:", font=("Goudy old style", 15, "bold"), fg="#3CAEA3",
              bg="white").place(relx=0.13, rely=0.27)
        # Username entry
        self.txt_user = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
        self.txt_user.place(relx=0.13, rely=0.37, relwidth=0.7, relheight=0.09)

        # Password heading
        Label(Frame_login, text="Password:", font=("Goudy old style", 15, "bold"), fg="#3CAEA3",
              bg="white").place(relx=0.13, rely=0.47)
        # Password entry
        self.txt_pass = Entry(Frame_login, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_pass.place(relx=0.13, rely=0.57, relwidth=0.7, relheight=0.09)

        # update password button
        upd_pass = Button(Frame_login, text="Forget password? Update now!", bg="white", fg="purple", bd=0,
                         font=("times new roman", 12), command=lambda: Update_password(root) ).place(relx=0.13, rely=0.67)

        # Login button
        # calls up the main frame page
        self.login_btn = Button(Frame_login, command=self.login_fxn, text="Login", bg="white", fg="purple",
                           font=("times new roman", 20)).place(relx=0.5, rely=0.88, relwidth=0.56, relheight=0.12,
                                                               anchor='s')

    # saves pass to variable passwordd
    def save_pass(self):

        query = "Select pass from password;"
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        pass_1 = myresult
        [(x)] = pass_1
        y = list(word for word in x)
        # print(y)
        global passwordd
        passwordd = "".join(y)


    def del_password(self):

        save_pass()
        query = "delete from PASSWORD where pass =%s;"
        val = (passwordd,)
        mycursor.execute(query, val)
        mycursor.execute("SET @num := 0;")
        mycursor.execute("UPDATE PASSWORD SET Id = @num := (@num+1);")
        mycursor.execute("ALTER TABLE PASSWORD AUTO_INCREMENT = 1;")
        con.commit()
        print("DELETED SUCCESSFULLY")

    # Login validator!
    def login_fxn(self):

        if self.txt_pass.get() == "" or self.txt_user.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.txt_pass.get() != passwordd.strip() or self.txt_user.get() != "admin":
            messagebox.showerror("Error", "Invalid user name or password", parent=self.root)
        else:
            Main_page(root)

#****** UPDATE PASSWORD ******
class Update_password(object):
    def __init__(self, root):
        self.root = root
        self.root.title("Update Password")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)

        # setting up image in the background
        self.bg = PhotoImage(file="ewblogin.png")
        self.bg_image = Label(self.root, image=self.bg).place(relx=0, rely=0, relwidth=1, relheight=1)

        # setting up frame
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(relx=0.677, rely=0.295, relheight=0.633, relwidth=0.278)

        # Update password heading
        Label(Frame_login, text="Update Password ", font=("Impact", 25, "bold"), fg="#d77337", bg="white").place(relx=0.5,
                                                                                                       rely=0.07,
                                                                                                       anchor='n')

        # new password heading
        self.newpass = Label(Frame_login, text="New Password:", font=("Goudy old style", 15, "bold"), fg="#3CAEA3",
              bg="white").place(relx=0.13, rely=0.27)
        # new password entry
        self.new_pass = Entry(Frame_login, font=("times new roman", 15), bg="lightgray", show='*')
        self.new_pass.place(relx=0.13, rely=0.37, relwidth=0.7, relheight=0.09)

        # Confirm Password heading
        self.confirmpass= Label(Frame_login, text="Confirm Password:", font=("Goudy old style", 15, "bold"), fg="#3CAEA3",
              bg="white").place(relx=0.13, rely=0.47)
        # COnfirm Password entry
        self.confirm_pass = Entry(Frame_login, font=("times new roman", 15), bg="lightgray", show="*")
        self.confirm_pass.place(relx=0.13, rely=0.57, relwidth=0.7, relheight=0.09)

        Back = Button(Frame_login, text="Back", bg="white", fg="purple", bd=0,
                          font=("times new roman", 12), command=lambda: Login(root)).place(relx=0.13,
                                                                                                     rely=0.67)

        # Submit button
        self.Submit = Button(Frame_login, command=self.check_pass, text="CONFIRM", bg="white", fg="purple",
                           font=("times new roman", 20)).place(relx=0.5, rely=0.88, relwidth=0.56, relheight=0.12,
                                                               anchor='s')

    def check_pass(self):
        if self.new_pass.get() == self.confirm_pass.get():
            self.upd_password(self.new_pass.get())
            messagebox.showinfo("Successful", "Password changed successfully!",parent=self.root)
            Login(root)
        else:
            messagebox.showerror("Error", "Passwords does not match!", parent=self.root)

    def save_pass(self):
        query = "Select pass from password;"
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        pass_1 = myresult
        [(x)] = pass_1
        y = list(word for word in x)
        # print(y)
        global passwordd
        passwordd = "".join(y)

    def del_password(self):
        self.save_pass()
        query = "delete from PASSWORD where pass =%s;"
        val = (passwordd,)
        mycursor.execute(query, val)
        mycursor.execute("SET @num := 0;")
        mycursor.execute("UPDATE PASSWORD SET Id = @num := (@num+1);")
        mycursor.execute("ALTER TABLE PASSWORD AUTO_INCREMENT = 1;")
        con.commit()

    def upd_password(self, newp):
        self.save_pass()
        self.del_password()
        query1 = "insert into password(PASS) values (%s);"
        val = (newp,)
        mycursor.execute(query1, val)
        con.commit()

# ******REGISTER PAGE******
class Register(object):
    def __init__(self, root):
        root.title("Register")
        root.geometry("1199x600+100+50")
        root.resizable(False, False)

        # seeting up the image in the background
        self.bg = PhotoImage(file="ewblogin.png")
        self.bg_image = Label(root, image=self.bg).place(relx=0, rely=0, relwidth=1, relheight=1)

        # setting up the frame
        Frame_register = Frame(root, bg='white')
        Frame_register.place(relx=0.677, rely=0.295, relheight=0.633, relwidth=0.278)

        # Register here heading
        Label(Frame_register, text="Register Here!", font=("Impact", 30, "bold"), fg="#d77337", bg="white").place(
            relx=0.5, rely=0.02, anchor='n', relheight=0.15, relwidth=0.75)

        # Name heading and its entry
        Label(Frame_register, text='Name', font=("Goudy old style", 15, "bold"), fg="#3CAEA3",
              bg="white").place(relx=0.1, rely=0.18)
        self.Name_entry = Entry(Frame_register, font=("times new roman", 13), bg="lightgray")
        self.Name_entry.place(relx=0.1, rely=0.25, relheight=0.07, relwidth=0.75)

        # Email heading and its entry
        Label(Frame_register, text='Email', font=("Goudy old style", 15, "bold"), fg="#3CAEA3",
              bg="white").place(relx=0.1, rely=0.32)
        self.Email_entry = Entry(Frame_register, font=("times new roman", 13), bg="lightgray")
        self.Email_entry.place(relx=0.1, rely=0.39, relheight=0.07, relwidth=0.75)

        # Roll No heading and its entry
        Label(Frame_register, text='Roll No', font=("Goudy old style", 15, "bold"), fg="#3CAEA3",
              bg="white").place(relx=0.1, rely=0.46)
        self.Roll_No_entry = Entry(Frame_register, font=("times new roman", 13), bg="lightgray")
        self.Roll_No_entry.place(relx=0.1, rely=0.53, relheight=0.07, relwidth=0.75)

        # Contact number heading and its entry
        Label(Frame_register, text='Contact Number', font=("Goudy old style", 15, "bold"), fg="#3CAEA3",
              bg="white").place(relx=0.1, rely=0.6)
        self.Contact_num_entry = Entry(Frame_register, font=("times new roman", 13), bg="lightgray")
        self.Contact_num_entry.place(relx=0.1, rely=0.67, relheight=0.07, relwidth=0.75)

        Back = Button(Frame_register, text="Back", bg="white", fg="purple", bd=0,
                        font=("times new roman", 12), command=lambda: Main_page(root)).place(relx=0.1, rely=0.74,relheight=0.07)
        # Submit button and its entry
        self.submit_button = Button(Frame_register, text='Submit', command=lambda: self.submit(), bg='white',
                                    fg="purple", font=("times new roman", 20))
        self.submit_button.place(relx=0.5, rely=0.96, relwidth=0.56, relheight=0.11, anchor='s')


    def submit_validators(self):
        if (self.Name_entry.get() == "") or (self.Roll_No_entry.get() == ""):
            messagebox.showerror("Error", "All fields are required", parent=root)
            return False
        elif not re.findall("@ncuindia.edu", self.Email_entry.get()):
            messagebox.showerror("Error", "Enter valid NCU Email ID", parent=root)
            return False
        elif not re.findall("[0-9]{10}", self.Contact_num_entry.get()):
            messagebox.showerror("Error", "Enter Valid Contact Number", parent=root)
            return False
        else:
            return True


    # enters the data in the database
    def submit(self):
        if self.submit_validators():
            query = "INSERT INTO Students(Roll_No,Name,Email, Contact_Number) VALUES(%s,%s,%s,%s);"
            val = (self.Roll_No_entry.get(), self.Name_entry.get(), self.Email_entry.get(), self.Contact_num_entry.get())
            mycursor.execute(query, val)
            con.commit()
            messagebox.showinfo('Registered', 'The Entry is successful!')
            Register(root)


class Main_page(object):
    def __init__(self, root):
        root.geometry("1199x600+100+50")
        root.resizable(False, False)
        root.title("EWB")

        self.frame = Frame(root, bg = '#8CE983')
        self.frame.place(relheight=1, relwidth=1)

        # self.bg = PhotoImage(file="backg.jpg")
        # self.bg_image = Label(self.root, image=self.bg).place(relx=0, rely=0, relwidth=1, relheight=1)

        # Operations main heading
        Label(self.frame, text="Operations:", bg="black", fg="white", font=("Goudy old style", 25, "bold")).place(relx=0.35, rely=0.02, relheight=0.09, relwidth=0.25)

        #setting up the back button to return to login frame
        self.back = Button(self.frame, text='BACK', font=("Goudy old style", 17, "bold"), bg='black', fg='white',
                           command=lambda: Login(root))
        self.back.place(relx=0.05, rely=0.02, relwidth=0.1, relheight=0.09)


        self.add = Button(self.frame, text="ADD STUDENT", bg="orange", fg="black", font=("Goudy old style", 15, "bold"), command=lambda: Register(root))
        self.add.place(relx=0.15, rely=0.3, relheight=0.1, relwidth=0.25)

        self.delete = Button(self.frame, text="DELETE INFO", bg="orange", fg="black", font=("Goudy old style", 15, "bold"), command=lambda: Delete_info(root))
        self.delete.place(relx=0.15, rely=0.6, relheight=0.1, relwidth=0.25)

        self.pr = Button(self.frame, text="PRINT RECORDS", bg="orange", fg="black", font=("Goudy old style", 15, "bold"), command=lambda: Print_Records(root))
        self.pr.place(relx=0.55, rely=0.3, relheight=0.1, relwidth=0.25)

        self.ad = Button(self.frame, text="ADD DRIVE", bg="orange", fg="black", font=("Goudy old style", 15, "bold"), command=lambda: Add_Drive(root))
        self.ad.place(relx=0.55, rely=0.6, relheight=0.1, relwidth=0.25)

# ******ADD DRIVE PAGE******
class Add_Drive(object):
    def __init__(self, root):
        root.geometry("1199x600+100+50")
        root.resizable(False, False)

        self.frame = Frame(root, bg='#8CE983')
        self.frame.place(relheight=1, relwidth=1)

        # self.bg = PhotoImage(file="backg.jpg")
        # self.bg_image = Label(self.root, image=self.bg).place(relx=0, rely=0, relwidth=1, relheight=1)

        # heading
        Label(self.frame, text="UPDATE RECORDS", bg="BLACK", fg="WHITE", font=("Goudy old style", 20, "bold")).place(relx=0.35, rely=0.05,
                                                                                                relheight=0.09, relwidth=0.25)
        self.back = Button(self.frame, text='BACK', font=("Goudy old style", 17, "bold"), bg='black', fg='white',
                           command=lambda: Main_page(root))
        self.back.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.09)

        Label(self.frame, text="ENTER DRIVE NAME ", bg="orange", fg="black", font=("Goudy old style", 17, "bold")).place(relx=0.15,
                                                                                                    rely= 0.22, relwidth=0.25)
        self.d_name = Entry(self.frame, font=("times new roman", 17), bg="lightgray")
        self.d_name.place(relx=0.5, rely=0.22, width=450)

        Label(self.frame, text="ENTER NO.OF HOURS", bg="orange", fg="black", font=("Goudy old style", 17, "bold")).place(relx=0.15,
                                                                                                    rely=0.32, relwidth=0.25)
        self.hrs = Entry(self.frame, font=("times new roman", 17), bg="lightgray")
        self.hrs.place(relx=0.5, rely=0.32, width=450)

        Label(self.frame, text="ENTER ROLL NOS", bg="orange", fg="black", font=("Goudy old style", 17, "bold")).place(relx=0.15,
                                                                                                    rely=0.42, relwidth=0.25)
        self.roll = Text(self.frame, font=("times new roman", 17), wrap=WORD, bg="lightgray")
        self.roll.place(relx=0.5, rely=0.42, width=450, height=180)

        submit = Button(self.frame, text='SUBMIT', font=("Goudy old style", 20, "bold"),fg='purple', command=lambda: self.Submit(self.roll.get('1.0', 'end'), self.d_name.get(), self.hrs.get()))
        submit.place(relx=0.5, rely=0.88, anchor='s', relwidth=0.2)

    def add_col(self, colname):
        query = "ALTER TABLE Students ADD {} VARCHAR(255) Default 0;".format(colname)
        mycursor.execute(query)
        con.commit()
        query = "ALTER TABLE Students MODIFY Total_Hours INT AFTER {};".format(colname)
        mycursor.execute(query)
        con.commit()

    def Submit(self, roll_nos, drive_name, hours):
        query = "select * from students;"
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        self.field_names = [i[0] for i in mycursor.description]
        if drive_name not in self.field_names:
            self.add_col(drive_name)

        query="Select Roll_No from Students;"
        mycursor.execute(query)
        rolls = mycursor.fetchall()
        print(rolls)
        for roll in roll_nos.split(","):
            if roll.strip() not in rolls[0]:
                messagebox.showerror("Error", "The Roll numbers are not correct!")
                break
            else:
                query = "UPDATE Students SET " + drive_name.strip() + "= %s WHERE Roll_no = %s;"
                value = (hours.strip(), roll.strip(),)
                mycursor.execute(query, value)
                query = "SELECT Total_Hours from Students where Roll_no = %s;"
                value = (roll.strip(),)
                mycursor.execute(query, value)
                total = mycursor.fetchall()
                total = int(total[0][0])
                print(total)
                total = total + int(hours)
                query="Update Students Set Total_Hours = " + str(total) + " WHERE Roll_no = %s;"
                mycursor.execute(query, value)
                con.commit()
                messagebox.showinfo('Succesful', 'The Entry is successful!')
                Add_Drive(root)

# ****** DELETE COLUMN PAGE ******
class Delete_info(object):
    def __init__(self, root):
        root.geometry("1199x600+100+50")
        root.resizable(False, False)

        self.frame = Frame(root, bg='#8CE983')
        self.frame.place(relheight=1, relwidth=1)

        # heading
        Label(self.frame, text="DELETE RECORDS", bg="BLACK", fg="WHITE", font=("Goudy old style", 20, "bold")).place(relx=0.35, rely=0.05,
                                                                                                relheight=0.09, relwidth=0.25)

        self.back = Button(self.frame, text = 'BACK', font=("Goudy old style", 17, "bold"),bg='black', fg='white', command=lambda: Main_page(root))
        self.back.place(relx=0.05, rely=0.05, relwidth= 0.1, relheight=0.09)

        Label(self.frame, text="ENTER ROLL NOS ", bg="orange", fg="black", font=("Goudy old style", 17, "bold")).place(relx=0.15,
                                                                                                    rely= 0.22, relwidth=0.25)

        self.roll = Text(self.frame, font=("times new roman", 17), wrap=WORD, bg="lightgray")
        self.roll.place(relx=0.5, rely=0.22, width=450, height=180)

        submit = Button(self.frame, text='SUBMIT', font=("Goudy old style", 20, "bold"),fg='purple', command=lambda: self.Submit(self.roll.get('1.0', 'end')))
        submit.place(relx=0.5, rely=0.88, anchor='s', relwidth=0.2)

    def Submit(self, roll_no):
        for roll in roll_no.split(","):
            query = "DELETE FROM Students WHERE Roll_no = %s; "
            value = (roll.strip(),)
            mycursor.execute(query, value)
            mycursor.execute("SET @num := 0;")
            mycursor.execute("UPDATE Students SET Id = @num := (@num+1);")
            mycursor.execute("ALTER TABLE Students AUTO_INCREMENT = 1;")
            con.commit()
        messagebox.showinfo('Succesful', 'The Deletion is successful!')
        Delete_info(root)


class Print_Records(object):
    def __init__(self, root):
        root.geometry("1199x600+100+50")
        root.resizable(False, False)

        self.frame = Frame(root, bg='#8CE983')
        self.frame.place(rely=0.05, relheight=0.95, relwidth=1)

        self.frame2 = Frame(root, bg='#8CE983')
        self.frame2.place(relheight=0.05, relwidth=1)

        self.back = Button(self.frame2, text='BACK', command=lambda: Main_page(root))
        self.back.place(relx=0.002,rely=0, relheight=1)

        query = "select * from students;"
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        records = []
        temp = []
        self.field_names = [i[0] for i in mycursor.description]
        for items in myresult:
            for item in items:
                temp.append(item)
            records.append(list(temp))
            temp.clear()

        self.c = pd.DataFrame(records, columns=self.field_names)
        self.table = pt = Table(self.frame, dataframe=self.c,
                                showtoolbar=True, showstatusbar=True)
        pt.show()



root = Tk()

global passwordd

obj = Login(root)
root.mainloop()
