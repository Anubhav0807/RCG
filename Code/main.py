# REPORT CARD GENERATOR

# Importing my modules
import webbrowser
from udfs import *
from settings import Settings
from student import Screen1
from tabulation import Screen2_1, Screen2_2
from pdf_generator import Screen3
from developer import Dev
from record_generator import RandomGenerator

# Main Window
root = tk.Tk()
screen_width = root.winfo_screenwidth() - 60
screen_height = root.winfo_screenheight() - 120
root.geometry(f"{screen_width}x{screen_height}+30+30")
root.minsize(1000, 500)
root.title("Report Card Generator")
try: root.iconbitmap(resource_path("Assets/Images/icon.ico"))
except Exception: pass

# Closing MySQL server connection before exiting the program
root.protocol("WM_DELETE_WINDOW", lambda: Exit(root, db, specs))

# Updating the whole app's colour at once
def UpdatePallete(*args, change=True):
    global cur_color_index
    if change: cur_color_index += 1
    if cur_color_index>=len(Palettes): cur_color_index = 0
    if args==(): args = Palettes[cur_color_index]
    else: args = args + tuple(["#F0F0F0" for i in range(4-len(args))])
    for screen in (screen0, screen1, screen2_1, screen2_2, screen3, dev):
        screen.update_pallete(*args)
    specs.data["color_idx"] = cur_color_index

# Help - Demo Video
def Help():
    if messagebox.askyesno("Help", "Do you want to watch a Demo Video?"):
        webbrowser.open("https://youtu.be/AyLbTIjUaYM")

# Credits - The most important thing in this App
def Credits():
    messagebox.showinfo("Credits", "Created by Anubhav Jha")


# Home Screen
class Screen0:

    def __init__(self):

        # Frame for the entire screen
        self.frame1 = tk.Frame(root)
        self.frame1.place(x=0, y=0, relwidth=1, relheight=1)

        # Heading Label
        self.heading = tk.Label(self.frame1, text="Main Menu", font="Arial 64 bold")
        self.heading.pack(pady=20)

        # Three button options
        self.btn1 = tk.Button(self.frame1, text="Add New Student", font="Arial 32", relief="ridge", command=self.on_btn1)
        self.btn1.pack(expand=True, fill="both", padx=50, pady=10)
        self.btn2 = tk.Button(self.frame1, text="Add/Edit Marks", font="Arial 32", relief="ridge", command=self.on_btn2)
        self.btn2.pack(expand=True, fill="both", padx=50, pady=10)
        self.btn3 = tk.Button(self.frame1, text="Generate Report Card", font="Arial 32", relief="ridge", command=self.on_btn3)
        self.btn3.pack(expand=True, fill="both", padx=50, pady=10)

    def on_btn1(self):
        if db.con_dict["db"]:
            screen1.select()
        else:
            specs.Notify("warning", "Not connected to any database.")

    def on_btn2(self):
        if db.con_dict["db"]:
            screen2_1.select()
        else:
            specs.Notify("warning", "Not connected to any database.")

    def on_btn3(self):
        if db.con_dict["db"]:
            screen3.select()
        else:
            specs.Notify("warning", "Not connected to any database.")

    def update_pallete(self, c1, c2, c3, c4):
        for i in (self.frame1, self.heading):
            i["bg"] = c1
        for btn in (self.btn1, self.btn2, self.btn3):
            btn["bg"] = c2
            Animate(btn)

    def select(self):
        if screen2_2.changes:
            bool_var = messagebox.askyesnocancel("Save On Close", "Do you want to save the changes done?")
            if bool_var:
                screen2_2.Save(popUp=False)
            elif bool_var==None:
                return
            else: 
                screen2_2.changes = False
                root.title("Report Card Generator")
                root.protocol("WM_DELETE_WINDOW", lambda: Exit(root, db))
                specs.Notify("info", "Unsaved changes are lost.", popUp=False)
        self.frame1.lift()
        self.frame1.focus()
        screen2_2.UnbindAll()
        screen3.UnbindAll()
        dev.UnbindAll()


# Conneting with the MySQL Server
class DB_Connector:

    def __init__(self):
        self.con_dict = {"server":False, "db":False}
        self.Connect(*tuple(specs.data["db"].values()))

    def Connect(self, host, user, passwd, database=None, notify=False):    
        try:
            self.mycon = msc.connect(host=host, user=user, passwd=passwd, database=database)
            self.cursor = self.mycon.cursor()
            if self.mycon.is_connected():
                self.con_dict["server"] = True
                if database: self.con_dict["db"] = True
                else:        self.con_dict["db"] = False
                specs.data["db"] = {"host":host, "user":user, "passwd":passwd, "database":database}
                if notify: specs.Notify("info", "Connection with the Server is established Successfully.")
            else:
                if notify: specs.Notify("error", "Connection Failed.")
        except msc.DatabaseError:
                if notify: specs.Notify("error", "Connection Failed.")

    def CreateTables(self):
        
        # Science Stream
        for exam in ("pmt", "mt", "pq", "q", "r1", "hy", "r2", "pb"):
            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {exam}_12_sci(
            Roll_No smallint UNIQUE,
            UID smallint PRIMARY KEY,
            Name varchar(30),
            Section char,
            Physics tinyint,
            Chemistry tinyint,
            Mathematics tinyint,
            Psychology tinyint,
            English tinyint,
            Computer_Science tinyint,
            Engineering_Graphics tinyint,
            Biology  tinyint,
            TOTAL smallint);
            """)

        # Commerce Stream
        for exam in ("pmt", "mt", "pq", "q", "r1", "hy", "r2", "pb"):
            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {exam}_12_comm(
            Roll_No smallint UNIQUE,
            UID smallint PRIMARY KEY,
            Name varchar(30),
            Section char,
            English tinyint,
            Business_Studies tinyint,
            Economics tinyint,
            Accountancy tinyint,
            Legal_Studies_Maths tinyint,
            Applied_Maths tinyint,
            Entrepreneurship tinyint,
            TOTAL smallint);
            """)


# Creating object of each Screen and ToolWindows
specs = Settings()
db = DB_Connector()

screen0 = Screen0()
screen1 = Screen1(root, specs, db)
screen2_2 = Screen2_2(root, specs, db)
screen2_1 = Screen2_1(root, screen2_2, specs, db)
screen2_2.screen2_1 = screen2_1
screen3 = Screen3(root, specs, db)

generator = RandomGenerator(db)
dev = Dev(root, screen2_2, screen3, specs, db, generator)

# Main Menu to toggle between the screens
main_menu = tk.Menu(root)
main_menu.add_command(label="Home", command=screen0.select)
main_menu.add_command(label="Settings", command=specs.open)
main_menu.add_command(label="Colour", command=UpdatePallete)
main_menu.add_command(label="Help", command=Help)
main_menu.add_command(label="Credits", command=Credits)
root["menu"] = main_menu

# Staring the APP!
screen0.select()
cur_color_index = specs.data["color_idx"]
UpdatePallete(change=False)
specs.Notify("info", "Welcome", popUp=False)
root.mainloop()