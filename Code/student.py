from udfs import *

# Add/Edit Student perticulars
class Screen1:

    label_list = []
    checkbox_list = []

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
        self.frame2.pack(side="left", expand=True, fill='y')

        # Name
        self.name_label = tk.Label(self.frame2, text="Name:", font="Arial 24", anchor='w')
        self.name_label.grid(row=0, column=0, padx=20, pady=10, sticky='we')
        self.name = tk.StringVar(self.frame2)
        self.name_entry = tk.Entry(self.frame2, textvariable=self.name, font="Arial 24", justify="center")
        self.name_entry.grid(row=0, column=1, padx=20, pady=10, sticky='we')
        self.name_entry.bind("<Return>", self.focus_uid)
        self.name_entry.bind("<Down>", self.focus_uid)

        # UID
        self.uid_label = tk.Label(self.frame2, text="UID:", font="Arial 24", anchor='w')
        self.uid_label.grid(row=1, column=0, padx=20, pady=10, sticky='we')
        self.uid = tk.StringVar(self.frame2)
        self.uid_entry = tk.Entry(self.frame2, textvariable=self.uid, font="Arial 24", justify="center")
        self.uid_entry.grid(row=1, column=1, padx=20, pady=10, sticky='we')
        self.uid_entry.bind("<Return>", self.focus_roll_no)
        self.uid_entry.bind("<Up>", self.focus_name)
        self.uid_entry.bind("<Down>", self.focus_roll_no)

        # Roll Number
        self.roll_no_label = tk.Label(self.frame2, text="Roll Number:", font="Arial 24", anchor='w')
        self.roll_no_label.grid(row=2, column=0, padx=20, pady=10, sticky='we')
        self.roll_no = tk.StringVar(self.frame2)
        self.roll_no_entry = tk.Entry(self.frame2, textvariable=self.roll_no, font="Arial 24", justify="center")
        self.roll_no_entry.grid(row=2, column=1, padx=20, pady=10, sticky='we')
        self.roll_no_entry.bind("<Up>", self.focus_uid)

        # Class
        self.clas_label = tk.Label(self.frame2, text="Class:", font="Arial 24", anchor='w')
        self.clas_label.grid(row=3, column=0, padx=20, pady=10, sticky='we')
        self.clas = tk.StringVar(self.frame2)
        self.clas_dropdown = tk.OptionMenu(self.frame2, self.clas, "XII", command=self.ask_stream)
        self.clas_dropdown.grid(row=3, column=1, padx=20, pady=10, sticky='we')
        self.clas_dropdown.config(width=20, font="Arial 24", relief='ridge')
        menu = root.nametowidget(self.clas_dropdown.menuname)
        menu.config(font="Arial 18")

        # Section
        self.sec_label = tk.Label(self.frame2, text="Section:", font="Arial 24", anchor='w')
        self.sec_label.grid(row=4, column=0, padx=20, pady=10, sticky='we')
        self.sec = tk.StringVar(self.frame2)
        self.sec_dropdown = tk.OptionMenu(self.frame2, self.sec, 'A', 'B', 'C', 'D', 'E', 'F', command=self.on_sec)
        self.sec_dropdown.grid(row=4, column=1, padx=20, pady=10, sticky='we')
        self.sec_dropdown.config(width=20, font="Arial 24", relief='ridge')
        menu = root.nametowidget(self.sec_dropdown.menuname)
        menu.config(font="Arial 18")

    def ask_stream(self, clas):
        if clas in ("XI", "XII"):
            self.stream_label = tk.Label(self.frame2, text="Stream:", font="Arial 24", anchor='w')
            self.stream_label.grid(row=5, column=0, padx=20, pady=10, sticky='we')
            self.stream = tk.StringVar(self.frame2)
            self.stream_dropdown = tk.OptionMenu(self.frame2, self.stream, "Science", "Commerce", command=self.ask_subjects)
            self.stream_dropdown.grid(row=5, column=1, padx=20, pady=10, sticky='we')
            self.stream_dropdown.config(width=20, font="Arial 24", relief='ridge')
            menu = self.root.nametowidget(self.stream_dropdown.menuname)
            menu.config(font="Arial 18")
            if self.sec.get() in ('A', 'B', 'C', 'D'):
                self.stream.initialize("Science")
                self.ask_subjects("Science")
            elif self.sec.get() in ('E', 'F'):
                self.stream.initialize("Commerce")
                self.ask_subjects("Commerce")
            self.update_pallete(*self.colors)

    def ask_subjects(self, stream):
        try:
            self.frame3.destroy()
            self.label_list.clear()
            self.checkbox_list.clear()
        except AttributeError:
            pass
        finally:
            self.Selected_Subs = {}
        self.frame3 = tk.Frame(self.frame1)
        self.frame3.pack(expand=True, fill='y', side="right", anchor='w')
        label = tk.Label(self.frame3, text="Subjects", font="Arial 24")
        label.grid(row=0, column=0, columnspan=2, pady=10)
        self.label_list.append(label)

        if stream=="Science":
            if self.sec.get() in ('E', 'F'): self.sec.set('')
            # Creating checkbuttons
            Subs = Sci_Subs
            for i in range(len(Subs)):
                check = i in (0, 1, 4)
                self.create_checkbtn(Subs[i], i+1, check)

        elif stream=="Commerce":
            if self.sec.get() in ('A', 'B', 'C', 'D'): self.sec.set('')
            # Creating checkbuttons
            Subs = Comm_Subs
            for i in range(len(Subs)):
                check = i in (0, 1, 2, 3)
                self.create_checkbtn(Subs[i], i+1, check)
        
        self.add_btn = tk.Button(self.frame3, text="Add", font="Arial 18 bold", width=10, command=self.add)
        self.add_btn.grid(row=len(Subs)+1, column=0, columnspan=2, pady=10)
        self.update_pallete(*self.colors)

    def create_checkbtn(self, sub, row_no, check=False):
        check_btn = tk.Checkbutton(self.frame3)
        check_btn.grid(row=row_no, column=0)
        if check:
            check_btn.select()
            sub_type = "main"
        else:
            check_btn.deselect()
            sub_type = "elective"
        check_btn.configure(command= lambda: self.on_check_btn(sub))
        self.Selected_Subs[sub]=[check_btn, check, sub_type]
        label = tk.Label(self.frame3, text=sub, font="Arial 18", anchor='w')
        label.grid(row=row_no, column=1, sticky='we')
        self.label_list.append(label)
        self.checkbox_list.append(check_btn)

    def on_check_btn(self, sub):
        self.Selected_Subs[sub][1] = not self.Selected_Subs[sub][1]

    def on_sec(self, sec):
        if sec in ('A', 'B', 'C', 'D') and self.clas.get() in ("XI", "XII"):
            self.stream.set("Science")
            self.ask_subjects("Science")
        elif sec in ('E', 'F') and self.clas.get() in ("XI", "XII"):
            self.stream.set("Commerce")
            self.ask_subjects("Commerce")

    def add(self):
        if self.validate():
            try:
                Subs = []
                for sub in self.Selected_Subs:
                    if self.Selected_Subs[sub][1]:
                        Subs.append(-1)
                    else:
                        Subs.append('NULL')
                Subs.append(-1)     # for Total
                Subs = str(Subs).lstrip('[').rstrip(']').replace("'NULL'", "NULL")
                clas = RomanToNum[self.clas.get()]
                if self.stream.get()=="Science":
                    stream = "sci"
                elif self.stream.get()=="Commerce":
                    stream = "comm"
                for exam in ShortForm.values():
                    table_name = exam+'_'+clas+'_'+stream
                    self.db.cursor.execute(f"INSERT INTO {table_name} VALUES({self.roll_no.get()}, {self.uid.get()}, '{self.name.get()}', '{self.sec.get()}', {Subs})")
                self.db.cursor.execute("COMMIT")
                self.specs.Notify("info", "Student Added")
                self.uid.set('')
                if self.roll_no.get()[-2:] in('99', ''):
                    self.roll_no.set('')
                else:
                    self.roll_no.set(str(int(self.roll_no.get())+1))
                self.name.set('')
                self.name_entry.focus()
            except Exception as e:
                self.specs.Notify("error", e)

    def focus_name(self, event):
        self.name_entry.focus()
        self.name_entry.select_range(0, 'end')
        self.name_entry.icursor('end')

    def focus_uid(self, event):
        self.uid_entry.focus()
        self.uid_entry.select_range(0, 'end')
        self.uid_entry.icursor('end')

    def focus_roll_no(self, event):
        self.roll_no_entry.focus()
        self.roll_no_entry.select_range(0, 'end')
        self.roll_no_entry.icursor('end')

    def check_rno(self):
        rno = self.roll_no.get()
        prefix = RomanToNum[self.clas.get()]+str(ord(self.sec.get())-64)
        if not rno.isdigit(): return False
        if len(rno)==1: self.roll_no.set('0'+rno)
        if len(rno)==2:
            self.roll_no.set(prefix+rno)
            return True
        if len(rno)==5 and rno.startswith(prefix):
            return True
        return False
        

    def validate(self):

        if (self.name.get()+' ').isspace():
            self.specs.Notify("error", "Name can not be left empty.")
            return False
        elif not self.name.get().replace(' ', '').isalpha():
            self.specs.Notify("error", "The given name is invalid, name should only contain alphabets and spaces.")
            return False

        elif (self.uid.get()+' ').isspace():
            self.specs.Notify("error", "UID can not be left empty.")
            return False
        elif not self.uid.get().isdecimal():
            self.specs.Notify("error", "The given UID is invalid, UID should only contain numbers.")
        elif not self.uid_is_available():
            self.specs.Notify("error", "UID already present.")
            return False

        elif (self.roll_no.get()+' ').isspace():
            self.specs.Notify("error", "Roll Number can not be left empty.")
            return False
        elif not self.roll_no.get().isdecimal():
            self.specs.Notify("error", "The given Roll Number is invalid, Roll Number should only contain numbers.")
            return False
        elif not self.rno_is_available():
            self.specs.Notify("error", "Roll number already present.")
            return False

        elif self.sec.get()=='':
            self.specs.Notify("error", "A Section must be selected.")
            return False

        msg = self.check_subs()
        if msg != True:
            self.specs.Notify("error", "Invalid combination:\n"+msg)
            return False

        if not self.check_rno():
            self.specs.Notify("error", "Invalid Roll Number.")
            return False

        # At the last if no error then True is returned and this record will be added in the database
        return True

    def check_subs(self):
        total_count = main_count = elective_count = 0
        stream = self.stream.get()

        for sub in self.Selected_Subs:
            if self.Selected_Subs[sub][1]:
                total_count += 1
            if self.Selected_Subs[sub][1] and self.Selected_Subs[sub][2]=="main":
                main_count += 1
            elif self.Selected_Subs[sub][1] and self.Selected_Subs[sub][2]=="elective":
                elective_count += 1

        if total_count<5:
            return "5 subjects must be selected."
        elif total_count>5:
            return "Only 5 subjects can be selected."

        if stream=="Science":
            if main_count<3:
                return "Physics, Chemistry and English must be selected."
            elif self.Selected_Subs["Mathematics"][1] and self.Selected_Subs["Psychology"][1]:
                return "Only one can be selected amoung Mathematics and Psychology."
            elif (self.Selected_Subs["Computer Science"][1], self.Selected_Subs["Engineering Graphics"][1], self.Selected_Subs["Biology"][1]).count(True)>1:
                return "Only one can be selected amoung Computer Science, Engineering Graphics and Biology."
            elif self.Selected_Subs["Psychology"][1]:
                if self.Selected_Subs["Computer Science"][1]:
                    return "Computer Science cannot be selected with Psychology."
                elif self.Selected_Subs["Engineering Graphics"][1]:
                    return "Engineering Graphics cannot be selected with Psychology."
                
        elif stream=="Commerce":
            if main_count<4:
                return "Business Studies, Accountancy, Economics and English must be selected."
            elif elective_count>1:
                return "Only one can be selected amoung Applied Maths, Entrepreneurship and Legal Studies."
        
        return True

    def uid_is_available(self):
        uid = int(self.uid.get())
        self.db.cursor.execute("SELECT UID FROM pmt_12_sci")
        lst1 = [i[0] for i in self.db.cursor.fetchall()]
        self.db.cursor.execute("SELECT UID FROM pmt_12_comm")
        lst2 = [i[0] for i in self.db.cursor.fetchall()]
        uid_list = lst1 + lst2
        if uid in uid_list: return False
        return True

    def rno_is_available(self):
        self.check_rno()
        rno = int(self.roll_no.get())
        stream = self.stream.get()
        match stream:
            case "Science":
                self.db.cursor.execute(f"SELECT Roll_No FROM pmt_12_sci")
            case "Commerce":
                self.db.cursor.execute(f"SELECT Roll_No FROM pmt_12_comm")
        rno_list = [i[0] for i in self.db.cursor.fetchall()]
        if rno in rno_list: return False
        return True

    def update_pallete(self, c1, c2, c3, c4):
        for i in (self.heading, self.frame1, self.frame2,
        self.name_label, self.uid_label, self.roll_no_label, self.clas_label, self.sec_label):
            i["bg"] = c1
        for i in (self.name_entry, self.uid_entry, self.roll_no_entry, self.clas_dropdown, self.sec_dropdown):
            i["bg"] = c3
        try:
            self.stream_label["bg"] = c1
            self.stream_dropdown["bg"] = c3
        except AttributeError:
            pass
        try:
            for i in (self.frame3, *self.label_list):
                i["bg"] = c1
            self.add_btn["bg"] = c2
            Animate(self.add_btn)
            for box in self.checkbox_list:
                box["bg"] = c4
        except AttributeError:
            pass
        self.colors = (c1, c2, c3, c4)


    def select(self):
        self.frame1.lift()
        self.frame1.focus()