from udfs import *

# Add/Edit Marks Screen Part-1
class Screen2_1:

    # Variables
    row_no = 0
    values = []
    label_lsit = []

    def __init__(self, root, screen2_2, specs, db):
        self.root = root
        self.screen2_2 = screen2_2
        self.specs = specs
        self.db = db

        # Frame for the entire screen
        self.frame1 = tk.Frame(root)
        self.frame1.place(x=0, y=0, relwidth=1, relheight=1)

        # Heading Label
        self.heading = tk.Label(self.frame1, text="Please fill the following details:", font="Arial 24 bold")
        self.heading.pack(pady=30)

        # Frame for dropdowns
        self.frame2 = tk.Frame(self.frame1)
        self.frame2.pack()

        # Creating 4 dropdowns
        self.Dropdowns = {}
        self.CreateDropdown("Examination", Exams)
        self.CreateDropdown("Class", ('XII',))
        self.CreateDropdown("Section", ('A', 'B', 'C', 'D', 'E', 'F'))
        self.CreateDropdown("Subject",
             ("Physics", "Chemistry", "Mathematics", "Psychology", "English", "Computer Science", "Biology", "Engineering Graphics")
            +("Business Studies", "Accountancy", "Economics", "Applied Mathematics", "Entrepreneurship", "Legal Studies"))

        # Add Marks Button
        self.btn1 = tk.Button(self.frame1, text="Add Marks", font="Arial 24", 
                command=self.ShowRecords, state="disable")
        self.btn1.pack(pady=30)
    
    # Methods

    def ShowRecords(self):
        values_str = [value.get() for value in self.values]
        self.screen2_2.set_values(values_str)
        self.screen2_2.select()

    def EnableBtn(self, value):
        if value in ('A', 'B', 'C', 'D'):
            if self.values[3].get() not in Sci_Subs: self.values[3].set("")
            self.Dropdowns["Subject"].destroy()
            options=Sci_Subs
            dropdown = tk.OptionMenu(self.frame2, self.values[-1], *options, command=self.EnableBtn)
            dropdown.config(width=20, font="Arial 24", relief='ridge')
            menu = self.root.nametowidget(dropdown.menuname)
            menu.config(font="Arial 18")
            dropdown.grid(row=self.row_no-1, column=1, padx=20)
            self.Dropdowns["Subject"]=dropdown
        elif value in ('E', 'F'):
            if self.values[3].get() not in Comm_Subs: self.values[3].set("")
            self.Dropdowns["Subject"].destroy()
            options=Comm_Subs
            dropdown = tk.OptionMenu(self.frame2, self.values[-1], *options, command=self.EnableBtn)
            dropdown.config(width=20, font="Arial 24", relief='ridge')
            menu = self.root.nametowidget(dropdown.menuname)
            menu.config(font="Arial 18")
            dropdown.grid(row=self.row_no-1, column=1, padx=20)
            self.Dropdowns["Subject"]=dropdown

        for i in self.values:
            if i.get()=="":
                self.update_pallete(*self.colors)
                return False
        self.btn1["state"] = "normal"
        self.update_pallete(*self.colors)
        return True

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
        self.label_lsit.append(label)

    def update_pallete(self, c1, c2, c3, c4):
        for i in (self.frame1, self.heading, self.frame2, *self.label_lsit):
            i["bg"] = c1
        for dropdown in self.Dropdowns:
            self.Dropdowns[dropdown]["bg"] = c3
        self.btn1["bg"] = c2
        Animate(self.btn1)
        self.colors = (c1, c2, c3, c4)

    def select(self):
        self.frame1.lift()
        self.frame1.focus()

# Add/Edit Marks Screen Part-2
class Screen2_2:

    # Variables
    changes = False
    pre_selected = True
    entry_color = "#FFFFFF"
    entry_visible = False

    def __init__(self, root, specs, db):
        self.root = root
        self.specs = specs
        self.db = db

        # Frame for the entire screen
        self.frame1 = tk.Frame(root)
        self.frame1.place(x=0, y=0, relwidth=1, relheight=1)

        # Heading Label
        self.heading = tk.Label(self.frame1, text="Examination - ??? \nClass - ??? \nSubject - ???", font="Arial 24 bold")
        self.heading.pack(pady=20)

        # Save Button
        self.btn1 = tk.Button(self.frame1, text="Save", font="Arial 18 bold", width=10, command=self.Save)
        self.btn1.pack(side="bottom", pady=20)

        # Back Button (Actually its a Label!)
        self.btn2 = tk.Label(self.frame1, text="⟸", font="Arial 32 bold")
        self.btn2.place(x=10, y=0)
        self.btn2.bind("<Button-1>", self.Back)

        # Frame for table
        self.frame2 = tk.Frame(self.frame1)
        self.frame2.pack(expand=True, fill="both", padx=20)

        # Packing a scrollbar on the right side
        scrollbar = tk.Scrollbar(self.frame2)
        scrollbar.pack(side="right", fill='y')

        # Tree View
        self.table = ttk.Treeview(self.frame2, columns=("roll_no", "name", "marks"), selectmode="browse")
        self.table.pack(side="left", expand=True, fill="both")

        # Linking the scrollbar with table
        scrollbar.configure(command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        # Theme for the table
        self.style = ttk.Style(self.frame2)
        self.style.theme_use("alt")

        # Font and Colour of table
        self.style.configure("Treeview.Heading", font=(None, 20, "bold"))
        self.style.configure("Treeview", font=(None, 18), rowheight=50)

        # Headings
        self.table.heading("#0", text='')
        self.table.heading("roll_no", text="Roll Number")
        self.table.heading("name", text="Name")
        self.table.heading("marks", text="Marks")

        # Columns
        self.table.column("#0", width=0, stretch="no")
        self.table.column("roll_no", anchor="center")
        self.table.column("name", anchor="center")
        self.table.column("marks", anchor="center")

        # Binding UDF with events
        self.heading.bind("<Button-1>", self.on_focus_lost)
        scrollbar.bind("<ButtonPress-1>", self.Place)
        scrollbar.bind("<B1-Motion>", self.Place)
        self.frame1.bind("<Leave>", self.on_focus_lost)
        self.frame1.bind_all("<Control-s>", self.Save)
        self.frame1.bind("<Button-1>", self.on_focus_lost)
        self.table.bind("<ButtonRelease-1>", self.on_click_release)

    def on_click_release(self, event):
        region_clicked = self.table.identify_region(event.x, event.y)
        if region_clicked != "cell": return
        self.column = self.table.identify_column(event.x)
        self.selected_iid = self.table.focus()
        self.selected_text = self.table.item(self.selected_iid, "values")[int(self.column[1:])-1]
        if self.column=="#3": self.CreateEntry()

    def on_focus_lost(self, event=None):
        try:
            new_value = self.entry.get()
            if new_value.lower() in ("ab", "absent"):
                new_value = "Absent"
            elif not (new_value+' ').isspace():
                for i in new_value:
                    if not(i.isdigit() or i in ('+', '-', 'x', '/', '^', '.', ' ')):
                        self.entry.destroy()
                        return
                new_value = new_value.replace('^', '**')
                new_value = new_value.replace('x', '*')
                try:
                    new_value = eval(new_value)
                except Exception:
                    self.entry.destroy()
                    return

            if type(new_value)==float: new_value = round(new_value)
            if type(new_value)==int and (new_value<0 or new_value>100):
                self.entry.destroy()
                return

            selected_values = self.table.item(self.selected_iid).get("values")
            selected_values[2] = new_value
            self.table.item(self.selected_iid, values=selected_values)
            self.entry.destroy()

        except Exception:
            pass

    def CreateEntry(self):
        try:
            self.entry.destroy()
        except AttributeError:
            pass
        self.entry = tk.Entry(self.frame2, font=(None, 18), justify="center", bg=self.entry_color)
        self.entry.insert(0, self.selected_text)
        if self.pre_selected: self.entry.select_range(0, "end")
        self.entry.focus()
        self.Place()
        self.entry.bind("<FocusOut>", self.on_focus_lost)
        self.entry.bind("<Escape>", self.on_focus_lost)
        self.entry.bind("<Key>", self.Jump)
        self.table.selection_set(self.selected_iid)
        self.SaveOnClose()

    def Place(self, event=None):
        try:
            cell_box = self.table.bbox(self.selected_iid, self.column)    # x, y, width, height
            self.entry.place(x=cell_box[0]+4, y=cell_box[1]+4, w=cell_box[2]-8, h=cell_box[3]-8)
            if cell_box[1]>self.frame2.winfo_height()-50: # Here 50 is rowheight (Important)
                self.entry.place_forget()
                self.entry_visible = False
            else:
                self.entry_visible = True
        except Exception:
            try:
                self.entry.place_forget()
                self.entry_visible = False
            except Exception:
                self.entry_visible = False

    def MoveUp(self, event):
        try:
            if int(self.selected_iid)==0 or self.column!="#3": return
            self.on_focus_lost()
            self.selected_iid = str(int(self.selected_iid)-1)
            self.selected_text = self.table.item(self.selected_iid, "values")[int(self.column[1:])-1]
            cell_box = self.table.bbox(self.selected_iid, self.column)    # x, y, width, height
            if cell_box=='': self.table.yview_scroll(-1, "units")
            self.CreateEntry()
            self.Jump()
        except Exception:
            pass

    def MoveDown(self, event):
        try:
            if int(self.selected_iid)==len(self.mydata)-1 or self.column!="#3": return
            self.on_focus_lost()
            self.selected_iid = str(int(self.selected_iid)+1)
            self.selected_text = self.table.item(self.selected_iid, "values")[int(self.column[1:])-1]
            cell_box = self.table.bbox(self.selected_iid, self.column)    # x, y, width, height
            if cell_box=='' or cell_box[1]>self.frame2.winfo_height()-50: # Here 50 is rowheight (Important)
                self.table.yview_scroll(+1, "units")
            self.CreateEntry()
            self.Jump()
        except Exception:
            pass

    def Jump(self, event=None):
        if not self.entry_visible:
            self.table.yview_moveto(int(self.selected_iid)/len(self.mydata))
            self.table.update_idletasks()
            self.Place()

    def Back(self, event):
        if self.changes:
            bool_var = messagebox.askyesnocancel("Save On Close", "Do you want to save the changes done?")
            if bool_var:
                self.Save(popUp=False)
            elif bool_var==None:
                return
            else: 
                self.changes = False
                self.root.title("Report Card Generator")
                self.root.protocol("WM_DELETE_WINDOW", lambda: Exit(self.root, self.db, self.specs))
                self.specs.Notify("info", "Unsaved changes are lost.", popUp=False)
        self.screen2_1.select()

    def Save(self, event=None, audio=None, popUp=None):
        self.on_focus_lost()
        if self.changes==False: return
        for i in range(len(self.mydata)):
            record = self.table.item(i).get("values")
            roll_no = record[0]
            marks = record[2]
            if   marks=='':       marks = -1
            elif marks=="Absent": marks = -2
            self.db.cursor.execute(f"UPDATE {self.table_name} SET {self.subject}={marks} WHERE Roll_No={roll_no}")
            self.Total(marks, roll_no)
        self.db.cursor.execute("COMMIT")
        self.root.protocol("WM_DELETE_WINDOW", lambda: Exit(self.root, self.db, self.specs))
        self.changes = False
        self.root.title("Report Card Generator")
        self.specs.Notify("info", "Marks are updated in the database.", audio, popUp)

    def SaveOnClose(self):
        if not self.changes:
            self.root.protocol("WM_DELETE_WINDOW", self.SaveAndExit)
            self.changes = True
            self.root.title("*Report Card Generator")

    def SaveAndExit(self):
        bool_var = messagebox.askyesnocancel("Save On Close", "Do you want to save the changes done?")
        if bool_var==None: return
        if bool_var: self.Save(audio=False, popUp=False)
        Exit(self.root, self.db, self.specs)

    def Total(self, marks, roll_no):
        if self.table_name.endswith("sci"):
            idx = Sci_Subs.index(self.subject.replace('_', ' '))
        elif self.table_name.endswith("comm"):
            idx = Comm_Subs.index(self.subject.replace('_', ' '))

        self.db.cursor.execute(f"SELECT * FROM {self.table_name} WHERE {self.subject} IS NOT NULL AND Section='{self.section}' AND Roll_No={roll_no}")
        record = list(self.db.cursor.fetchone())[4:-1]
        record[idx] = marks
        while None in record: record.remove(None)

        total = 0
        for m in record:
            if m == -1:     # -1 means Marks not entered yet therefore no totaling
                total = -1
                break
            elif m == -2:   # -2 means Absent (so 0 marks)
                continue
            else:           # Otherwise marks are added in the total
                total += m  

        self.db.cursor.execute(f"UPDATE {self.table_name} SET TOTAL={total} WHERE Roll_No={roll_no}")

    def BindAll(self):
        self.frame2.bind_all("<Up>", self.MoveUp)
        self.frame2.bind_all("<Down>", self.MoveDown)
        self.frame2.bind_all("<Return>", self.MoveDown)
        self.frame2.bind_all("<Configure>", self.Place)
        self.frame2.bind_all("<MouseWheel>", self.Place)

    def UnbindAll(self):
        self.frame1.unbind_all("<Up>")
        self.frame1.unbind_all("<Down>")
        self.frame1.unbind_all("<Return>")
        self.frame1.unbind_all("<Configure>")
        self.frame1.unbind_all("<MouseWheel>")

    def update_pallete(self, c1, c2, c3, c4):
        for i in (self.frame1, self.heading, self.btn2):
            i["bg"] = c1
        self.style.configure("Treeview.Heading", background=c2)
        self.style.configure("Treeview", background=c4, fieldbackground=c4)
        self.style.map("Treeview", background=[("selected", c3)], foreground=[("selected", "black")])
        self.btn1["bg"] = c2
        Animate(self.btn1)
        self.entry_color = c3
        try: self.entry["bg"] = c3
        except Exception: pass

    def set_values(self, values):
        self.values = values
        self.heading["text"] = f"{values[0]} Examination \nClass - {values[1]} '{values[2]}' \nSubject - {values[3]}"

        # Fetching Records from MySQL database
        self.table_name = GetTableName(*self.values[:-1])
        self.section = values[2]
        self.subject = values[3].replace(' ', '_')
        self.db.cursor.execute(f"SELECT Roll_No, Name, {self.subject} FROM {self.table_name} WHERE {self.subject} IS NOT NULL AND Section='{self.section}' ORDER BY Roll_No")
        self.mydata = self.db.cursor.fetchall()

        # Deleting precious data from table (if any)
        for i in self.table.get_children():
            self.table.delete(i)

        # Adding Data
        for i in range(len(self.mydata)):
            record = self.mydata[i]
            # record = (Roll_No, Name, Marks)
            if record[-1]==-1:
                record = (record[0], record[1], '')
            elif record[-1]==-2:
                record = (record[0], record[1], "Absent")
            self.table.insert(parent='', index="end", iid=i, values=record)
            
    def select(self):
        self.frame1.lift()
        self.frame1.focus()
        self.BindAll()