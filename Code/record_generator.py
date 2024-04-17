# RECORD GENERATOR for MySQL
from udfs import *
from random import randint

# There are 100 male names followed by 100 female names
FirstNames = ['Aaditya', 'Aarya', 'Abhay', 'Abhijeet', 'Abhinandan', 'Abhinay', 'Abhishek', 'Abimanyu', 'Aditya', 'Akhil', 'Akshat', 'Anil', 'Avi', 'Balaraam', 'Bharat', 'Bhaskar', 'Bhaumik', 'Bijay', 'Brijesh', 'Chandan', 'Chetan', 'Chirag', 'Chiranjeeve', 'Daksh', 'Daman', 'Depen', 'Dev', 'Dhruv', 'Divyanshu', 'Ekambar', 'Ekansh', 'Ekaraj', 'Eklavya', 'Elilarasan', 'Falak', 'Gagan', 'Gajendra', 'Garv', 'Gaurav', 'Gautam', 'Hardik', 'Harsh', 'Hemant', 'Hridaya', 'Indivar', 'Indra', 'Indraneel', 'Ishaan', 'Ishwar', 'Jai', 'Jaideep', 'Jatindra', 'Jayant', 'Kabir', 'Kamal', 'Kanha', 'Kartik', 'Kush', 'Lakhan', 'Lakshya', 'Lingam', 'Madhu', 'Manas', 'Manav', 'Mayank', 'Mihir', 'Milind', 'Nakul', 'Nikhil', 'Nischay', 'Nitish', 'Ojas', 'Om', 'Palash', 'Paras', 'Piyush', 'Pushkal', 'Rachit', 'Rahul', 'Rajan', 'Rajesh', 'Ranganathan', 'Ravi', 'Rohit', 'Sachin', 'Sahil', 'Sajan', 'Sameer', 'Satya', 'Saumil', 'Saurav', 'Tanish', 'Tanmay', 'Tejas', 'Tushar', 'Ujjwal', 'Vasu', 'Vidit', 'Vijay', 'Vishvas', 'Aahna', 'Aarzoo', 'Akriti', 'Ananya', 'Anmol', 'Avani', 'Babita', 'Bhaagyasree', 'Bhanu', 'Bharati', 'Bhoomi', 'Chahat', 'Charu', 'Chetna', 'Chhavi', 'Chhaya', 'Damini', 'Darpana', 'Deepal', 'Dipti', 'Divya', 'Ekaja', 'Ekanshi', 'Ekta', 'Ena', 'Esha', 'Falguni', 'Gargi', 'Garima', 'Garvita', 'Gehna', 'Gunjan', 'Heena', 'Hema', 'Hetal', 'Himani', 'Indira', 'Ira', 'Isha', 'Ishika', 'Ishita', 'Jagriti', 'Janhavi', 'Jhalak', 'Jiya', 'Juhi', 'Kaajal', 'Kaavya', 'Kanak', 'Kanika', 'Karishma', 'Kashish', 'Khushi', 'Kinjal', 'Kirti', 'Komal', 'Koyal', 'Kshipra', 'Latika', 'Laveena', 'Lavleen', 'Lipi', 'Lipika', 'Madhuri', 'Mallika', 'Mansi', 'Mayuari', 'Mehar', 'Mridul', 'Naina', 'Nandini', 'Neeta', 'Neharika', 'Nidhi', 'Niyati', 'Nupur', 'Ojaswini', 'Palak', 'Pallavi', 'Pari', 'Prajakta', 'Pratibha', 'Praveen', 'Preeti', 'Prerena', 'Priya', 'Raakhi', 'Raashi', 'Radha', 'Ragini', 'Rajni', 'Riya', 'Ruhi', 'Sachi', 'Saloni', 'Sejal', 'Shagun', 'Shefali', 'Shilpa', 'Vasudha']

# There are 100 Surnames
LastNames = ['Acharya', 'Agarwal', 'Khatri', 'Ahuja', 'Anand', 'Laghari', 'Patel', 'Reddy', 'Bakshi', 'Anthony', 'Babu', 'Arya', 'Balakrishnan', 'Banerjee', 'Burman', 'Bhatt', 'Basu', 'Bedi', 'Varma', 'Dara', 'Dalal', 'Chowdhury', 'Chabra', 'Chadha', 'Chakrabarti', 'Chawla', 'Ahluwalia', 'Amin', 'Apte', 'Datta', 'Deol', 'Deshpande', 'Dewan', 'Lal', 'Kohli', 'Mangal', 'Malhotra', 'Jha', 'Joshi', 'Kapadia', 'Iyer', 'Jain', 'Khanna', 'Grover', 'Kaur', 'Kashyap', 'Gokhale', 'Ghosh', 'Garg', 'Dhar', 'Gandhi', 'Ganguly', 'Gupta', 'Das', 'Chopra', 'Dhawan', 'Dixit', 'Dubey', 'Haldar', 'Kapoor', 'Khurana', 'Kulkarni', 'Madan', 'Bajwa', 'Bhasin', 'Chandra', 'Chauhan', 'Deshmukh', 'Dayal', 'Dhillon', 'Goswami', 'Goel', 'Mallick', 'Mahajan', 'Kumar', 'Mani', 'Gill', 'Mannan', 'Biswas', 'Batra', 'Bawa', 'Mehta', 'Mukherjee', 'Saxena', 'Zacharia', 'Shah', 'Ray', 'Rao', 'Purohit', 'Parekh', 'Thakur', 'Singh', 'Sharma', 'Seth', 'Sachdev', 'Ranganathan', 'Puri', 'Pandey', 'Naidu', 'Modi']

class RandomGenerator:

    def __init__(self, db):
        self.db = db

    def Fname(self, gender=None):
        """
        Takes gender as argument (optional)
        Returns a random First name
        """    
        if gender==None:
            return FirstNames[randint(0, 199)]
        elif gender.lower() in ('m', 'male'):
            return FirstNames[randint(0, 99)]
        elif gender.lower() in ('f', 'female'):
            return FirstNames[randint(100, 199)]

    def Lname(self):
        "Returns a random Last name"
        return LastNames[randint(0,99)]

    def Name(self, gender=None):
        """
        Takes gender as argument (optional)
        Returns a random Name
        """    
        return self.Fname(gender) +' '+ self.Lname()

    def get_name_list(self, n, gender=None):
        """
        Takes number of names (compulsory) and gender (optional) as argument 
        Returns a list of random Names
        """
        lst = []
        for i in range(n):
            lst.append(self.Name(gender))
        return lst

    def GrantSubjects(self, stream):
        lst = []

        if stream=="sci":

            lst.append(-1)                           # Physics
            lst.append(-1)                           # Chemistry
            lst.append(-1)                           # English
            if randint(0,1):
                lst.append(-1)                       # Mathematics
                lst.append("NULL")                   # Psychology
            else:
                lst.append("NULL")                   # Mathematics
                lst.append(-1)                       # Psychology 

            match randint(1,3):
                case 1:
                    lst.append(-1)                   # Computer Science
                    lst.append("NULL")               # Biology
                    lst.append("NULL")               # Engineering Graphics
                case 2:
                    lst.append("NULL")               # Computer Science
                    lst.append(-1)                   # Biology
                    lst.append("NULL")               # Engineering Graphics
                case 3:
                    lst.append("NULL")               # Computer Science
                    lst.append("NULL")               # Biology
                    lst.append(-1)                   # Engineering Graphics

        elif stream=="comm":

            lst.append(-1)                           # Business Studies
            lst.append(-1)                           # Accountancy
            lst.append(-1)                           # Economics
            lst.append(-1)                           # English

            match randint(1,3):
                case 1:
                    lst.append(-1)                   # Applied Mathematics
                    lst.append("NULL")               # Entrepreneurship
                    lst.append("NULL")               # Legal Studies
                case 2:
                    lst.append("NULL")               # Applied Mathematics
                    lst.append(-1)                   # Entrepreneurship
                    lst.append("NULL")               # Legal Studies
                case 3:
                    lst.append("NULL")               # Applied Mathematics
                    lst.append("NULL")               # Entrepreneurship
                    lst.append(-1)                   # Legal Studies

        return tuple(lst)

    def SubjectMarks(self, subjects):
        lst = []
        for sub in subjects:
            if sub == -1:
                lst.append(randint(0, 100))
            else:
                lst.append("NULL")
        return tuple(lst)

    def get_UID(self):
        "Extracts the previous UID from both the stream and Returns the next UID"
        self.db.cursor.execute("SELECT MAX(UID) FROM pmt_12_sci")
        max1 = self.db.cursor.fetchone()[0]
        if max1==None: max1 = 10000
        self.db.cursor.execute("SELECT MAX(UID) FROM pmt_12_comm")
        max2 = self.db.cursor.fetchone()[0]
        if max2==None: max2 = 10000
        return max(max1, max2)+1

    def get_rno(self, stream, clas, old_rno, n):
        "Returns the next roll number in the form CCSRR-ClassClassSectionRnoRno"
        
        if n not in range(100): raise RuntimeError("The number of Students can not be more that 99.")
        if clas in RomanToNum: clas = RomanToNum[clas]
        if old_rno==None:
            rno = 1
        else:
            rno = int(str(old_rno)[-2:])
            if rno==n:
                self.update_sec(stream)
                rno = 1
                if self.sec==None:
                    return
            else:
                rno += 1
        rno = str(rno)
        if len(rno)<2: rno = '0'+rno
        new_rno = clas+str(ord(self.sec.lower())-96)+rno
        return int(new_rno)

    def update_sec(self, stream):
        if stream.lower()=="sci":
            match self.sec:
                case None: self.sec = 'A'
                case 'A':  self.sec = 'B'
                case 'B':  self.sec = 'C'
                case 'C':  self.sec = 'D'
                case 'D':  self.sec = None
        elif stream.lower()=="comm":
            match self.sec:
                case None: self.sec = 'E'
                case 'E':  self.sec = 'F'
                case 'F':  self.sec = None

    def TotalMarks(self, subject_marks):
        total = 0
        for m in subject_marks:
            if m == "NULL": continue
            if m == -1: return -1
            total += m
        return total

    def Create(self, clas, stream, n, filled):
        if n not in range(100): raise RuntimeError("The number of Students can not be more that 99.")
        Name_list = self.get_name_list(4*n, "male")
        Subject_list = [self.GrantSubjects(stream) for i in range(4*n)]
        UID = self.get_UID()
        for exam in Exams:
            self.sec = None
            self.update_sec(stream)
            rno = self.get_rno(stream, clas, None, n)
            uid = UID
            i = 0
            table_name = GetTableName(exam, clas, self.sec)
            while self.sec:
                if filled: subject_marks = self.SubjectMarks(Subject_list[i])
                else:      subject_marks = Subject_list[i]
                values = (rno, uid, Name_list[i], self.sec) + subject_marks + (self.TotalMarks(subject_marks),)
                query = f"INSERT INTO {table_name} VALUES {values}".replace("'NULL'", "NULL")
                # print(query)
                self.db.cursor.execute(query)
                rno = self.get_rno(stream, clas, rno, n)
                uid += 1
                i += 1
        self.db.cursor.execute("COMMIT")
