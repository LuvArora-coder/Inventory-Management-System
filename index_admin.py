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
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (str(USERNAME.get()), str(PASSWORD.get())))
        
        if cursor.fetchone() is not None:
            
            cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (str(USERNAME.get()), str(PASSWORD.get())))
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
