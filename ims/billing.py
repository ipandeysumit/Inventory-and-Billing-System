from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile


class billClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Managment System")
        self.root.config(bg="White")
        self.cart_list = []
        self.chk_print = 0
# ==============================title========================
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Inventory Managment System", image=self.icon_title, compound=LEFT, font=(
            "times new roman", 40, "bold"), bg="#010c48", fg="white", anchor='w', padx=20).place(x=0, y=0, relwidth=1, height=70)

# =============================btn logout======================
        btn_logout = Button(self.root, text="Logout", command=self.logout, font=(
            "Times new roman", 15, "bold"), bg="yellow", cursor="hand2").place(x=1150, y=10, height=50, width=150)

# ===================== clock===================================
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Managment System\t\t Date: DD-MM-YY\t\t Time: HH:MM:SS",
                               font=("Times new      roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

# ========================= product frmae===========================

        ProductFrame = Frame(self.root, bd=4, relief=RIDGE)
        ProductFrame.place(x=6, y=110, width=410, height=550)

        ptitle = Label(ProductFrame, text="All Product", font=(
            "goudy old style", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)
# =============================product search frame=====================
        self.var_search = StringVar()
        ProductFrame2 = Frame(ProductFrame, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name", font=(
            "times new roman", 15, "bold"), bg="white", fg="green").place(x=2, y=5)

        lbl_search = Label(ProductFrame2, text="Product Name", font=(
            "times new roman", 15, "bold"), bg="white").place(x=5, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=(
            "times new roman", 15), bg="lightyellow").place(x=131, y=47, width=150,  height=22)
        btn_search = Button(ProductFrame2, text="Search", command=self.search, font=(
            "goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").        place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, command=self.show, text="Show All", font=(
            "goudy old style", 15), bg="#083531", fg="white",      cursor="hand2").place(x=285, y=10, width=100, height=25)

        Cart_Frame = Frame(ProductFrame, bd=3, relief=RIDGE)
        Cart_Frame.place(x=2, y=140, width=398, height=385)

        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(Cart_Frame, column=(
            "pid", "name", "price", "qty", "status"), yscrollcommand=scrolly.set,   xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid", text="PID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"] = "headings"
        self.product_Table.column("pid", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
        lbl_note = Label(ProductFrame, text="Note:'Enter 0 Quantity to remove product from the cart'", font=(
            "goudy old style", 10), bg="white",  fg="red").pack(side=BOTTOM, fill=X)

# =========================== customer frame=======================
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE)
        CustomerFrame.place(x=420, y=110, width=530, height=80)

        ctitle = Label(CustomerFrame, text="Customer Details", font=(
            "goudy old style", 20, "bold"), bg="lightgray").pack(side=TOP, fill=X)
        lbl_name = Label(CustomerFrame, text="Name", font=(
            "times new roman", 15)).place(x=5, y=41)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=(
            "times new roman", 13), bg="lightyellow").place(x=75, y=43, width=180)

        lbl_contact = Label(CustomerFrame, text="Contact", font=(
            "times new roman", 15)).place(x=272, y=41)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=(
            "times new roman", 13), bg="lightyellow").place(x=350, y=43,  width=150)
# =========================calculator cart frame====================
        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE)
        Cal_Cart_Frame.place(x=420, y=195, width=530, height=360)

# ==============================calculator frame==================
        self.var_cal_input = StringVar()

        Cal_Frame = Frame(Cal_Cart_Frame, bd=8, relief=RIDGE)
        Cal_Frame.place(x=5, y=10, width=268, height=340)

        txt_cal_input = Entry(Cal_Frame, textvariable=self.var_cal_input, font=(
            "arial", 15, "bold"), width=21, bd=10, relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(Cal_Frame, text='7', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            7), bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=0)
        btn_8 = Button(Cal_Frame, text='8', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            8), bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=1)
        btn_9 = Button(Cal_Frame, text='9', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            9), bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=2)
        btn_sum = Button(Cal_Frame, text='+', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            '+'), bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=3)

        btn_4 = Button(Cal_Frame, text='4', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            4), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=0)
        btn_5 = Button(Cal_Frame, text='5', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            5), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=1)
        btn_6 = Button(Cal_Frame, text='6', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            6), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=2)
        btn_sub = Button(Cal_Frame, text='-', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            '-'), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=3)

        btn_1 = Button(Cal_Frame, text='1', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            1), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=0)
        btn_2 = Button(Cal_Frame, text='2', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            2), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=1)
        btn_3 = Button(Cal_Frame, text='3', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            3), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=2)
        btn_mul = Button(Cal_Frame, text='*', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            '*'), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=3)

        btn_0 = Button(Cal_Frame, text='0', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            0), bd=5, width=4, pady=15, cursor="hand2").grid(row=4, column=0)
        btn_c = Button(Cal_Frame, text='c', font=('arial', 15, 'bold'), command=self.clear_cal,
                       bd=5, width=4, pady=15, cursor="hand2").grid(row=4,        column=1)
        btn_eq = Button(Cal_Frame, text='=', font=('arial', 15, 'bold'), command=self.perform_cal,
                        bd=5, width=4, pady=15, cursor="hand2").grid(row=4,     column=2)
        btn_div = Button(Cal_Frame, text='/', font=('arial', 15, 'bold'), command=lambda: self.get_input(
            '/'), bd=5, width=4, pady=15, cursor="hand2").grid(row=4, column=3)

# ==================================cart frame==============================
        Cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        Cart_Frame.place(x=280, y=8, width=245, height=342)

        self.carttitle = Label(Cart_Frame, text="Cart \t Total Product: [0]", font=(
            "goudy old style", 15,), bg="lightgray")
        self.carttitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(Cart_Frame, column=(
            "pid", "name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        self.CartTable["show"] = "headings"
        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=100)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

# ====================ADD cart widget frame=================================
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_stock = StringVar()

        Add_cartwidgetFrame = Frame(self.root, bd=2, relief=RIDGE)
        Add_cartwidgetFrame.place(x=420, y=550, width=530, height=110)

        p_name = Label(Add_cartwidgetFrame, text="Product Name",
                       font=("times new roman", 15)).place(x=5, y=5)
        txt_p_name = Entry(Add_cartwidgetFrame, textvariable=self.var_pname, font=(
            "times new roman", 15), bg="lightyellow", state='readonly').place(x=5, y=35, width=190, height=22)

        p_price = Label(Add_cartwidgetFrame, text="Price Per Qty",
                        font=("times new roman", 15)).place(x=230, y=5)
        txt_p_price = Entry(Add_cartwidgetFrame, textvariable=self.var_price, font=(
            "times new roman", 15), bg="lightyellow", state='readonly').place(x=230, y=35, width=150, height=22)

        lbl_p_qty = Label(Add_cartwidgetFrame, text="Quantity", font=(
            "times new roman", 15)).place(x=390, y=5)
        txt_p_qty = Entry(Add_cartwidgetFrame, textvariable=self.var_qty, font=(
            "times new roman", 15), bg="lightyellow").place(x=390, y=35, width=120, height=22)

        self.lbl_inStock = Label(
            Add_cartwidgetFrame, text="In Stock", font=("times new roman", 15))
        self.lbl_inStock.place(x=5, y=70)

        btn_clear_cart = Button(Add_cartwidgetFrame, text="Clear", command=self.clear_cart, font=(
            "times new roman", 15, "bold"), bg="lightgray", cursor="hand2").place(x=180,   y=70, width=150, height=30)
        btn_add_cart = Button(Add_cartwidgetFrame, text="ADD | Update Cart", command=self.add_update_cart, font=(
            "times new roman", 13, "bold"),       bg="orange", cursor="hand2").place(x=340, y=70, width=150, height=30)
# ===============================Billing area====================================

        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=953, y=110, width=400, height=410)

        btitle = Label(billFrame, text="Customer Bill Area", font=(
            "goudy old style", 20, "bold"), bg="#f44336", fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        billmenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billmenuFrame.place(x=953, y=520, width=400, height=140)

        self.lbl_amnt = Label(billmenuFrame, text='Bill Amount\n[0]', font=(
            "goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billmenuFrame, text='Discount\n[5%]', font=(
            "goudy old style", 15, "bold"), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billmenuFrame, text='Net Pay\n[0]', font=(
            "goudy old style", 15, "bold"), bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        lbl_print = Button(billmenuFrame, text='Print', command=self.print_bill, font=(
            "goudy old style", 15, "bold"), bd=2, bg="#3f51b5", fg="white", cursor="hand2")
        lbl_print.place(x=2, y=80, width=120, height=70)

        lbl_clear_all = Button(billmenuFrame, text='Clear All', command=self.clear_all, font=(
            "goudy old style", 15, "bold"), bd=2, bg="#8bc34a", fg="white", cursor="hand2")
        lbl_clear_all.place(x=124, y=80, width=120, height=70)

        lbl_generate = Button(billmenuFrame, text='Generate Bill', command=self.generate_bill, font=(
            "goudy old style", 15, "bold"), bd=5, bg="#607d8b", fg="white", cursor="hand2")
        lbl_generate.place(x=246, y=80, width=160, height=70)

        self.show()
    #     self.bill_top()

        self.update_date_time()
# =========================All function===================================

    def get_input(self, num):
        xnum = self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute(
                "select pid,name,price,qty,status from product where status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror(
                    "Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%" +
                            self.var_search.get()+"%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(
                        *self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No record found !", parent=self.root)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_Table.focus()
        content = (self.product_Table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock[{str(row [3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']
        # pid,name,price,qty,stock
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock[{str(row [4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror(
                'Error', "Please select product from list", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror(
                'Error', "Quantity is required", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)
        else:
            price_cal = self.var_price.get()
            # pid,name,price,qty,stock
            cart_data = [self.var_pid.get(), self.var_pname.get(
            ), price_cal, self.var_qty.get(), self.var_stock.get()]
    # ======================update cart========================
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1
            if present == 'yes':
                op = messagebox.askyesno(
                    'confirm', "Product already present\nDo you want to Update|Remove from the Cart List", parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3] = self.var_qty.get()  # qty
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            # pid,name,price,qty,status
            self.bill_amnt = self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount = (self.bill_amnt*5)/100
        self.net_pay = self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f"Bill Amt.(Rs.)\n[{str(self.bill_amnt)}]")
        self.lbl_net_pay.config(text=f'Net Pay(Rs.)\n[{str(self.net_pay)}]')
        self.carttitle.config(
            text=f"Cart\t Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror(
                "Error", f"Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror(
                "Error", f"Please Add the Product to the Cart")
        else:
            # ====Bill Top===
            self.bill_top()
            # ====Bill Middle==
            self.bill_middle()
            # ====Bill Bottom===
            self.bill_bottom()

            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo(
                'Saved', 'Bill has been generated and Saved', parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + \
            int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t\t\tXYZ-Inventory 
\tPhone No. 7398******,Prayagraj-211004
{str("="*46)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tData: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
 Product Name\t\t\tQTY\tPrice
{str("="*46)}   
                '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*46)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*46)}\n
                '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                # pid,name,price,qty,stock
                pid = row[0]
                name = row[1]
                qty = int(row[4])-int(row[3])
                if int(row[3]) == int(row[4]):
                    status = 'Inactive'
                if int(row[3]) != int(row[4]):
                    status = 'Active'

                price = float(row[2])*int(row[3])
                price = str(price)
                self.txt_bill_area.insert(
                    END, "\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
    # ======================updata quantity in product table============================
                cur.execute('Update Product set qty=?,status=? where pid=?', (
                    qty,
                    status,
                    pid

                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.carttitle.config(text=f"Cart\t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.lbl_amnt.config(text=f"Bill Amount")
        self.lbl_net_pay.config(text=f"Net Pay")
        self.chk_print = 0

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(
            text=f"Welcome to Inventory Managment System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo(
                'Print', 'Please wait while printing', parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showerror(
                'Print', 'Please generate bill, to print the receipt', parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = billClass(root)
    root.mainloop()
