from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os
import MySQLdb

conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", database = "PyProject")
cursor = conn.cursor()

root = Tk()
root.title("Construction Inventory System")
width = 500
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
#root.geometry("500x500")


#========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()
PRODUCT_NAME = StringVar()
PRODUCT_PRICE = IntVar()
PRODUCT_QTY = IntVar()
SEARCH = StringVar()

#========================================METHODS==========================================

def resizer(e):
    global bg1, resized_bg, new_bg
    
    bg1 = Image.open(r"C:\Users\PC\Desktop\Virtual-Inventory-master\1.jpg")
    resized_bg = bg1.resize((e.width, e.height), Image.ANTIALIAS)
    new_bg = ImageTk.PhotoImage(resized_bg)
    my_canvas.create_image(0, 0, image = new_bg, anchor = "nw")
    my_canvas.create_rectangle(4, 70, 496, 140, outline="black", fill="#873600")
    my_canvas.create_text(250, 100, text = "Construction Inventory System", font = ("Helvetica", 25, "bold"), fill = "white")

    
def Database():
    #global conn, mycursor
    
    #cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY NOT NULL AUTO_INCREMENT, username varchar(20), password varchar(50))")
    cursor.execute("CREATE TABLE IF NOT EXISTS product (product_id int PRIMARY KEY NOT NULL AUTO_INCREMENT, product_name varchar(50), product_qty varchar(10), product_price varchar(10))")
    cursor.execute("SELECT * FROM users WHERE username = 'admin' AND password = 'admin'")
    if cursor.fetchone() is None:
        #cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', 'admin')")
        cursor.execute("INSERT INTO users (username, password) VALUES('admin', 'admin')")
        conn.commit()

    
def ShowLoginForm(e):
    global loginform
    loginform = Toplevel()
    loginform.title("Account Login")
    width = 300
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    loginform.config(bg="#873600")
    LoginForm()


def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=300, height=20, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    image1 = Image.open(r"C:\Users\PC\Desktop\Virtual-Inventory-master\3.jpg")
    #image1 = image1.resize((20, 20), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)
    lbl_text = Label(TopLoginForm, text="  Administrator's Login", font=('arial', 18), width=300)
    label_img = Label(lbl_text, image=test)
    label_img.image = test
    label_img.place(x = 10, y = 3)
    lbl_text.pack(fill=X)

    
    MidLoginForm = Frame(loginform, width=300)
    MidLoginForm.pack(side=LEFT, fill = BOTH, expand = True)
    lbl_username = Label(MidLoginForm, text="Username: ", font=('arial', 15))
    lbl_username.place(x = 5, y = 25)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 15), width=10, relief = SUNKEN)
    username.place(x = 160, y = 25)
    lbl_password = Label(MidLoginForm, text="Password: ", font=('arial', 15))
    lbl_password.place(x = 5, y = 75)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 15), width=10, show="*")
    password.place(x = 160, y = 75)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 12))
    lbl_result.place(x = 20, y = 120 )
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=10, bg = "#873600", fg = "white", command=Login)
    btn_login.place(x = 75, y = 160)
    btn_login.bind('<Return>', Login)


# fetches username and password and validates it(called by LoginForm)
def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        #cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (str(USERNAME.get()), str(PASSWORD.get())))
        
        if cursor.fetchone() is not None:
            
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (str(USERNAME.get()), str(PASSWORD.get())))
            data = cursor.fetchone()
            admin_id = data[0]
            #user_id = data[0]
            #username = data[1]
            #if username = 'admin':
            #   showAdminForm()
            #else:
            #   showUserForm()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")


# called by Login, calls homepage
def ShowHome():
    #print(Home)
    root.withdraw()
    loginform.destroy()
    os.system("python home_page.py")
    #Home()
    
'''
# home page   
def Home():
    global Home, bg_home, canvas
    Home = Toplevel()
    Home.title("Construction Inventory System/Home")
    width = 1024
    height = 520
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)    
    
    bg_home = ImageTk.PhotoImage(file = "images\\construction_background_1024x520.png")
    canvas = Canvas(Home, width = 1024, height = 520)
    canvas.create_image(0, 0, image = bg_home, anchor = "nw")  #nw: northwest
    canvas.pack(fill = "both", expand = True)
    canvas.create_rectangle(260, 70, 780, 140, outline="black", fill="#873600")
    canvas.create_text(520, 100, text = "Construction Inventory System", font = ("Helvetica", 25, "bold"), fill = "white")

    view_button = Button(Home, text = "View Our Products", height = 3, width = 15, relief = RAISED, font = "Helvetica", command = "ShowLoginForm", bg = "white", fg = "#873600")
    view_window = canvas.create_window(200, 250, anchor = "nw", window = view_button)
    view_button.bind('<Button-1>', ShowView)

    product_button = Button(Home, text = "Add New Product", height = 3, width = 15, relief = RAISED, font = "Helvetica", command = "ShowLoginForm", bg = "white", fg = "#873600")
    product_window = canvas.create_window(700, 250, anchor = "nw", window = product_button)
    product_button.bind('<Button-1>', ShowAddNew)
    
    
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    menubar.add_cascade(label="Account", menu=filemenu)
    Home.config(menu=menubar)
    #Home.config(bg="#6666ff")
    Home.mainloop()

            
def ShowView(event = None):
    global viewform
    viewform = Toplevel()
    viewform.title("Construction Inventory System/View Product")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)

    ViewForm()


# view product (called by show view)
def ViewForm():
    global tree
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="View Products", font=('arial', 18), width=600, bg = "#873600", fg = "white")
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('arial', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", bg = "#873600", fg = "white",command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text="Reset", bg = "#873600", fg = "white", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", bg = "#873600", fg = "white", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("ProductID", "Product Name", "Product Qty", "Product Price"), selectmode="browse", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
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

def DisplayData():
    cursor.execute("SELECT * FROM product")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    
    
# searches a product (called by ViewForm)
def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM product WHERE product_name LIKE %s", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        

# resets (called by ViewForm)
def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")


# deletes a product (called by ViewForm)
def Delete():
    if not tree.selection():
        tkMessageBox.showinfo('Construction Inventory System', 'First Select the item you want to delete')
    else:
        result = tkMessageBox.askquestion('Construction Inventory System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            cursor.execute("DELETE FROM product WHERE product_id = %d" % selecteditem[0])
            conn.commit()
            

# add new product
def ShowAddNew(event  = None):
    global addnewform
    addnewform = Toplevel()
    addnewform.title("Construction Inventory System/Add new")
    width = 600
    height = 500
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

    
# add new product
def AddNewForm():
    TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text="Add New Product", font=('arial', 18), width=600, bg = "#873600", fg = "white")
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=600)
    MidAddNew.pack(side=TOP, pady=50)
    lbl_productname = Label(MidAddNew, text="Product Name:", font=('arial', 25), bd=10)
    lbl_productname.grid(row=0, sticky=W)
    lbl_qty = Label(MidAddNew, text="Product Quantity:", font=('arial', 25), bd=10)
    lbl_qty.grid(row=1, sticky=W)
    lbl_price = Label(MidAddNew, text="Product Price (Per Item):", font=('arial', 25), bd=10)
    lbl_price.grid(row=2, sticky=W)
    productname = Entry(MidAddNew, textvariable=PRODUCT_NAME, font=('arial', 25), width=10)
    productname.grid(row=0, column=1)
    productqty = Entry(MidAddNew, textvariable=PRODUCT_QTY, font=('arial', 25), width=10)
    productqty.grid(row=1, column=1)
    productprice = Entry(MidAddNew, textvariable=PRODUCT_PRICE, font=('arial', 25), width=10)
    productprice.grid(row=2, column=1)
    btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg = "#873600", fg = "white", command=AddNew)
    btn_add.grid(row=3, columnspan=2, pady=20)


# adds new product to the database
def AddNew():
    cursor.execute("INSERT INTO product (product_name, product_qty, product_price) VALUES(%s, %s, %s)", (str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get())))
    conn.commit()
    PRODUCT_NAME.set("")
    PRODUCT_PRICE.set("")
    PRODUCT_QTY.set("")


def Logout():
    result = tkMessageBox.askquestion('Simple Inventory System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        #print(Home)
        Home.destroy()
        #del Home
        #print(Home)
   

def Exit2():
    result = tkMessageBox.askquestion('Simple Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()
'''


def Back():
    result = tkMessageBox.askquestion('ADMIN SIDE', 'Do You Want To Exit To Main Menu?',
                                      icon="warning")
    if result == 'yes':

        root.destroy()
        os.system("python pyproj.py")



bg = ImageTk.PhotoImage(file = r"C:\Users\PC\Desktop\Virtual-Inventory-master\1.jpg")
my_canvas = Canvas(root, width = 500, height = 500)


my_canvas.create_image(0, 0, image = bg, anchor = "nw")  #nw: northwest
my_canvas.create_rectangle(4, 70, 496, 140, outline="black", fill="#873600")
my_canvas.create_text(250, 100, text = "Construction Inventory System", font = ("Helvetica", 25, "bold"), fill = "white")

login_button = Button(root, text = "Login", height = 3, width = 10, relief = RAISED, font = ("Helvetica", 18, "bold"), fg = "#873600", command = "ShowLoginForm")
login_window = my_canvas.create_window(190, 200, anchor = "nw", window = login_button)
login_button.bind('<Button-1>', ShowLoginForm)

my_canvas.pack(fill = "both", expand = True)
root.bind('<Configure>', resizer)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="BACK",command=Back)
menubar.add_cascade(label="BACK", menu=filemenu)
root.config(menu=menubar)
if __name__ == '__main__':
    root.mainloop()
