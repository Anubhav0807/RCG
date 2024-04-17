from udfs import *
import datetime
try:
    from fpdf import FPDF
except ModuleNotFoundError:
    messagebox.showwarning("Module Not Found", "Module named fpdf was not found. \nGo to the command prompt and run the command: \npip install fpdf2")
    quit()

# Ignoring warnings
import warnings
warnings.filterwarnings("ignore")

class Screen3():

    # Variables
    row_no = 0
    values = []
    label_list = []

    def __init__(self, root, specs, db):
        self.root = root
        self.specs = specs
        self.db = db
        
        # Frame for the entire screen
        self.frame1 = tk.Frame(root)
        self.frame1.place(x=0, y=0, relwidth=1, relheight=1)

        # Heading Label
        self.heading = tk.Label(self.frame1, text="Please fill the following details:", font="Arial 24 bold")
        self.heading.pack(pady=30)

        # Frame with all perticulars
        self.frame2 = tk.Frame(self.frame1)
        self.frame2.pack()

        # Creating 4 dropdowns
        self.Dropdowns = {}
        self.CreateDropdown("Class", ('XII',))
        self.CreateDropdown("Section", ('A', 'B', 'C', 'D', 'E', 'F'))

        # Entry Widget to input roll number (default value = all)
        label = tk.Label(self.frame2, text="Roll Number:", font="Arial 24", anchor='w')
        label.grid(row=self.row_no, column=0, padx=20, pady=10, sticky='we')
        self.label_list.append(label)
        variable = tk.StringVar(self.frame2)
        variable.initialize("all")
        self.values.append(variable)
        self.roll_no_entry = tk.Entry(self.frame2, textvariable=variable, font="Arial 24", justify="center")
        self.roll_no_entry.grid(row=self.row_no, column=1, padx=20, pady=10, sticky='we')
        self.roll_no_entry.bind("<Button-1>", self.on_click)
        self.roll_no_entry.bind("<Return>", self.generate_pdf)
        self.row_no += 1

        # Checkbutton to toggle open the File/Folder or not
        self.frame3 = tk.Frame(self.frame1)
        self.frame3.pack()
        self.open = tk.IntVar(self.frame1)
        self.check_btn = tk.Checkbutton(self.frame3, anchor='e', variable=self.open)
        self.check_btn.grid(row=0, column=0)
        self.textvar = tk.StringVar(self.frame1)
        self.textvar.initialize("Open the Folder after generating the pdfs")
        label = tk.Label(self.frame3, textvariable=self.textvar, anchor='w', font="Arial 18")
        label.grid(row=0, column=1, pady=10)
        self.label_list.append(label)

        # Button to Generate Report Card in .pdf form
        self.pdf_btn = tk.Button(self.frame1, text="Generate the PDF!", font="Arial 24", command=self.generate_pdf, state="disable")
        self.pdf_btn.pack(pady=20)

    def CreateDropdown(self, category, options):
        label = tk.Label(self.frame2, text=f"Select the {category}:", font="Arial 24", anchor='w')
        label.grid(row=self.row_no, column=0, pady=20, padx=20, sticky='we')
        variable = tk.StringVar(self.root)
        dropdown = tk.OptionMenu(self.frame2, variable, *options, command=self.EnableBtn)
        dropdown.config(width=20, font="Arial 24", relief='ridge')
        dropdown.grid(row=self.row_no, column=1, padx=20)
        self.Dropdowns[category]=dropdown
        menu = self.root.nametowidget(dropdown.menuname)
        menu.config(font="Arial 18")
        self.row_no += 1
        self.values.append(variable)
        self.label_list.append(label)

    def EnableBtn(self, value=None):
        if self.roll_no_entry.get().lower()=="all":
            self.textvar.set("Open the Folder after generating the pdfs")
        else:
            self.textvar.set("Open the file after generating the pdf")

        for i in self.values:
            if i.get()=="":
                if self.pdf_btn["state"] != "disabled":
                    self.pdf_btn["state"] = "disable"
                    InAnimate(self.pdf_btn)
                    self.update_pallete(*self.colors)
                return False
        self.pdf_btn["state"] = "normal"
        Animate(self.pdf_btn)
        return True

    def BindAll(self):
        self.root.bind_all("<Key>", self.EnableBtn, add='+')

    def UnbindAll(self):
        self.root.unbind_all("<Key>")

    def on_click(self, event=None):
        if self.roll_no_entry.get().lower()=="all": self.roll_no_entry.delete(0, "end")
        self.EnableBtn()

    def generate_pdf(self, event=None):
        self.clas = self.values[0].get()
        self.sec = self.values[1].get()
        self.roll_no = self.values[2].get().lower()
        if self.roll_no != "all":
            try:
                self.roll_no = int(self.roll_no)%100
            except ValueError:
                self.specs.Notify("error", "Invalid Roll Number.")
                return
        table_name = GetTableName("Pre-Midterm", self.clas, self.sec)
        if "sci" in table_name:
            self.Subs = Sci_Subs
        elif "comm" in table_name:
            self.Subs = Comm_Subs

        if self.roll_no=="all":
            self.db.cursor.execute(f"SELECT COUNT(uid) FROM {table_name} WHERE Section='{self.sec}'")
            n = int(self.db.cursor.fetchone()[0])
        else:
            n = 1
        self.db.cursor.execute(f"SELECT uid, roll_no, name FROM {table_name} WHERE Section='{self.sec}'")
        stud = self.db.cursor.fetchall()
        if stud==[]:
            self.specs.Notify("error", f"{self.clas}-'{self.sec}' is empty.")
            return
        
        for i in range(n):
            
            if self.roll_no != "all":    # This will be True if the user only wants to generate pdf for a specific student
                if self.roll_no not in [rec[1]%100 for rec in stud]:
                    self.specs.Notify("error", f"Roll Number {self.roll_no} is not present.")
                    return
                i = self.roll_no-1
            
            # Create a FPDF Object
            pdf = FPDF('L', 'mm', 'Legal')
            pdf.add_page()

            # Title
            try: pdf.image(resource_path("Assets/Images/dav-logo.png"), 10, 8, 40)
            except FileNotFoundError: pass
            pdf.set_font('helvetica', 'B', 24)
            pdf.cell(0, 10, "D.A.V Boys Senior Secondary School, Chennai 600086", ln=True, align='C')
            date = datetime.date.today().isoformat()
            date = date.split('-')
            date = date[2]+'-'+date[1]+'-'+date[0]
            pdf.cell(0, 20, f"Report Card {date}", ln=True, align='C')

            # Student name, roll_no, class and section
            pdf.ln(15)
            pdf.set_font('helvetica', 'B', 16)
            pdf.set_x(50)
            pdf.cell(100, 10, f"Name: {stud[i][2]}")
            pdf.cell(100, 10, f"Roll Number: {stud[i][1]}")
            pdf.cell(100, 10, f"Class: {self.clas} '{self.sec}'")
            
            # Creating a tabulation
            matrix = []
            pdf.ln(15)

            # Knowing which are the 5 subjects of the student
            self.db.cursor.execute(f"SELECT * FROM {table_name} WHERE uid={stud[i][0]} AND roll_no={stud[i][1]}")
            all_subs = self.db.cursor.fetchone()[4:-1]
            self.sub_index_lst = [i for i in range(len(all_subs)) if all_subs[i] != None]

            # Extracting the data for a perticular student from all the 8 tables
            for exam in ShortForm:
                table_name = GetTableName(exam, self.clas, self.sec)
                self.db.cursor.execute(f"SELECT * FROM {table_name} WHERE uid={stud[i][0]} AND roll_no={stud[i][1]}")
                matrix.append(self.validate(self.db.cursor.fetchone()[4:]))

            # Placing the marks
            matrix = self.transpose(matrix)
            self.add_row_headers(matrix)
            self.add_col_headers(matrix)
            self.add_sign(matrix)
            for j in range(len(matrix)):
                pdf.set_x(35)
                for k in range(len(matrix[0])):
                    if j==0 or k==0:
                        pdf.set_font('helvetica', 'B', 12)
                    else:
                        pdf.set_font('helvetica', '', 12)
                    if k==0:
                        pdf.set_text_color(0, 0, 0)
                        pdf.cell(45, 10, str(matrix[j][k]), align='C', border=True)
                    else:
                        if j in (1,2,3,4,5) and k != 0:
                            try:
                                if matrix[j][k] < 40:
                                    pdf.set_text_color(255, 0, 0)
                                else:
                                    pdf.set_text_color(0, 150, 0)
                            except TypeError:
                                pdf.set_text_color(0, 0, 0)
                            pdf.cell(30, 10, str(matrix[j][k]), align='C', border=True)
                        else:
                           pdf.set_text_color(0, 0, 0)
                           pdf.cell(30, 10, str(matrix[j][k]), align='C', border=True)
                pdf.ln()

            # Producing the output pdf in the same directory with name as uid_rollno.pdf
            file_name = f"{self.specs.data['path']}/PDFs/Class_{RomanToNum[self.clas]}/{RomanToNum[self.clas]}_{self.sec}/{stud[i][0]}_{stud[i][1]}.pdf"
            try:
                try:
                    if file_name.startswith('/'): raise FileNotFoundError
                    pdf.output(file_name)
                except FileNotFoundError:
                    path = filedialog.askdirectory()
                    if path=='': return     # If the user presses Cancel then don't generate pdfs
                    file_name = f"{path}/PDFs/Class_{RomanToNum[self.clas]}/{RomanToNum[self.clas]}_{self.sec}/{stud[i][0]}_{stud[i][1]}.pdf"
                    self.create_directory(path)
                    self.specs.data['path'] = path
                    pdf.output(file_name)
            except PermissionError:
                self.specs.Notify("error", "Can't generate the pdf because that file is already open.")
                return

        # Starting the pdf file if there is only one or else opening the directory
        if self.open.get():
            if self.roll_no=="all": os.startfile(f"{self.specs.data['path']}/PDFs/Class_{RomanToNum[self.clas]}/{RomanToNum[self.clas]}_{self.sec}")
            else: os.startfile(file_name)

        # Send message to the user that the pdfs were generated successfully
        if n==1:
            self.specs.Notify("info", f"Report Card has been generated Successfully. \nIn the form of pdf, for {stud[i][2]} of Class "
                +f"{self.clas}-'{self.sec}'", popUp=(not self.open.get()))
        else:
            self.specs.Notify("info", "Report Cards have been generated Successfully. \nIn the form of pdf, for Class "
                +f"{self.clas}-'{self.sec}'", popUp=(not self.open.get()))

    def add_row_headers(self, matrix):
        for i, heading in enumerate([self.Subs[j] for j in self.sub_index_lst]+["Total"]):  # 5 Subject + Total
            matrix[i] = [heading]+matrix[i]

    def add_col_headers(self, matrix):
        "Examination as Column headers"
        matrix.insert(0, ["Subjects"]+Exams)

    def add_sign(self, matrix):
        for sign in ("Principal Sign", "Class Teacher Sign", "Parent's Sign"):
            row = [sign]+['' for i in range(8)]
            matrix.append(row)

    def validate(self, lst1):
        lst2 = []
        for i in range(len(lst1)):
            if lst1[i]==None:
                continue
            elif lst1[i]==-1:
                lst2.append('')
            elif lst1[i]==-2:
                lst2.append("Ab")
            else:
                lst2.append(lst1[i])
        return lst2

    def transpose(self, matrix):
        trans = []
        for i in range(len(matrix[0])):
            row = []
            for j in range(len(matrix)):
                row.append(matrix[j][i])
            trans.append(row)            
        return trans

    def create_directory(self, path):
        try: os.mkdir(f"{path}/PDFs")
        except FileExistsError: pass
        for i in range(1, 13):
            try: os.mkdir(f"{path}/PDFs/Class_{i}")
            except FileExistsError: pass
        for sec in "ABCDEF":
            try: os.mkdir(f"{path}/PDFs/Class_12/12_{sec}")
            except FileExistsError: pass

    def update_pallete(self, c1, c2, c3, c4):
        for i in (self.frame1, self.frame2, self.frame3, self.heading, *self.label_list):
            i["bg"] = c1
        for dropdown in self.Dropdowns:
            self.Dropdowns[dropdown]["bg"] = c3
        self.roll_no_entry["bg"] = c3
        self.check_btn["bg"] = c4
        self.pdf_btn["bg"] = c2
        Animate(self.pdf_btn)
        self.colors = (c1, c2, c3, c4)

    def select(self):
        self.frame1.lift()
        self.frame1.focus()
        self.BindAll()