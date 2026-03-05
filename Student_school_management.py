from tkinter import *
from tkinter import ttk
import csv
import os

# ---------------- LOGIN WINDOW ----------------

def login():
    if username.get() == "admin" and password.get() == "1234":
        login_window.destroy()
        open_main()
    else:
        status.config(text="Invalid Login", fg="red")

login_window = Tk()
login_window.title("Student Login")
login_window.geometry("300x200")
login_window.config(bg="#dfe6e9")

Label(login_window,text="Username",bg="#dfe6e9").pack(pady=5)
username = Entry(login_window)
username.pack()

Label(login_window,text="Password",bg="#dfe6e9").pack(pady=5)
password = Entry(login_window,show="*")
password.pack()

Button(login_window,text="Login",command=login,bg="#0984e3",fg="white").pack(pady=10)

status = Label(login_window,text="",bg="#dfe6e9")
status.pack()

# ---------------- MAIN WINDOW ----------------

def open_main():

    root = Tk()
    root.title("Student Management System")
    root.geometry("1050x520")
    root.config(bg="#f1f2f6")

# -------- Entry Fields --------

    Label(root,text="Name",bg="#f1f2f6").grid(row=0,column=0,pady=5)
    name_entry=Entry(root)
    name_entry.grid(row=0,column=1)

    Label(root,text="Telugu",bg="#f1f2f6").grid(row=1,column=0)
    telugu_entry=Entry(root)
    telugu_entry.grid(row=1,column=1)

    Label(root,text="Hindi",bg="#f1f2f6").grid(row=2,column=0)
    hindi_entry=Entry(root)
    hindi_entry.grid(row=2,column=1)

    Label(root,text="English",bg="#f1f2f6").grid(row=3,column=0)
    english_entry=Entry(root)
    english_entry.grid(row=3,column=1)

    Label(root,text="Maths",bg="#f1f2f6").grid(row=4,column=0)
    maths_entry=Entry(root)
    maths_entry.grid(row=4,column=1)

    Label(root,text="Science",bg="#f1f2f6").grid(row=5,column=0)
    science_entry=Entry(root)
    science_entry.grid(row=5,column=1)

    Label(root,text="Social",bg="#f1f2f6").grid(row=6,column=0)
    social_entry=Entry(root)
    social_entry.grid(row=6,column=1)

# -------- Table --------

    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
        background="#dfe6e9",
        foreground="black",
        rowheight=25,
        fieldbackground="#dfe6e9")

    style.map('Treeview',background=[('selected','#74b9ff')])

    table=ttk.Treeview(root)

    table['columns']=("Name","Telugu","Hindi","English","Maths","Science","Social","Total","Percent","Grade")

    table.column("#0",width=0,stretch=NO)

    for col in table['columns']:
        table.column(col,width=90)
        table.heading(col,text=col)

    table.grid(row=0,column=3,rowspan=12,padx=20)

# -------- Functions --------

    def calculate_grade(percent):

        if percent>=90:
            return "A+"
        elif percent>=75:
            return "A"
        elif percent>=60:
            return "B"
        elif percent>=50:
            return "C"
        else:
            return "Fail"

    def clear_fields():

        name_entry.delete(0,END)
        telugu_entry.delete(0,END)
        hindi_entry.delete(0,END)
        english_entry.delete(0,END)
        maths_entry.delete(0,END)
        science_entry.delete(0,END)
        social_entry.delete(0,END)

    def add_student():

        name=name_entry.get()

        telugu=int(telugu_entry.get())
        hindi=int(hindi_entry.get())
        english=int(english_entry.get())
        maths=int(maths_entry.get())
        science=int(science_entry.get())
        social=int(social_entry.get())

        total=telugu+hindi+english+maths+science+social
        percent=round(total/6,2)

        grade=calculate_grade(percent)

        data=[name,telugu,hindi,english,maths,science,social,total,percent,grade]

        table.insert('',END,values=data)

        save_data(data)

        clear_fields()

    def save_data(data):

        file_exists=os.path.isfile("students.csv")

        with open("students.csv","a",newline='') as f:
            writer=csv.writer(f)

            if not file_exists:
                writer.writerow(["Name","Telugu","Hindi","English","Maths","Science","Social","Total","Percent","Grade"])

            writer.writerow(data)

    def load_data():

        if os.path.exists("students.csv"):

            with open("students.csv","r") as f:
                reader=csv.reader(f)
                next(reader)

                for row in reader:
                    table.insert('',END,values=row)

    def delete_student():

        selected=table.selection()

        if not selected:
            return

        values=table.item(selected,'values')
        name=values[0]

        table.delete(selected)

        rows=[]

        with open("students.csv","r") as f:
            reader=csv.reader(f)
            rows=list(reader)

        with open("students.csv","w",newline='') as f:
            writer=csv.writer(f)

            for row in rows:
                if row and row[0]!=name:
                    writer.writerow(row)

    def select_record(event):

        selected=table.focus()
        values=table.item(selected,'values')

        if values:

            clear_fields()

            name_entry.insert(0,values[0])
            telugu_entry.insert(0,values[1])
            hindi_entry.insert(0,values[2])
            english_entry.insert(0,values[3])
            maths_entry.insert(0,values[4])
            science_entry.insert(0,values[5])
            social_entry.insert(0,values[6])

    def update_student():

        selected=table.focus()

        name=name_entry.get()

        telugu=int(telugu_entry.get())
        hindi=int(hindi_entry.get())
        english=int(english_entry.get())
        maths=int(maths_entry.get())
        science=int(science_entry.get())
        social=int(social_entry.get())

        total=telugu+hindi+english+maths+science+social
        percent=round(total/6,2)

        grade=calculate_grade(percent)

        new_data=[name,telugu,hindi,english,maths,science,social,total,percent,grade]

        table.item(selected,values=new_data)

        rows=[]

        with open("students.csv","r") as f:
            reader=csv.reader(f)
            rows=list(reader)

        rows.append(new_data)

        with open("students.csv","w",newline='') as f:
            writer=csv.writer(f)
            writer.writerows(rows)

        clear_fields()

    def search_student():

        name=search_entry.get()

        for item in table.get_children():
            table.delete(item)

        if os.path.exists("students.csv"):

            with open("students.csv","r") as f:

                reader=csv.reader(f)
                next(reader)

                for row in reader:

                    if name.lower() in row[0].lower():
                        table.insert('',END,values=row)

# -------- Buttons --------

    Button(root,text="Add Student",command=add_student,bg="#00b894",fg="white").grid(row=7,column=0,pady=10)

    Button(root,text="Update",command=update_student,bg="#fdcb6e").grid(row=7,column=1)

    Button(root,text="Delete",command=delete_student,bg="#d63031",fg="white").grid(row=7,column=2)

# -------- Search --------

    Label(root,text="Search Name",bg="#f1f2f6").grid(row=9,column=0)

    search_entry=Entry(root)
    search_entry.grid(row=9,column=1)

    Button(root,text="Search",command=search_student,bg="#6c5ce7",fg="white").grid(row=9,column=2)

    table.bind("<ButtonRelease-1>",select_record)

    load_data()

    root.mainloop()

login_window.mainloop()
