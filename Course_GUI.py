import tkinter as tk
import ttkbootstrap as ttk
import mysql.connector
from DATABASE_CONFIG import dbhost, dbuser, dbpasswd, dbname

class EnrollmentDB():
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host= dbhost,
            user= dbuser,
            passwd= dbpasswd,
            database= dbname
        )
        
        self.cursor = self.db.cursor()
    
    def add(self,subjectcode,subjectname,units):
        self.cursor.execute("INSERT INTO subject VALUES (%s,%s,%s)",(subjectcode,subjectname,units))
        self.db.commit() 
    
    def view_all(self):
        self.cursor.execute("SELECT * FROM subject")
        results = self.cursor.fetchall()
        return results
    
    def view_one(self,subjectcode):
        self.cursor.execute("SELECT * FROM subject WHERE subjcode = %s",(subjectcode,))
        result = self.cursor.fetchone()
        return result

class Course_Create(EnrollmentDB):
    def __init__(self) -> None:
        super().__init__()
        # Window
        self.window = ttk.Window(themename='flatly', title="Course Subject")
        self.window.geometry("500x300")
        self.window.iconbitmap("MSEUF_LOGO_HD.ico")
        self.window.resizable(False, False)

        # Notebook
        self.notebook = ttk.Notebook(master=self.window)
        self.notebook.pack()

        # Add Tab
        self.add_tab = ttk.Frame(master=self.notebook, width=500)
        self.notebook.add(self.add_tab, text="Create Course Subject")

        # Title Label
        self.title = ttk.Label(
            master=self.add_tab,
            text="Create a Course Subject",
            font="Calibri 36 bold")
        self.title.pack(padx=10)

        # Subject Code
        self.SubjCode_Var = tk.StringVar()
        self.SubjCode_Frame = ttk.Frame(master=self.add_tab)
        self.code_label = ttk.Label(
            master=self.SubjCode_Frame,
            text="Subject Code:",
            font="Calibri 18"
        )
        self.code_entry = ttk.Entry(
            master= self.SubjCode_Frame,
            textvariable= self.SubjCode_Var,
            width=40
        )
        self.code_label.pack(side="left",padx=10)
        self.code_entry.pack(side="right")
        self.SubjCode_Frame.pack(pady=3)

        # Subject Name
        self.SubjName_Var = tk.StringVar()
        self.SubjName_Frame = ttk.Frame(master=self.add_tab)
        self.name_label = ttk.Label(
            master=self.SubjName_Frame,
            text="Subject Name:",
            font="Calibri 18"
        )
        self.name_entry = ttk.Entry(
            master= self.SubjName_Frame,
            textvariable= self.SubjName_Var,
            width=40
        )
        self.name_label.pack(side="left",padx=6)
        self.name_entry.pack(side="right")
        self.SubjName_Frame.pack(pady=3)

        # Units
        self.SubjUnits_Var = tk.StringVar()
        self.SubjUnits_Frame = ttk.Frame(master=self.add_tab)
        self.name_label = ttk.Label(
            master=self.SubjUnits_Frame,
            text="Subject Units:",
            font="Calibri 18"
        )
        self.name_entry = ttk.Entry(
            master= self.SubjUnits_Frame,
            textvariable= self.SubjUnits_Var,
            width=40
        )
        self.name_label.pack(side="left",padx=10)
        self.name_entry.pack(side="right")
        self.SubjUnits_Frame.pack(pady=3)

        # Submit Button
        self.Submit = ttk.Button(
            master=self.add_tab,
            text="Create Course Subject",
            command= self.Submit_Button
        )
        self.Submit.pack(pady=10)

        # Result Label
        self.result = ttk.Label(
            master=self.add_tab,
            text="",
            font="Calibri 18"
        )
        self.result.pack()

        # View Tab
        self.view_tab = ttk.Frame(master=self.notebook, width=500)
        self.notebook.add(self.view_tab, text="View Course Subject")

        # View Title Label
        self.view_title = ttk.Label(
            master=self.view_tab,
            text="View Course Subject",
            font="Calibri 36 bold"
        )
        self.view_title.pack(padx=10)

        # Listbox
        self.listbox = tk.Listbox(master=self.view_tab, width=10, height=10, font="Calibri 18")
        self.listbox.pack(side="left", pady=10, padx=5)

        # Bind the listbox to the select function
        self.listbox.bind("<<ListboxSelect>>", self.list_select)

        # Scrollbar
        scrollbar = ttk.Scrollbar(master=self.view_tab, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="left", pady=10,fill="y")

        # Connect scrollbar to listbox
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Add the values to the listbox
        for row in self.view_all():
            self.listbox.insert("end", row[0])
        
        # Details label
        self.details_label = ttk.Label(
            master=self.view_tab,
            text="Details:",
            font="Calibri 18 bold"
        )
        self.details_label.pack(pady=10)

        # Course Name Label that will be updated
        self.course_name = ttk.Label(
            master=self.view_tab,
            text="",
            font="Calibri 18 bold"
        )
        self.course_name.pack(pady=10)

        # Units Label that will be updated
        self.units = ttk.Label(
            master=self.view_tab,
            text="",
            font="Calibri 18"
        )
        self.units.pack(pady=10)
        

        # Run Loop
        self.window.mainloop()
    
    def Submit_Button(self):
        # Get the values from the entry fields
        SubjCode = self.SubjCode_Var.get()
        SubjName = self.SubjName_Var.get()
        SubjUnits = self.SubjUnits_Var.get()

        # Add the values to the database
        self.add(SubjCode,SubjName,SubjUnits)

        # Display the result
        self.result.config(text="Course Subject Created")

        # Update the listbox with the new item
        self.listbox.insert("end", SubjName)

        # Clear the entry fields
        self.SubjCode_Var.set("")
        self.SubjName_Var.set("")
        self.SubjUnits_Var.set("")
    
    def list_select(self, event):
        # Get the selected item
        subjcode = self.listbox.get(self.listbox.curselection())

        # Get the details of the selected item
        subj_details = self.view_one(subjcode)

        # Update the labels
        self.course_name.config(text=f"{subj_details[1]}")
        self.units.config(text=f"Units: {subj_details[2]}")





if __name__ == "__main__":
    window = Course_Create()