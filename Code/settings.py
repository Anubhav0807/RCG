# SETTINGS

# Importing Modules
from udfs import *
import pickle
import threading
from time import sleep
try:
    import pyttsx3
except ModuleNotFoundError:
    messagebox.showwarning("Module Not Found", "Module named pyttsx3 was not found. \nGo to the command prompt and run the command: \npip install pyttsx3")
    quit()


# Audio
engine = pyttsx3.init()
voices = engine.getProperty("voices")


class Settings:

    def __init__(self):
        # Fetching the previous data from data.dat file
        try:
            with open("Data/data.dat", "rb") as f:
                self.data = pickle.load(f)
            self.data["db"]["passwd"] = self.decrypt(self.data["db"]["passwd"])
        except Exception:
            self.data = {
                    "notify":(True, True), 
                    "properties":{"voice":1, "rate":150, "volume":100}, 
                    "db":{"host":"", "user":"", "passwd":"", "database":None},
                    "path":"",
                    "color_idx":0
                }
        finally:
            self.temp_data = self.data.copy()
            self.audio, self.popUp = self.data["notify"]
            self.property = self.data["properties"]
            self.set_properties()
    
    def open(self):
        try:
            # Focusing the tool window if it already exists
            self.win.focus()
        except Exception:

            # Creating a tool window
            if __name__=="__main__":
                self.win = tk.Tk()  
            else:
                self.win = tk.Toplevel()
                self.win.attributes("-toolwindow", True)
                
            self.win.title("Settings")
            self.win.geometry("400x500+60+80")
            self.win.resizable(False, False)
            self.win.bind("<Escape>", lambda e: self.win.destroy())
            self.win.focus()

            # FRAME 1
            self.frame1 = tk.Frame(self.win)
            self.frame1.place(x=0, y=0, relwidth=1, relheight=1)
            for i in range(4): self.frame1.columnconfigure(index=i, weight=1)

            # Notification type
            tk.Label(self.frame1, text="Notification type:", font="Arial 16", anchor='w').grid(row=0, column=0, columnspan=4, sticky='we', padx=20, pady=10)

            self.audio_var = tk.BooleanVar(self.win)
            check_btn1 = tk.Checkbutton(self.frame1, anchor='e', variable=self.audio_var)
            check_btn1.grid(row=1, column=0, sticky='we')
            if self.audio: check_btn1.select()
            tk.Label(self.frame1, text="Audio", font="Arial 14", anchor='w').grid(row=1, column=1, sticky='we')

            self.popUp_var = tk.BooleanVar(self.win)
            check_btn2 = tk.Checkbutton(self.frame1, anchor='e', variable=self.popUp_var)
            check_btn2.grid(row=1, column=2, sticky='we')
            if self.popUp: check_btn2.select()
            tk.Label(self.frame1, text="Pop Up", font="Arial 14", anchor='w').grid(row=1, column=3, sticky='we')

            # Radio buttons to choose gender of audio
            tk.Label(self.frame1, text="\nAudio Gender:", font="Arial 16", anchor='w').grid(row=2, column=0, columnspan=4, sticky='we', padx=20, pady=10)
            self.gender_var = tk.IntVar(self.win)
            self.gender_var.initialize(self.property["voice"])

            r1 = tk.Radiobutton(self.frame1, anchor='e', variable=self.gender_var, value=0) # 0-male
            r1.grid(row=3, column=0, sticky='we')
            tk.Label(self.frame1, text="Male", font="Arial 14", anchor='w').grid(row=3, column=1, sticky='we')

            r2 = tk.Radiobutton(self.frame1, anchor='e', variable=self.gender_var, value=1) # 1-female
            r2.grid(row=3, column=2, sticky='we')
            tk.Label(self.frame1, text="Female", font="Arial 14", anchor='w').grid(row=3, column=3, sticky='we')

            # Slider to specify WPM (words per minute)
            tk.Label(self.frame1, text="\n\nSpeed (WPM):", font="Arial 16", anchor='w').grid(row=4, column=0, columnspan=4, sticky='we', padx=20)
            self.rate_var = tk.IntVar(self.win)
            wpm_slider = tk.Scale(self.frame1, length=400, width=10, from_=0, to=400,  orient='horizontal', tickinterval=50, variable=self.rate_var)
            wpm_slider.grid(row=5, column=0, columnspan=4, padx=10)
            wpm_slider.set(self.property["rate"])

            # Slider to change the volume of audio
            tk.Label(self.frame1, text="\nVolume:", font="Arial 16", anchor='w').grid(row=6, column=0, columnspan=4, sticky='we', padx=20)
            self.vol_var = tk.IntVar(self.win)
            vol_slider = tk.Scale(self.frame1, length=400, width=10, from_=0, to=100,  orient='horizontal', tickinterval=10, variable=self.vol_var)
            vol_slider.grid(row=7, column=0, columnspan=4, padx=10)
            vol_slider.set(self.property["volume"])

            # Button to apply the changes
            apply_btn = tk.Button(self.frame1, text="Apply", font="Arial 14", command=self.apply)
            apply_btn.grid(row=8, column=2, columnspan=2, sticky='we', padx=20, pady=20)
            Animate(apply_btn)

            # Button to navigate to Frame 2
            test_btn = tk.Button(self.frame1, text="Test", font="Arial 14", command=self.test)
            test_btn.grid(row=8, column=0, columnspan=2, sticky='we', padx=20, pady=20)
            Animate(test_btn)
            
            # FRAME 2
            self.frame2 = tk.Frame(self.win)
            self.frame2.place(x=0, y=0, relwidth=1, relheight=1)

            # Button to navigate to Frame 1
            back_btn = tk.Button(self.frame2, text="Back", font="Arial 14", command=self.back)
            back_btn.pack(padx=10, pady=10, anchor='w')
            Animate(back_btn)

            # Button to play the audio
            play_btn = tk.Button(self.frame2, text="Play", font="Arial 14", command=self.play)
            play_btn.pack(side="bottom", pady=10)
            Animate(play_btn)

            # Test the audio by saying some text given by the user
            tk.Label(self.frame2, text="Enter some text to test the audio:", font="Arial 16").pack(padx=10, anchor='w')
            self.text = tk.Text(self.frame2, font="Arial 14")
            self.text.insert("end", "Hello World!")
            self.text.pack(padx=10, pady=10)

            self.frame1.lift()
            if __name__=="__main__": self.win.mainloop()

    def apply(self):
        self.audio, self.popUp = self.audio_var.get(), self.popUp_var.get()
        self.property = {"voice":self.gender_var.get(), "rate":self.rate_var.get(), "volume":self.vol_var.get()}
        self.data["notify"] = self.audio, self.popUp
        self.data["properties"] = self.property
        self.set_properties()
        self.save_data()
        self.win.destroy()

    def test(self):
        self.frame2.lift()
    
    def back(self):
        self.frame1.lift()

    def play(self):
        global thread
        engine.setProperty("voice", voices[self.gender_var.get()].id)
        engine.setProperty("rate", self.rate_var.get())
        engine.setProperty("volume", self.vol_var.get()/100)
        try:
            if not thread.is_alive():
                engine.say(self.text.get("1.0","end-1c"))
                thread = threading.Thread(target=self.say_and_goto_past)
                thread.start()
        except NameError:
            engine.say(self.text.get("1.0","end-1c"))
            thread = threading.Thread(target=self.say_and_goto_past)
            thread.start()

    def say_and_goto_past(self):
        engine.runAndWait()
        self.set_properties()

    def set_properties(self):
        engine.setProperty("voice", voices[self.property["voice"]].id)
        engine.setProperty("rate", self.property["rate"])
        engine.setProperty("volume", self.property["volume"]/100)   # Volume should be between 0 and 1

    def save_data(self):
        self.data["db"]["passwd"] = self.encrypt(self.data["db"]["passwd"])
        with open("Data/data.dat", "wb") as f:
            pickle.dump(self.data, f)
        self.data["db"]["passwd"] = self.decrypt(self.data["db"]["passwd"])

    def encrypt(self, pw_str):
        pw_list = []
        for i in pw_str:
            pw_list.append(ord(i))
        return pw_list

    def decrypt(self, pw_list):
        pw_str = ""
        for i in pw_list:
            pw_str += chr(i)
        return pw_str

    def Notify(self, category, msg, audio=None, popUp=None):
        global thread

        if audio==None: audio=self.audio
        if popUp==None: popUp=self.popUp

        if audio:
            delay = 1 if popUp else 0
            try:
                if not thread.is_alive():
                    engine.say(msg)
                    thread = threading.Thread(target= lambda: self.DelayStart(engine.runAndWait, delay))
                    thread.start()
            except NameError:
                engine.say(msg)
                thread = threading.Thread(target= lambda: self.DelayStart(engine.runAndWait, delay))
                thread.start()

        if popUp:
            match category:
                case "info":
                    messagebox.showinfo("Notification", msg)
                case "error":
                    messagebox.showerror("Error", msg)
                case "warning":
                    messagebox.showwarning("Warning", msg)

    def DelayStart(self, func, time):
        sleep(time)
        try: func()
        except RuntimeError: pass


if __name__=="__main__":
    specs = Settings()
    specs.open()