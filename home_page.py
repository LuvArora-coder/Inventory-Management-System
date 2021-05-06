from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os
import re
import MySQLdb

conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", database = "PyProject")
cursor = conn.cursor()


Home = Tk()
Home.title("Construction Inventory System/Home")
width = 1024
height = 520
screen_width = Home.winfo_screenwidth()
screen_height = Home.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
Home.resizable(0, 0)
Home.lift()
#========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()
PRODUCT_NAME = StringVar()
PRODUCT_PRICE = IntVar()
PRODUCT_QTY = IntVar()
SEARCH = StringVar()


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
        tkMessageBox.showinfo('Construction Inventory System/Delete', 'First Select the item you want to delete')
        viewform.lift()
    else:
        result = tkMessageBox.askquestion('Construction Inventory System/Delete', 'Are you sure you want to delete this record?', icon="warning")
        viewform.lift()
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

    #if re.search('[a-zA-Z]', PRODUCT_QTY.get()) and re.search('[a-zA-Z]', PRODUCT_PRICE.get()):
        #tkMessageBox.showinfo('Construction Inventory System/Add New', 'Price and Quality should be integer')
    
    #else:
    try:
        cursor.execute("INSERT INTO product (product_name, product_qty, product_price) VALUES(%s, %s, %s)", (str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get())))
        conn.commit()
        PRODUCT_NAME.set("")
        PRODUCT_PRICE.set("")
        PRODUCT_QTY.set("")

    except:
        tkMessageBox.showinfo('Construction Inventory System/Add Product', 'Enter correct values')
        addnewform.lift()
    
        

def Logout():
    result = tkMessageBox.askquestion('Construction Inventory System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        #root.deiconify()
        #print(Home)
        Home.destroy()
        os.system("python index_admin.py")
        #del Home
        #print(Home)
    

def Exit2():
    result = tkMessageBox.askquestion('Construction Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()



bg_home = ImageTk.PhotoImage(file = r"C:\Users\PC\Desktop\Virtual-Inventory-master\2.jpg")
canvas = Canvas(Home, width = 1024, height = 520)
canvas.create_image(0, 0, image = bg_home, anchor = "nw")  #nw: northwest
canvas.pack(fill = "both", expand = True)
canvas.create_rectangle(260, 70, 780, 140, outline="black", fill="#873600")
canvas.create_text(520, 100, text = "Construction Inventory System", font = ("Helvetica", 25, "bold"), fill = "white")

view_button = Button(Home, text = "View Our Products", height = 3, width = 15, relief = RAISED, font = ("Helvetica", 18, "bold"), command = "ShowLoginForm", bg = "white", fg = "#873600")
view_window = canvas.create_window(200, 250, anchor = "nw", window = view_button)
view_button.bind('<Button-1>', ShowView)

product_button = Button(Home, text = "Add New Product", height = 3, width = 15, relief = RAISED, font = ("Helvetica", 18, "bold"), command = "ShowLoginForm", bg = "white", fg = "#873600")
product_window = canvas.create_window(700, 250, anchor = "nw", window = product_button)
product_button.bind('<Button-1>', ShowAddNew)
    
    
'''
Title = Frame(bg_frame, bd=1, relief=SOLID)
Title.pack(pady=10)
lbl_display = Label(Title, text="Construction Inventory System", font=('arial', 45))
lbl_display.pack() '''
menubar = Menu(Home)
filemenu = Menu(menubar, tearoff=0)
filemenu2 = Menu(menubar, tearoff=0)
filemenu.add_command(label="Logout", command=Logout)
filemenu.add_command(label="Exit", command=Exit2)
menubar.add_cascade(label="Account", menu=filemenu)
Home.config(menu=menubar)
#Home.config(bg="#6666ff")
Home.mainloop()




          
