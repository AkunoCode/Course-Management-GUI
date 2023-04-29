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
    
    def add_to_DB(self,subjectcode,subjectname,units):
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

class App(tk.Tk):
    def __init__(self, title, size, icon):
        
        # Main Setup
        super().__init__()
        self.enrollmentdb = EnrollmentDB()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.iconbitmap(icon)

        # Widgets
        self.notebook = Notebook(master=self)

        # Run
        self.mainloop()

class Notebook(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack(expand=True, fill="both")

        self.add(TabFrame1(master=self, width=500), text="Create Course Subject")
        self.add(TabFrame2(master=self, width=500), text="View Course Subject")

class TabFrame1(ttk.Frame):
    def __init__(self, master, width):
        super().__init__(master=master, width=width)
        self.pack()

        # Widgets
        self.title = ttk.Label(
            master=self,
            text="Create Course Subject",
            font="Calibri 36 bold")
        self.title.pack(padx=10)
        
        # Subject Code
        self.SubjCode_Var = tk.StringVar()
        self.SubjCode_Frame = ttk.Frame(master=self)
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
        self.SubjName_Frame = ttk.Frame(master=self)
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
        self.SubjUnits_Frame = ttk.Frame(master=self)
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

        self.submit_button = ttk.Button(
            master=self,
            text="Create Course Subject",
            command=self.submit
        )
        self.submit_button.pack(pady=3)

        self.result = ttk.Label(
            master=self,
            text="",
            font="Calibri 18 bold")
        self.result.pack(pady=3)

    def submit(self):
         # Get the values from the entry fields
        SubjCode = self.SubjCode_Var.get()
        SubjName = self.SubjName_Var.get()
        SubjUnits = self.SubjUnits_Var.get()

        # Add the values to the database
        self.master.master.enrollmentdb.add_to_DB(SubjCode, SubjName, SubjUnits)

        # Display the result
        self.result.config(text="Course Subject Created")

        # Clear the entry fields
        self.SubjCode_Var.set("")
        self.SubjName_Var.set("")
        self.SubjUnits_Var.set("")

class TabFrame2(ttk.Frame):
    def __init__(self, master, width):
        super().__init__(master=master, width=width)
        self.pack()

        # Widgets
        self.title = ttk.Label(
            master=self,
            text="View Course Subjects",
            font="Calibri 36 bold")
        self.title.pack()

        # Frame for button and listbox
        self.frame = ttk.Frame(master=self)
        self.frame.pack(side='left', padx=10, pady=10)

        # Frame for the listbox and scrollbar
        self.list_scroll_frame = ttk.Frame(master=self.frame)
        self.list_scroll_frame.pack()
        

        self.listbox = tk.Listbox(master=self.list_scroll_frame, width=10, height=5, font="Calibri 18",state="disabled")
        self.listbox.pack(side="left", padx=5)

        self.listbox.bind("<<ListboxSelect>>", self.list_select)

        self.scrollbar = ttk.Scrollbar(master=self.list_scroll_frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side="left", padx=5, fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Refresh Button
        self.refresh_button = ttk.Button(
            master=self.frame,
            text="Refresh",
            command=self.refresh
        )
        self.refresh_button.pack(side='bottom',pady=3, padx=5)

        # Details Label
        self.details_label = ttk.Label(
            master=self,
            text="Details: ",
            font="Calibri 18 bold")
        self.details_label.pack(pady=10)

        # Course Name Label that will be updated
        self.course_name = ttk.Label(
            master=self,
            text="",
            font="Calibri 18 bold",
            foreground="blue")
        self.course_name.pack(pady=10)

        # Units Label that will be updated
        self.units = ttk.Label(
            master=self,
            text="",
            font="Calibri 18")
        self.units.pack(pady=10)

    def refresh(self):
        # enable the listbox
        self.listbox.config(state="normal")

        # Clear the listbox
        self.listbox.delete(0, "end")

        # Get the data from the database
        results = self.master.master.enrollmentdb.view_all()

        # Populate the listbox
        for result in results:
            self.listbox.insert("end", result[0])
    
    def list_select(self, event):
        # Get the name of the course subject
        course_code = self.listbox.get(self.listbox.curselection())

        # Get the data from the database
        result = self.master.master.enrollmentdb.view_one(course_code)

        # Update the labels
        self.course_name.config(text=result[1])
        self.units.config(text=f'{result[2]} Units')

if __name__ == "__main__":
    App(title="Program Courses", size=(500,300), icon="MSEUF_LOGO_HD.ico")