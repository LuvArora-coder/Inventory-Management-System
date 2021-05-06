import tkinter
from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import pyscreenshot as ImageGrab
import time
import os
import sys
import csv
from tkinter import scrolledtext
from PIL import Image, ImageTk
import MySQLdb

conn = MySQLdb.connect(host = "localhost", user = "root", password = "root",database="PyProject")
cursor = conn.cursor()
#str='create database PyProject'
#cursor.execute(str)

root = Tk()
root.title("Inventory Management System")

width = 1024
height = 520
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")


USERNAME=StringVar()
PASSWORD=StringVar()
PRODUCT_NAME=StringVar()
PRODUCT_QTY=StringVar()
PRODUCT_NAME=StringVar()
PRODUCT_PRICE=StringVar()
SEARCH=StringVar()





def Database():
    global conn,cursor

    cursor.execute("CREATE TABLE IF NOT EXISTS admin (admin_id int PRIMARY KEY AUTO_INCREMENT , username varchar(20), password varchar(20))")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY AUTO_INCREMENT, username varchar(20), password varchar(50))")
    cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id int PRIMARY KEY  AUTO_INCREMENT, product_name varchar(50), product_qty TEXT, product_price varchar(10))")
    cursor.execute("SELECT * FROM users WHERE username = 'admin' AND password = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO admin (username, password) VALUES('admin', 'admin')")
        cursor.execute("INSERT INTO users (username, password) VALUES('admin', 'admin')")
        conn.commit()



def Exit():
    result = tkMessageBox.askquestion('Simple Inventory System', 'Are you sure you want to exit?', icon="warning")
    cursor.close()
    conn.close()
    if result == 'yes':
        root.destroy()
        exit()


def Logout():
    result = tkMessageBox.askquestion('Simple Inventory System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes':
        admin_id = ""
        root.deiconify()
        Home.destroy()

######LOGIN########
def ShowLoginForm(event=None):
    global loginform
    loginform = Toplevel()
    loginform.title("USER LOGIN")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()

def LoginForm(event=None):
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="User Public Login", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="USERNAME:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="PASSWORD:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=30, command=UserLogin)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', UserLogin)

####REGISTER#####
def ShowRegisterForm(event=None):
    global registerform
    registerform = Toplevel()
    registerform.title("USER LOGIN")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    registerform.resizable(0, 0)
    registerform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    RegisterForm()

def RegisterForm(event=None):
    global lbl_result1,USERNAME,PASSWORD
    TopLoginForm = Frame(registerform, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Register Login", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(registerform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="USERNAME:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="PASSWORD:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_result1 = Label(MidLoginForm, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Register", font=('arial', 18), width=30, command=UserRegister)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', UserRegister)


#####AFTER LOGIN######
def DisplayData():
    cursor.execute("SELECT * FROM product")
    fetch = cursor.fetchall()

    for data in fetch:
        tree.insert('', 'end', values=(data))



def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM product WHERE product_name LIKE %s", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))




# view product (called by show view)
def ViewForm():
    global tree,nameLabel,priceLabel
    TopViewForm = Frame(Home, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(Home, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(Home, width=800)
    MidViewForm.pack(side=RIGHT)



    lbl_text = Label(TopViewForm, text="View Products", font=('arial', 18), width=600, bg = "#873600", fg = "white")
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('arial', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=20)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", bg = "#873600", fg = "white",command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)


    tree = ttk.Treeview(MidViewForm, columns=("ProductID", "Product Name", "Product Qty", "Product Price","CART BUTTON"), selectmode="browse", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('ProductID', text="ProductID",anchor=W)
    tree.heading('Product Name', text="Product Name",anchor=W)
    tree.heading('Product Qty', text="Product Qty",anchor=W)
    tree.heading('Product Price', text="Product Price",anchor=W)

    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=0)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=120)

    tree.pack()
    DisplayData()

def view():
    os.system("python main.py")

def UserHome(event=None):
    global Home
    Home = Toplevel()
    Home.title("WELCOME USER")
    width = 800
    height = 520
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)

    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit)
    filemenu2.add_command(label="VIEW CART", command=view)
    # filemenu2.add_command(label="BUY NOW",command=Cart)
    menubar.add_cascade(label="ACCOUNT", menu=filemenu)
    menubar.add_cascade(label="CART", menu=filemenu2)
    Home.config(menu=menubar)
    Home.config(bg="white")
    ViewForm()


###LOGIN CHECK###
def ShowHome():
    root.withdraw()
    loginform.destroy()
    UserHome()

def UserLogin(event=None):
    global user_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `users` WHERE `username` = %s AND `password` = %s",
                       (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `users` WHERE `username` = %s AND `password` = %s",
                           (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            user_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")

###REGISTERING####
def UserRegister(event=None):
    global user_id , str3
    Database()
    if USERNAME.get() == "" or len(USERNAME.get())==0 or PASSWORD.get() == "" or len(PASSWORD.get())==0:
        lbl_result1.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("INSERT INTO users(username,password) VALUES(%s,%s)",(str(USERNAME.get()), str(PASSWORD.get())))
        conn.commit()
        registerform.destroy()




def ad():
    root.destroy()
    os.system("python index_admin.py")


######FIRST PAGE#######
bg_home = ImageTk.PhotoImage(file = r"C:\Users\PC\Desktop\Virtual-Inventory-master\2.jpg")
canvas = Canvas(root, width = 1024, height = 520)
canvas.create_image(0, 0, image = bg_home, anchor = "nw")  #nw: northwest
canvas.pack(fill = "both", expand = True)
canvas.create_rectangle(260, 70, 780, 140, outline="black", fill="#873600")
canvas.create_text(520, 100, text = "Construction Inventory System", font = ("Helvetica", 25, "bold"), fill = "white")

login_button = Button(root, text = "LOGIN", height = 3, width = 15, relief = RAISED, font = ("Helvetica", 18, "bold"), command = "ShowLoginForm", bg = "white", fg = "#873600")
login_window = canvas.create_window(200, 250, anchor = "nw", window = login_button)
login_button.bind('<Button-1>', ShowLoginForm)

register_button = Button(root, text = "REGISTER", height = 3, width = 15, relief = RAISED, font = ("Helvetica", 18, "bold"), command = "ShowLoginForm", bg = "white", fg = "#873600")
register_window = canvas.create_window(700, 250, anchor = "nw", window = register_button)
register_button.bind('<Button-1>', ShowRegisterForm)



menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="ADMIN",command=ad)
filemenu.add_command(label="EXIT",command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

root.mainloop()






