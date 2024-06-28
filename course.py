from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3
class CourseClass:
    def __init__(self, root):
       self.root=root
       self.root.title("student result management system")
       self.root.geometry("1200x480+80+170")
       self.root.config(bg="white")
       self.root.focus_force()
       title = Label(self.root, text="Manage Course Details:", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15,width=1180,height=35 )
       #===variables===
       self.var_course=StringVar()
       self.var_duration=StringVar()
       self.var_charges=StringVar()
       #===widgets==
       lbl_courseName=Label(self.root,text="course name",font=("goudy old style",15, "bold"),bg="white").place(x=10,y=60)
       lbl_duration=Label(self.root,text="duration",font=("goudy old style",15, "bold"),bg="white").place(x=10,y=100)
       lbl_charges=Label(self.root,text="charges",font=("goudy old style",15, "bold"),bg="white").place(x=10,y=140)
       lbl_description=Label(self.root,text="description",font=("goudy old style",15, "bold"),bg="white").place(x=10,y=180)
       #===entry fields===
       self.txt_courseName=Entry(self.root,textvariable=self.var_course,font=("goudy old style",15, "bold"),bg="lightyellow")
       self.txt_courseName.place(x=150,y=60,width=200)
       txt_duration=Entry(self.root,textvariable=self.var_duration,font=("goudy old style",15, "bold"),bg="lightyellow").place(x=150,y=100,width=200)
       txt_charges=Entry(self.root,textvariable=self.var_charges,font=("goudy old style",15, "bold"),bg="lightyellow").place(x=150,y=140,width=200)
       self.txt_description=Text(self.root,font=("goudy old style",15, "bold"),bg="lightyellow")
       self.txt_description.place(x=150,y=180,width=500,height=140)
       #===button====
       self.btn_add=Button(self.root,text="SAVE",font=("goudy old style",15, "bold"),bd=5,relief=RIDGE,bg="#2196f3",fg="white",cursor="hand2",command=self.add)
       self.btn_add.place(x=150,y=400,width=110,height=40)
       self.btn_update=Button(self.root,text="UPDATE",font=("goudy old style",15, "bold"),relief=RIDGE,bd=5,bg="#607d8b",fg="white",cursor="hand2",command=self.update)
       self.btn_update.place(x=270,y=400,width=110,height=40)
       self.btn_delete=Button(self.root,text="DELETE",font=("goudy old style",15, "bold"),relief=RIDGE,bd=5,bg="#f44336",fg="white",cursor="hand2",command=self.delete)
       self.btn_delete.place(x=390,y=400,width=110,height=40)
       self.btn_clear=Button(self.root,text="CLEAR",font=("goudy old style",15, "bold"),relief=RIDGE,bd=5,bg="#4caf50",fg="white",cursor="hand2",command=self.clear)
       self.btn_clear.place(x=510,y=400,width=110,height=40)
        #===search pannel===
       self.var_search=StringVar()
       lbl_search_courseName=Label(self.root,text="course name:",font=("goudy old style",15, "bold"),bg="white").place(x=720,y=60)
       txt_search_courseName=Entry(self.root,textvariable=self.var_search,font=("goudy old style",15, "bold"),bg="lightyellow").place(x=870,y=60,width=180)
       btn_search=Button(self.root,text="SEARCH",font=("goudy old style",15, "bold"),bd=5,bg="#2196f3",fg="white",cursor="hand2",command=self.search).place(x=1070,y=60,width=120,height=28)
        #===content_course===
       self.c_Frame=Frame(self.root,bd=2,relief=RIDGE)
       self.c_Frame.place(x=720,y=100,width=470,height=340)
       scrolly=Scrollbar(self.c_Frame,orient=VERTICAL)
       scrollx=Scrollbar(self.c_Frame,orient=HORIZONTAL)
       self.coursetable=ttk.Treeview(self.c_Frame,columns=("cid","name","duration","charges","description"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
       scrollx.pack(side=BOTTOM,fill=X)
       scrolly.pack(side=RIGHT,fill=Y)
       scrollx.config(command=self.coursetable.xview)
       scrolly.config(command=self.coursetable.yview)
       self.coursetable.heading("cid",text="course ID")
       self.coursetable.heading("name",text="name")
       self.coursetable.heading("duration",text="duration")
       self.coursetable.heading("charges",text="fees")
       self.coursetable.heading("description",text="description")
       self.coursetable.column("cid",width=100)
       self.coursetable.column("name",width=100)
       self.coursetable.column("duration",width=100)
       self.coursetable.column("charges",width=100)
       self.coursetable.column("description",width=150)
       self.coursetable["show"]="headings"
       self.coursetable.pack(fill=BOTH,expand=1)
       self.coursetable.bind("<ButtonRelease-1>",self.get_data)
       self.show()
      #=======================functions========================

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0",END)
        self.txt_courseName.config(state=NORMAL)  

    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
           if self.var_course.get()=="":
              messagebox.showerror("error","course name cannot be empty",parent=self.root)
           else:
               cur.execute("SELECT * FROM course WHERE name=?",(self.var_course.get(),))
               row=cur.fetchone()
               if row==None:
                   messagebox.showerror("error","select course from list",parent=self.root)
               else:
                   op=messagebox.askyesno("confirm","do you want to delete?",parent=self.root)
                   if op==True:
                       cur.execute("delete from course where name=?",(self.var_course.get(),))
                       con.commit()
                       messagebox.showinfo("Delete","course deleted successfully",parent=self.root)
                       self.clear()
        except Exception as ex:
           messagebox.showerror("error",f"error due to{str(ex)}")  

    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
           if self.var_course.get()=="":
              messagebox.showerror("error","course name cannot be empty",parent=self.root)
           else:
               cur.execute("SELECT * FROM course WHERE name=?",(self.var_course.get(),))
               row=cur.fetchone()
               if row==None:
                   messagebox.showerror("error","select from list",parent=self.root)
               else:
                  cur.execute("update course set duration=?,charges=?,description=? where name=?",(
                     self.var_duration.get(),
                     self.var_charges.get(),
                     self.txt_description.get("1.0",END),
                     self.var_course.get()
                  ))
                  con.commit()
                  messagebox.showinfo("success","course updated successfully",parent=self.root)
                  self.show()
        except Exception as ex:
           messagebox.showerror("error",f"error due to{str(ex)}")  

    def get_data(self,ev):
        self.txt_courseName.config(state='readonly')
        r=self.coursetable.focus()
        content=self.coursetable.item(r)
        row=content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
      #  self.var_.set(row[4])
        self.txt_description.delete("1.0",END)
        self.txt_description.insert(END,row[4])  


    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
           if self.var_course.get()=="":
              messagebox.showerror("error","course name cannot be empty",parent=self.root)
           else:
               cur.execute("SELECT * FROM course WHERE name=?",(self.var_course.get(),))
               row=cur.fetchone()
               if row!=None:
                   messagebox.showerror("error","course name already present",parent=self.root)
               else:
                   cur.execute("insert into course(name,duration,charges,description)values(?,?,?,?)",(
                     self.var_course.get(),
                     self.var_duration.get(),
                     self.var_charges.get(),
                     self.txt_description.get("1.0",END) 
                   ))
                   con.commit()
                   messagebox.showinfo("Success","Course added successfully",parent=self.root)
                   self.show()
        except Exception as ex:
           messagebox.showerror("error",f"error due to{str(ex)}")    


    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM course")
            rows=cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
               self.coursetable.insert('',END,values=row)
        except Exception as ex:
           messagebox.showerror("error",f"error due to {str(ex)}")

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute(f"SELECT * FROM course WHERE name LIKE '%{self.var_search.get()}%'")
            rows=cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
               self.coursetable.insert('',END,values=row)
        except Exception as ex:
           messagebox.showerror("error",f"error due to{str(ex)}")



if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
