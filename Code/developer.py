from udfs import *

# Dev Mode
class Dev:
    
    def __init__(self, root, screen2_2, screen3, specs, db, generator):
        self.root = root
        self.screen2_2 = screen2_2
        self.screen3 = screen3
        self.specs = specs
        self.db = db
        self.generator = generator
        self.cmd = ""
        self.devmode = False
        self.label_list = []
        root.bind("<KeyPress-backslash>", self.on_backslash_press)
        root.bind("<KeyRelease-backslash>", self.on_backslash_release)

        # Frame for the entire screen
        self.frame1 = tk.Frame(root)
        self.frame1.place(x=0, y=0, relwidth=1, relheight=1)

        # Heading (Label)
        self.heading = tk.Label(self.frame1, text="<DEV MODE>", font="Arail 24 bold")
        self.heading.pack(pady=20)

        # Frame for two sub LabelFrames
        self.frame2 = tk.Frame(self.frame1)
        self.frame2.pack(expand=True, fill="both", pady=10)
        self.frame2.grid_columnconfigure(0, weight=1, uniform="group1")
        self.frame2.grid_columnconfigure(1, weight=1, uniform="group1")
        self.frame2.grid_rowconfigure(0, weight=1)

        # TABS for Settings (LabelFrame + Notebook)
        self.frame3 = tk.LabelFrame(self.frame2, text="Settings", font="Arial 24", labelanchor='n', relief="sunken")
        self.frame3.grid(row=0, column=0, sticky="nsew", padx=10)
        self.notebook = ttk.Notebook(self.frame3)
        self.notebook.place(x=0, y=0, relwidth=1, relheight=1)
        self.style = ttk.Style(self.frame3)

        # Cover containg all the current server and database information  and an edit button (Frame)
        self.cover = tk.Frame(self.frame3)
        self.cover.place(x=0, y=0, relwidth=1, relheight=1)
        self.info_label = tk.Label(self.cover, font="Arial 24", justify="left")
        self.info_label.pack(pady=10)

        # Edit Button
        self.edit_btn = tk.Button(self.cover, text="Edit", font="Arial 24", width=6, command=self.ShowSettings)
        self.edit_btn.pack(pady=20)

        # SERVER SETTINGS
        self.server_frame = tk.Frame(self.notebook)
        self.server_frame.pack(expand=True, fill="both")
        self.notebook.add(self.server_frame, text="Server")
        for i in range(3): self.server_frame.columnconfigure(index=i, weight=1)

        # Host
        label = tk.Label(self.server_frame, text="Host:", font="Arial 24", anchor='w')
        label.grid(row=0, column=0, sticky='w', padx=20)
        self.label_list.append(label)
        self.host_entry = tk.Entry(self.server_frame, font="Arial 24", width=12)
        self.host_entry.grid(row=0, column=1, padx=10, pady=20, sticky='we')
        self.host_entry.bind("<Down>", lambda e: self.focus(self.user_entry))
        self.host_entry.bind("<Return>", lambda e: self.focus(self.user_entry))

        # User
        label = tk.Label(self.server_frame, text="User:", font="Arial 24", anchor='w')
        label.grid(row=1, column=0, sticky='w', padx=20)
        self.label_list.append(label)
        self.user_entry = tk.Entry(self.server_frame, font="Arial 24", width=12)
        self.user_entry.grid(row=1, column=1, padx=10, sticky='we')
        self.user_entry.bind("<Up>", lambda e: self.focus(self.host_entry))
        self.user_entry.bind("<Down>", lambda e: self.focus(self.pw_entry))
        self.user_entry.bind("<Return>", lambda e: self.focus(self.pw_entry))

        # Password
        label = tk.Label(self.server_frame, text="Password:", font="Arial 24", anchor='w')
        label.grid(row=2, column=0, sticky='w', padx=20)
        self.label_list.append(label)
        self.pw_entry = tk.Entry(self.server_frame, font="Arial 24", width=12)
        self.pw_entry.grid(row=2, column=1, padx=10, pady=20, sticky='we')
        self.pw_entry.bind("<Up>", lambda e: self.focus(self.user_entry))
        self.pw_entry.bind("<Return>", self.Connect)

        # Connect Button
        self.con_btn = tk.Button(self.server_frame, text="Connect", font="Arial 24", state="disable", command=self.Connect)
        self.con_btn.grid(row=3, column=0, columnspan=3, pady=20)

        # DATABASE SETTINGS
        self.db_frame = tk.Frame(self.notebook)
        self.db_frame.pack(expand=True, fill="both")
        self.notebook.add(self.db_frame, text="Database")
        for i in range(3): self.db_frame.columnconfigure(index=i, weight=1)
        label = tk.Label(self.db_frame, font="Arial 18")
        label.grid(row=0, column=0)
        self.label_list.append(label)

        # Database Name
        label = tk.Label(self.db_frame, text="Database Name:", font="Arial 24")
        label.grid(row=1, column=0, columnspan=3, sticky='w', padx=20)
        self.label_list.append(label)
        self.db_name_entry = tk.Entry(self.db_frame, font="Arial 32 bold", justify="center")
        self.db_name_entry.grid(row=2, column=0, columnspan=3, sticky='we', padx=80, pady=20)
        self.db_name_entry.bind("<Return>", self.SelectDB)

        # Create New Database
        self.create_btn = tk.Button(self.db_frame, text="Create", font="Arial 24", state="disable", command=self.CreateDB)
        self.create_btn.grid(row=3, column=0, pady=20)

        # Select Database
        self.select_btn = tk.Button(self.db_frame, text="Select", font="Arial 24", state="disable", command=self.SelectDB)
        self.select_btn.grid(row=3, column=1)

        # Delete Database
        self.del_btn = tk.Button(self.db_frame, text="Delete", font="Arial 24", state="disable", command=self.DeleteDB)
        self.del_btn.grid(row=3, column=2)
        
        # RANDOM RECORD GENERATOR (LabelFrame)
        self.frame4 = tk.LabelFrame(self.frame2, text="Random Records", font="Arial 24", labelanchor='n', relief="sunken")
        self.frame4.grid(row=0, column=1, sticky="nsew", padx=10)
        self.frame4.columnconfigure(index=0, weight=1)
        self.frame4.columnconfigure(index=1, weight=1)
        label = tk.Label(self.frame4, font="Arial 18")
        label.grid(row=0, column=0)
        self.label_list.append(label)

        # Class
        label = tk.Label(self.frame4, text="Class:", font="Arial 24", anchor='w')
        label.grid(row=1, column=0, padx=20, pady=10, sticky='we')
        self.label_list.append(label)
        self.clas = tk.StringVar(self.frame4)
        self.clas_dropdown = tk.OptionMenu(self.frame4, self.clas, "XII", command=self.EnableGenBtn)
        self.clas_dropdown.grid(row=1, column=1, padx=20, sticky='we')
        self.clas_dropdown.config(width=12, font="Arial 24", relief='ridge')
        menu = root.nametowidget(self.clas_dropdown.menuname)
        menu.config(font="Arial 18")

        # Stream
        label = tk.Label(self.frame4, text="Stream:", font="Arial 24", anchor='w')
        label.grid(row=2, column=0, padx=20, pady=10, sticky='we')
        self.label_list.append(label)
        self.stream = tk.StringVar(self.frame4)
        self.stream_dropdown = tk.OptionMenu(self.frame4, self.stream, "Science", "Commerce", command=self.EnableGenBtn)
        self.stream_dropdown.grid(row=2, column=1, padx=20, pady=20, sticky='we')
        self.stream_dropdown.config(width=12, font="Arial 24", relief='ridge')
        menu = self.root.nametowidget(self.stream_dropdown.menuname)
        menu.config(font="Arial 18")

        # Number of students per section
        label = tk.Label(self.frame4, text="Number:", font="Arial 24", anchor='sw')
        label.grid(row=3, column=0, padx=20, sticky='we')
        self.label_list.append(label)
        label = tk.Label(self.frame4, text="    (0 to 99)", font="Arial 14", anchor='nw')
        label.grid(row=4, column=0, padx=20, sticky='we')
        self.label_list.append(label)
        self.n = tk.IntVar(self.frame4)
        self.n.initialize(40)
        self.n_entry = tk.Entry(self.frame4, textvariable=self.n, font="Arial 24", justify="center", width=12)
        self.n_entry.grid(row=3, column=1, padx=20, pady=10, sticky='nwe', rowspan=2)

        # Checkbutton to toggle generate random marks or not
        self.frame5 = tk.Frame(self.frame4)
        self.frame5.grid(row=5, column=0, columnspan=2)
        self.marks = tk.IntVar(self.frame5)
        self.check_btn = tk.Checkbutton(self.frame5, variable=self.marks)
        self.check_btn.pack(side="left")
        label = tk.Label(self.frame5, text="Generate Random Marks as well", font="Arial 18")
        label.pack(side="left")
        self.label_list.append(label)

        # Generate Button
        self.gen_btn = tk.Button(self.frame4, text="Generate", font="Arial 24", state="disable", command=self.Generate)
        self.gen_btn.grid(row=6, column=0, columnspan=2, pady=20)

    def on_backslash_press(self, event):
        if not self.devmode:
            self.devmode = True
            self.root.bind("<Key>", self.on_Key)

    def on_backslash_release(self, event):
        self.root.unbind("<Key>")
        self.devmode = False
        if self.cmd.lower() == "dev": self.select()
        self.cmd = ""

    def on_Key(self, event):
        if self.devmode and not event.keycode == 220:    # 220 keycode is for backslash:
            try:
                self.cmd += event.char
            except AttributeError:
                pass

    def BindAll(self):
        self.root.bind_all("<Key>", self.EnableGenBtn, add='+')
        self.root.bind_all("<Key>", self.EnableConBtn, add='+')
        self.root.bind_all("<Key>", self.Enable3Btns, add='+')

    def UnbindAll(self):
        self.root.unbind_all("<Key>")

    def ShowInfo(self):
        if self.db.con_dict["server"]:
            self.frame3["text"] = "Curent Status"
            host = self.specs.data["db"]["host"]
            user = self.specs.data["db"]["user"]
            database = self.specs.data["db"]["database"]
            if not self.db.con_dict["db"]: database = "Not selected"
            self.info_label["text"] = f"\nHost: {host}\n\nUser: {user}\n\nDatabase: {database}"
            self.cover.lift()
        else:
            self.frame3["text"] = "Settings"
            self.notebook.lift()

    def ShowSettings(self):
        self.frame3["text"] = "Settings"
        self.notebook.lift()

    def EnableGenBtn(self, value):
        if self.clas.get() and self.stream.get() and self.isValid():
            if self.gen_btn["state"] == "disabled":
                self.gen_btn["state"] = "normal"
                Animate(self.gen_btn)
        elif self.gen_btn["state"] != "disabled":
            self.gen_btn["state"] = "disable"
            InAnimate(self.gen_btn)
            self.update_pallete(*self.colors)

    def EnableConBtn(self, value):
        if self.host_entry.get() and self.user_entry.get() and self.pw_entry.get():
            if self.con_btn["state"] == "disabled":
                self.con_btn["state"] = "normal"
                Animate(self.con_btn)
        elif self.con_btn["state"] != "disabled":
            self.con_btn["state"] = "disable"
            InAnimate(self.con_btn)
            self.update_pallete(*self.colors)

    def Enable3Btns(self, value):
        if self.db_name_entry.get():
            for btn in (self.create_btn, self.select_btn, self.del_btn):
                if btn["state"] == "disabled":
                    btn["state"] = "normal"
                    Animate(btn)
        else:
            for btn in (self.create_btn, self.select_btn, self.del_btn):
                if btn["state"] != "disabled":
                    btn["state"] = "disable"
                    InAnimate(btn)

    def Connect(self, event=None):
        self.db.Connect(self.host_entry.get(), self.user_entry.get(), self.pw_entry.get(), notify=True)

    def CreateDB(self):
        db_name = self.db_name_entry.get().title()
        if not self.db.con_dict["server"]:
            self.specs.Notify("error", "Not connected to the Server.")
            return
        try:
            self.db.cursor.execute(f"CREATE DATABASE {db_name}")
            self.specs.Notify("info", f"{db_name} database is Created and Selected.")
        except msc.errors.DatabaseError:
            self.specs.Notify("error", f"{db_name} database already exists.")
        finally:
            self.db.cursor.execute(f"USE {db_name}")
            self.db.CreateTables()
            self.db.con_dict["db"] = True
            self.specs.data["db"]["database"] = db_name

    def SelectDB(self, event=None):
        db_name = self.db_name_entry.get().title()
        if not self.db.con_dict["server"]:
            self.specs.Notify("error", "Not connected to the Server.")
            return
        try:
            self.db.cursor.execute(f"USE {db_name}")
            self.db.con_dict["db"] = True
            self.specs.data["db"]["database"] = db_name
            self.specs.Notify("info", f"{db_name} database is Selected.")
        except msc.errors.DatabaseError:
            self.specs.Notify("error", f"{db_name} database is not available.")

    def DeleteDB(self):
        db_name = self.db_name_entry.get().title()
        if not self.db.con_dict["server"]:
            self.specs.Notify("error", "Not connected to the Server.")
            return
        try:
            self.db.cursor.execute(f"DROP DATABASE {db_name}")
            self.specs.Notify("info", f"{db_name} database is Deleted.")
        except msc.errors.DatabaseError:
            self.specs.Notify("error", f"{db_name} database is not available.")

    def focus(self, entry):
        entry.focus()
        entry.select_range(0, 'end')
        entry.icursor('end')

    def isValid(self):
        try:
            return 0 <= self.n.get() < 100
        except:
            return False

    def Generate(self):
        if not self.db.con_dict["db"]:
            self.specs.Notify("error", "Not connected to the Database.")
            return
        clas = self.clas.get()
        match self.stream.get():
            case "Science":
                stream = "sci"
            case "Commerce":
                stream = "comm"
        n = self.n.get()
        filled = self.marks.get()

        # Check if the tables are already filled
        self.db.cursor.execute(f"SELECT COUNT(*) FROM pmt_12_{stream}")
        if self.db.cursor.fetchone()[0]==0:
            self.generator.Create(clas, stream, n, filled)
            self.specs.Notify("info", f"{n} random records are generated for each section of {self.stream.get()} Stream.")
        else:
            self.specs.Notify("error", "Tables are already filled.")

    def update_pallete(self, c1, c2, c3, c4):
        for i in (self.frame1, self.heading, self.frame2, self.frame3, self.frame4, self.frame5, self.server_frame, self.db_frame, self.cover,*self.label_list, self.info_label):
            i["bg"] = c1
        for i in (self.clas_dropdown, self.stream_dropdown, self.n_entry, self.host_entry, self.user_entry, self.pw_entry, self.db_name_entry):
            i["bg"] = c3
        for btn in (self.gen_btn, self.con_btn, self.select_btn, self.create_btn, self.del_btn, self.edit_btn):
            btn["bg"] = c2
            Animate(btn)
        self.style.configure('TNotebook.Tab', background=c2, font="Arial 18")
        self.style.configure('TNotebook', background=c1)
        self.style.map("TNotebook.Tab", background= [("selected", c2)])
        self.check_btn["bg"] = c4
        self.colors = (c1, c2, c3, c4)

    def select(self):
        if self.screen2_2.changes:
            bool_var = messagebox.askyesnocancel("Save On Close", "Do you want to save the changes done?")
            if bool_var:
                self.screen2_2.Save(popUp=False)
            elif bool_var==None:
                return
            else: 
                self.screen2_2.changes = False
                self.root.title("Report Card Generator")
                self.root.protocol("WM_DELETE_WINDOW", lambda: Exit(self.root, self.db))
                self.specs.Notify("info", "Unsaved changes are lost.", popUp=False)
        self.frame1.lift()
        self.frame1.focus()
        self.ShowInfo()
        self.screen2_2.UnbindAll()
        self.screen3.UnbindAll()
        self.BindAll()