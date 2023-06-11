from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
import sqlite3
from tkinter import ttk,messagebox

class supplierClass:
        def __init__(self,root):
                self.root=root
                self.root.geometry("1100x500+200+130")
                self.root.title("Inventory Managment System")
                self.root.config(bg="White")
                self.root.focus_force()
                # ------------------------------
                # All variable----
                self.var_searchby=StringVar()
                self.var_searchtxt=StringVar()

                # self.var_supid=StringVar()
                self.var_sup_invoice=StringVar()
                self.var_name=StringVar()
                self.var_contact=StringVar()        
                

        # search---------------------

        # option---------------
                lbl_search= Label(self.root,text="Supplier ID",font=("goudy old style",15),bg="white")
                lbl_search.place(x=690,y=58)
                
                txt_search=Entry(self.root,textvariabl=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=790,y=58,width=165)
                btn_search=Button(self.root,text="search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=960,y=58,width=110,height=26)

        # Title-------------

                title=Label(self.root,text="Supplier Details",bg="blue",fg="white",font=("goudy old style",20,"bold")).place(x=50,y=10,height=40,width=1000)

        # content--------------
        # row 1----------------------
                lbl_supplier_invoice=Label(self.root,text="Supplier ID",font=("goudy old style",13),bg="white").place(x=50,y=80)
                txt_supplier_invoice= Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",13),bg="lightyellow").place(x=180,y=80,width=180)
                
        #  Row 2---------------

                lbl_name=Label(self.root,text="Name",font=("goudy old style",13),bg="white").place(x=50,y=120)
                txt_name= Entry(self.root,textvariable=self.var_name,font=("goudy old style",13),bg="lightyellow").place(x=180,y=120,width=180)        
        # Row 3 ---------------------
                lbl_contact=Label(self.root,text="Contact",font=("goudy old style",13),bg="white").place(x=50,y=160)
                txt_contact= Entry(self.root,textvariable=self.var_contact,font=("goudy old style",13),bg="lightyellow").place(x=180,y=160,width=180)        
        # Row 4--------------------- 

                lbl_desc = Label(self.root,text="Address",font=("goudy old style",13),bg="white").place(x=50,y=200)
                self.txt_desc = Text(self.root,font=("goudy old style",13),bg="lightyellow")
                self.txt_desc.place(x=180,y=200,width=500,height=90)
                
        # button for the delete save update clear---------------

                btn_save = Button(self.root,text="Save",command=self.add,font=("goudy old style",13),bg="#4caf50",fg="white",cursor="hand2").place(x=180,y=400,width=110,height=35)
                btn_update = Button(self.root,text="Update",command=self.update,font=("goudy old style",13),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=400,width=110,height=35)
                btn_delete = Button(self.root,text="Delete",command=self.delete,font=("goudy old style",13),bg="#4caf50",fg="white",cursor="hand2").place(x=420,y=400,width=110,height=35)
                btn_clear = Button(self.root,text="Clear",command=self.clear,font=("goudy old style",13),bg="#4caf50",fg="white",cursor="hand2").place(x=540,y=400,width=110,height=35)

                # supplier details--------3

                emp_frame= Frame(self.root,bd=3,relief=RIDGE)
                emp_frame.place(x=690,y=100,width=380,height=350)

                scrolly=Scrollbar(emp_frame,orient=VERTICAL)
                scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

                self.supplierTable = ttk.Treeview(emp_frame,column=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
                scrollx.pack(side=BOTTOM,fill=X)
                scrolly.pack(side=RIGHT,fill=Y)
                scrollx.config(command=self.supplierTable.xview)
                scrolly.config(command=self.supplierTable.yview)


                # self.supplierTable.heading("supid",text="Sup ID")
                self.supplierTable.heading("invoice",text="Sup ID")
                self.supplierTable.heading("name",text="Name")
                self.supplierTable.heading("contact",text="Email")
                self.supplierTable.heading("desc",text="Description")

                self.supplierTable["show"]="headings"

                # self.supplierTable.column("supid",width=90)
                self.supplierTable.column("invoice",width=90)
                self.supplierTable.column("name",width=100)
                self.supplierTable.column("contact",width=100)
                self.supplierTable.column("desc",width=100)
                self.supplierTable.pack(fill=BOTH,expand=1)
                self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

                self.show()
# ========================================================================

        def add(self):
                con=sqlite3.connect(database=r'ims.db')
                cur=con.cursor()
                try:
                        if self.var_sup_invoice.get()=="" :
                                messagebox.showerror("Error","Invoice must be required",parent=self.root)
                        else:
                                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                                row=cur.fetchone()
                                if row!=None:
                                        messagebox.showerror("Error","Invoice no. already assinged, try different",parent=self.root)
                                else:
                                        cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                                                       
                                                                self.var_sup_invoice.get(),
                                                                self.var_name.get(),
                                                                self.var_contact.get(),        
                                                                self.txt_desc.get('1.0',END),
                                                                
                                                        
                                        ))
                                        con.commit()
                                        messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)
                                        self.show()
                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

        def show(self):
                con=sqlite3.connect(database=r'ims.db')
                cur=con.cursor()
                try:
                        cur.execute("select * from supplier")
                        rows=cur.fetchall()
                        self.supplierTable.delete(*self.supplierTable.get_children())
                        for row in rows:
                                self.supplierTable.insert('',END,values=row)
                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

        def get_data(self,ev):
                f=self.supplierTable.focus()
                content=(self.supplierTable.item(f))
                row=content['values']
                # print(row)
                self.var_sup_invoice.set(row[0])
                self.var_name.set(row[1])
                self.var_contact.set(row[2])        
                self.txt_desc.delete('1.0',END)
                self.txt_desc.insert(END,row[3])
                
        def update(self):
                con=sqlite3.connect(database=r'ims.db')
                cur=con.cursor()
                try:
                        if self.var_sup_invoice.get()=="":
                                messagebox.showerror("Error","Invoice no. must be required",parent=self.root)
                        else:
                                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                                row=cur.fetchone()
                                if row==None:
                                        messagebox.showerror("Error","Invalid Invoice no,",parent=self.root)
                                else:
                                        cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                                                       
                                                                
                                                                self.var_name.get(),
                                                                self.var_contact.get(),
                                                                self.txt_desc.get('1.0',END),
                                                                self.var_sup_invoice.get(),
                                                        
                                        ))
                                        con.commit()
                                        messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
                                        self.show()
                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
       

        def delete(self):
                con=sqlite3.connect(database=r'ims.db')
                cur=con.cursor()
                try:
                        if self.var_sup_invoice.get()=="" :
                                messagebox.showerror("Error","Invoice no must be required",parent=self.root)
                        else:
                                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                                row=cur.fetchone()
                                if row==None:
                                        messagebox.showerror("Error","Invalid Invoice no",parent=self.root)
                                else:
                                        op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                                        if op==True:

                                                cur.execute("delete from Supplier where invoice=?",(self.var_sup_invoice.get(),))
                                                con.commit()
                                                messagebox.showinfo("Delete","Supplier Deleted successfully",parent=self.root)
                                                self.show()

                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        
        def clear(self):
                self.var_sup_invoice.set("")
                self.var_name.set("")
                self.var_contact.set("")
                self.txt_desc.delete('1.0',END)
                self.var_searchtxt.set("")
                self.show()
        
        def search(self):
                con=sqlite3.connect(database=r'ims.db')
                cur=con.cursor()
                try:
                        if self.var_searchtxt.get()=="":
                                messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
                        else:
                                cur.execute("select * from Supplier where invoice=?",(self.var_searchtxt.get(),))
                                row=cur.fetchone()
                                if row!=None:
                                        self.supplierTable.delete(*self.supplierTable.get_children())
                                        self.supplierTable.insert('',END,values=row)
                                else:
                                        messagebox.showerror("Error","No record found !",parent=self.root)
                              
                except Exception as ex:
                        messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()