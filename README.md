
# Report Card Generator

This app enables the subject teachers to enter the marks of all the students which is then stored in MySQL database. Once the marks are entered, report cards can be generated in the form of pdfs on just one click. The GUI is made using tkinter module. pyttsx3 module is also used to narrate the actions performed.

### Credits:

This RCG App (Report Card Generator) is created by Anubhav Jha.
## Built-In Modules
1. os
2. pickle
3. random
4. sys
5. threading
6. time
7. tkinter
## Non Built-In Modules

1. fpdf 
```bash
    pip install fpdf2
```
2. mysql.connector
```bash
    pip install mysql-connector-python
```
3. pyttsx3
```bash
    pip install pyttsx3
```
## Instructions

1. Run the program named "main.py"
2. To connect to the MySQL Server and select the database you will
   need to access the DEV MODE!
   The DEV MODE can be accessed from anywhere on the window by 
   typing the command "dev" while holding the '\\' key down.
3. The DEV MODE also has a Random Record Generator so that the
   app can be tested without wasting any time on manually inserting
   few record of students for testing purposes.
