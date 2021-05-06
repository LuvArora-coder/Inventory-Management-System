import tkinter as tk
import MySQLdb
import pyscreenshot as ImageGrab
import time
import os
import sys
import csv
from tkinter import scrolledtext
from tkinter.font import Font
from tkinter import *  
from tkinter import messagebox
from  models.Store import Store
from  models.ShoppingCart import ShoppingCart


conn = MySQLdb.connect(host = "localhost", user = "root", password = "root",database="PyProject")
cursor = conn.cursor()
global cart
cart = {"name" : [], "price" : []}

def viewStore():
    global storeWindow
    storeLabelFrame = LabelFrame(storeWindow, text="Store Items")
    storeLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    storeItemsFrame = Frame(storeLabelFrame)
    storeItemsFrame.pack(padx="10", pady="5")
    # store = Store()
    # storeItems = store.getStoreItems()

    cursor.execute("SELECT product_name,product_price FROM product")
    storeItems = cursor.fetchall()

    for item in storeItems:
        itemFrame = Frame(storeItemsFrame,  pady="5")
        itemFrame.pack(fill="both", expand="yes")

        nameLabel = Label(itemFrame, text=item[0] ,font=("Candara",15),fg="blue")
        priceLabel = Label(itemFrame, text="Rs. %s"%item[1] , font=("Candara",13),fg="red")
        addToCartBtn = Button(itemFrame, text="Add To Cart",cursor="hand2", command=lambda i=item: addItemToCart(i) )
        btnImage=PhotoImage(file="images/addToCart.png")
        addToCartBtn.image= btnImage
        addToCartBtn.config(image=btnImage,width="40",height="40")

        nameLabel.pack(side="left")
        priceLabel.pack(side="left",fill="both", expand="yes" )
        addToCartBtn.pack(side="right" )

    btnGoCart = Button(storeWindow, text="Go To Cart", font=("Candara",15,"bold"),fg="red",bg="white",cursor="hand2", command=viewCart )
    btnGoCart.pack(pady="6")

def viewCart():   
    cartWindow = Toplevel()
    cartWindow.title("The Cart")
    cartWindow.grab_set()
    global cart
    # cartItems = cart.getCartItems()

    cartItemsLabelFrame = LabelFrame(cartWindow,text="Cart Items")
    cartItemsLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    cartItemsFrame = Frame(cartItemsLabelFrame, padx=3, pady=3)
    cartItemsFrame.pack()
    index = 0
    totalprice=0

    for i in range(len(cart["name"])):
        itemFrame = Frame(cartItemsFrame,  pady="5")
        itemFrame.pack(fill="both", expand="yes")

        nameLabel = Label(itemFrame, text=cart["name"][i],font=("Candara",15),fg="blue")
        priceLabel = Label(itemFrame, text="Rs. %s"%cart["price"][i],font=("Candara",13),fg="red")
        addToCartBtn = Button(itemFrame, text="Remove From Cart", font=("Candara",11,"bold"),fg="red",bg="white",cursor="hand2", command=lambda i=index: removeFromCart(i,cartWindow) )
        a=int(cart["price"][i])
        totalprice=totalprice+a
        nameLabel.pack(side="left")
        priceLabel.pack(side="left")
        addToCartBtn.pack(side="right" )
        index += 1

    checkOutFrame = Frame(cartWindow, pady="10")
    totalPriceLabel = Label(checkOutFrame, text="Total Price : Rs. %s" % totalprice, font=("Candara",14,"bold"),fg="indigo")
    totalPriceLabel.pack(side="left")
    buyBtn = Button(checkOutFrame, text="Buy Now", font=("Candara",15,"bold"),fg="indigo",bg="white",cursor="hand2", command=lambda : buyCommand(cartWindow))
    buyBtn.pack(side="left",padx="10")
    checkOutFrame.pack()

    backToStoreBtn = Button(cartWindow, text="Back To Store", font=("Candara",15,"bold"),fg="red",bg="white",cursor="hand2",command=cartWindow.destroy)
    backToStoreBtn.pack(pady="6")

    cartWindow.mainloop()



def addItemToCart(item=None):
    cart["name"].append(item[0])
    cart["price"].append(item[1])
    messagebox.showinfo(title="Success" , message="Item %s Added To The Cart !!"%item[0])

def removeFromCart(itemIndex=None,cartWindow=None):

    cart["name"].pop(itemIndex)
    cart["price"].pop(itemIndex)
    messagebox.showinfo(title="success",message="Item Removed")
    cartWindow.destroy()
    viewCart()
def buyCommand(cartWindow):
    cartWindow.destroy()    
    messagebox.showinfo(title="success",message="Purchase Completed Successfully")

    global viewform
    viewform = Toplevel()
    viewform.title("Construction Inventory System/View Product")
    width = 700
    height = 520
    screen_width = 520
    screen_height = 520
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)

    bill_frame = Frame(viewform, width=x, height=y)
    bill_frame.place(x=0, y=0)

    # Bill Title
    bill_label = Label(bill_frame, text="BILL", font="Consolas 30 bold", border=7, relief="groove", anchor='c',
                       background='#282c34', foreground='#fff')
    bill_label.grid(row=0, ipadx=317)

    # Bill Contents/Text Area
    bill_text = scrolledtext.ScrolledText(bill_frame, font="Consolas 10", width=101, height=29)
    bill_text.grid(row=1, sticky='W')

    # Define attributes for Bill entry
    heading = "Retail Invoice"
    cust_name = f"Customer Name    : {width}"
    cust_phno = f"Customer Id  : {1}"
    # Defining date and time variables
    date_string = "Date : " + time.strftime("%d/%b/%Y")
    time_string = "Time : " + time.strftime("%I:%M:%S %p")
    # print(date_string,time_string)

    # First Deleting Entire bill Contents/Texts
    bill_text.delete('1.0', 'end')
    # Inserting to Clean bill/Texts
    bill_text.insert('end', "\n" + heading + "\n")
    bill_text.insert('end', "\n" + cust_name)
    bill_text.insert('end', "\t\t\t\t\t\t\t\t\t" + date_string + "\n")
    bill_text.insert('end', "\n" + cust_phno)
    bill_text.insert('end', "\t\t\t\t\t\t\t\t\t" + time_string + "\n\n")

    bill_text.insert('end', "-" * 100 + "\n")
    bill_text.insert('end', "No   Product Name\t\t\t\t\t\t        Rate(\u20B9)\t\t    \n")
    bill_text.insert('end', "-" * 100 + "\n")

    # Total Price set to 0 before calculating
    sum = 0.0
    # Inserting items to Bill and Calculating sum of all contents
    totalprice=0
    for i in range(len(cart["name"])):

        bill_text.insert('end', f"\n  {i + 1}  {cart['name'][i]}\t\t\t\t\t\t\t{cart['price'][i]}\t")
        a = int(cart["price"][i])
        totalprice = totalprice + a
        # print(items[i])
    # Inserting sum amount at the end
    bill_text.insert('end', "\n\n\n\n" + "-" * 100 + "\n")
    # print(sum)
    total_amt = f"\u20B9 {sum}"
    bill_text.insert('end', f"TOTAL =  {totalprice}")
    bill_text.insert('end', "\n" + "-" * 100 + "\n")

    # Tags and styling
    bill_text.tag_add('heading', '2.0', '2.end')
    bill_text.tag_config('heading', font='Arial 20 bold', justify='center')
    bill_text.tag_add('customer', '4.0', '6.end')
    bill_text.tag_config('customer', font='Consolas 11', lmargin1=20)
    bill_text.tag_add('sub-head', '9.0', '9.end')
    bill_text.tag_config('sub-head', font='Consolas 12 bold', lmargin1=10)

    total_line = str(i + 17)  # Calculating total lines to style Total Amount
    # print(total_line)
    bill_text.tag_add('total', f'{total_line}.0', f'{total_line}.end')
    bill_text.tag_config('total', font='Aerial 15 bold', justify='center')

    # Disabling modification of bill
    bill_text.config(state='disabled')

    # Creating Backup/Record in local disk
    # write_to_disk(bill_win)

storeWindow = tk.Tk()
storeWindow.title("The Store")
viewStore()

#cart = ShoppingCart()

storeWindow.mainloop()
