import os 
import datetime
import hashlib

# --- PATHS FOR RELATIONAL DATA ---

#For PAULO and INDAH: Use these paths for any manual file reading/writing
#define the folder for the database
db_folder = 'database'
#define the file path for all database files, using os.path.join for better compatibility across different operating systems
students_path = os.path.join(db_folder, 'students.txt')
attendance_path = os.path.join(db_folder, 'attendance.txt')
users_path = os.path.join(db_folder, 'users.txt')
courses_path = os.path.join(db_folder, 'courses.txt')
teachers_path = os.path.join(db_folder, 'teachers.txt')
enrollments_path = os.path.join(db_folder, 'enrollments.txt')

#setup the database with initial files and sample data if they don't exist. This function is called at the end of this script to ensure the environment is ready before any UI interactions.
def setup_database():
    #create a directory for the database if it doesn't exist
    if not os.path.exists(db_folder):
        try: 
            os.makedirs(db_folder)
            print(f"Created database folder: {db_folder}")
        except Exception as e:
            print(f"Error creating database folder: {e}")
            return
    #setup the students.txt file with sample data if it doesn't exist. This file is important for both the registration process and for populating the student dropdown in the Teacher UI when marking attendance.
    if not os.path.exists(students_path):
        try:
            #format: StudentID, Name
            sample_students = [
                "1, Alice Smith\n",
                "2, Bob Jones\n",
                "3, Charlie Brown\n"
            ]
            with open(students_path, 'w') as f:
                f.writelines(sample_students)
            print(f"Initialized: {students_path} with sample data.")
        except Exception as e:
            print(f"Failed to create students file: {e}")

    #setup the attendance.txt file with sample data if it doesn't exist. This file is important for Task 4 where we need to display attendance records based on filters. By pre-populating it with some records, we can test the filtering functionality without needing to first mark attendance through the UI.
    if not os.path.exists(attendance_path):
        try:
            #format: Date, CourseID, StudentID, Status[P/A]
            sample_attendance = [
                "16-05-2025, ICT105, 1, P\n",
                "16-05-2025, ICT105, 2, P\n",
                "16-05-2025, ICT105, 3, A\n"
            ]
            with open(attendance_path, 'w') as f:
                f.writelines(sample_attendance)
            print(f"Initialized: {attendance_path} with sample data.")
        except Exception as e:
            print(f"Failed to create attendance file: {e}")
         
    #setup the users.txt file with sample data if it doesn't exist. This file is important for the login functionality in both Teacher and Student UIs.
    if not os.path.exists(users_path):
        try:
            #we hash the passwords before saving them! 
            #format: Username, Password(saved in hash), Role[Teacher/Student]
            sample_users = [
                f"T101, {hash_password('teacher123')}, Teacher\n",
                f"student1, {hash_password('student123')}, Student\n"
            ]
            with open(users_path, 'w') as f:
                f.writelines(sample_users)
        except Exception as e:
            print(f"Failed to create users file: {e}")

    #setup the courses.txt file with sample data if it doesn't exist. This file is important for populating the course dropdown in the Teacher UI when marking attendance.
    if not os.path.exists(courses_path):
        try:
            # Format: CourseID, CourseName
            sample_courses = [
                "ICT105, Programming Principles\n",
                "MAT101, Discrete Mathematics\n",
                "DAT200, Database Systems\n"
            ]
            with open(courses_path, 'w') as f:
                f.writelines(sample_courses)
            print(f"Initialized: {courses_path}")
        except Exception as e:
            print(f"Failed to create courses file: {e}")

    #setup the teachers.txt file with sample data if it doesn't exist. This file is important for linking courses to teachers in the enrollment process.
    if not os.path.exists(teachers_path):
        try:
            # Format: TeacherID, Name
            sample_teachers = ["T101, Dr. Smith\n", "T102, Prof. Jones\n"]
            with open(teachers_path, 'w') as f:
                f.writelines(sample_teachers)
        except Exception as e:
            print(f"Failed to create teachers file: {e}")

    # setup Enrollments file with sample data if it doesn't exist. This file links students to courses and teachers, which is essential for the attendance marking process.
    if not os.path.exists(enrollments_path):
        try:
            #format: CourseID, TeacherID, StudentID
            sample_enrollments = [
                "ICT105, T101, 1\n", # Alice is with Dr. Smith in ICT105
                "ICT105, T101, 2\n", # Bob is with Dr. Smith in ICT105
                "MAT101, T102, 3\n"  # Charlie is with Prof. Jones in MAT101
            ]
            with open(enrollments_path, 'w') as f:
                f.writelines(sample_enrollments)
        except Exception as e:
            print(f"Failed to create enrollments file: {e}")


# --- SECURITY & UTILITY ---


#function to hash passwords using SHA-256. This ensures that we never store plain text passwords in our users.txt file, enhancing security.
def hash_password(password):
    #creates a secure SHA-256 hash of a password string.
    return hashlib.sha256(password.encode()).hexdigest()

#function to verify login credentials by comparing the input username and hashed password against the stored values in users.txt. It also checks the selected role to ensure it matches the user's role in the database.
def verify_login(username, password, selected_role):
    """
    FOR PAULO: Call this when the 'Login' button is clicked.
    
    Args:
        username (str): Input from UI.
        password (str): Input from UI.
        
    Returns:
        tuple: (bool, str or None) -> (True, 'Teacher'), (True, 'Student'), or (False, None)
    """
    input_hash = hash_password(password)
    try:
        if os.path.exists(users_path):
            with open(users_path, 'r') as file:
                for line in file:
                    #standardized split and strip to ensure match even with extra spaces
                    u, p_hash, r = [item.strip() for item in line.split(',')]
                    # Compare the hashes, not the plain text!
                    if username == u and input_hash == p_hash:
                        return True, r
        return False, None
    except Exception as e:
        print(f"Login error: {e}")
        return False


# --- STUDENT MANAGEMENT ---


#function to generate the next unique Student ID by reading existing IDs from students.txt and returning the next available number. This ensures that each student gets a unique ID without manual input.
def generate_next_id():
    #helper function to find the next available Student ID.
    if not os.path.exists(students_path):
        return "1"
    
    ids = []
    try:
        with open(students_path, 'r') as file:
            for line in file:
                parts = [item.strip() for item in line.split(',')]
                if parts[0]:
                    ids.append(int(parts[0]))
        
        #if the file is empty, start at 1. Otherwise, Max ID + 1.
        return str(max(ids) + 1) if ids else "1"
    except (ValueError, IndexError, Exception):
        return "1"

#register a new student by adding their name to students.txt and creating a login in users.txt with a default password. The ID is generated automatically to ensure uniqueness.
def registration_student(name):
    """
    FOR PAULO:
    Call this function when the 'Register' button is clicked.
    
    Args:
        name (str): The Name entered in the GUI.

    REVISED FOR PAULO: now only needs to send the NAME.
    The ID is generated automatically to ensure it is unique.
    """
    try:
        #generate the unique ID automatically
        new_id = generate_next_id()
        
        #append to students.txt
        with open(students_path, 'a') as file:
            file.write(f"{new_id}, {name}\n")
        
        #create a login for the new student
        #using a default password 'student123'
        default_pass_hash = hash_password("student123")
        with open(users_path, 'a') as file:
            file.write(f"{new_id}, {default_pass_hash}, Student\n")
        
        return True, f"Success: {name} registered with ID: {new_id}. Default pass: student123"

    except Exception as e:
        #manage file errors gracefully
        return False, f"Database error: {e}"


# --- ATTENDANCE & FILTERING ---


#added relational function to show only students enrolled with a specific teacher in a specific course.
def get_students_for_class(course_id, teacher_id):
    """
    FOR PAULO: Call this to show ONLY the students taught by this teacher in this course[cite: 1].
    """
    enrolled_ids = []
    try:
        if os.path.exists(enrollments_path):
            with open(enrollments_path, 'r') as file:
                for line in file:
                    c, t, s = [item.strip() for item in line.split(',')]
                    if c == course_id and t == teacher_id:
                        enrolled_ids.append(s)
        
        all_students = get_all_students()
        return [s for s in all_students if s[0] in enrolled_ids]
    except:
        return []

#save attendance records when the teacher marks P or A for a student. Each record includes the date, course ID, student ID, and status.
def save_attendance(course_id, student_id, status, date=None):
    """
    FOR PAULO: Call this for each student once the teacher marks P or A.
    Args:
        course_id (str): The ID of the course (e.g., 'ICT105').
        student_id (str): The ID of the student being marked.
        status (str): Must be 'P' or 'A'.
        date (str, optional): The date in 'DD-MM-YYYY' format. 
                              Defaults to today if not provided.
    
    Returns:
        tuple: (bool, str) Success status and feedback message.
    """
    #handle the date requirement
    if date is None:
        date = datetime.datetime.now().strftime("%d-%m-%Y")

    #validate status input
    if status.upper() not in ['P', 'A']:
        return False, "Invalid status. Use 'P' or 'A'."

    try:
        #save in format: Date, CourseID, StudentID, Status
        with open(attendance_path, 'a') as file:
            record = f"{date}, {course_id}, {student_id}, {status.upper()}\n"
            file.write(record)
        
        return True, "Attendance recorded."
    except Exception as e:
        return False, f"Error saving attendance: {e}"

#get attendance records with optional filters. If no filters, returns all records.
def get_attendance_records(student_id=None, course_id=None, date=None):
    """
    FOR INDAH: Use this to filter and display records for Task 4.
    If no arguments are passed, it returns all records.
    """
    records = []
    try:
        if not os.path.exists(attendance_path):
            return False, "File does not exist" 

        with open(attendance_path, 'r') as file:
            for line in file:
                #format: Date, CourseID, StudentID, Status
                parts = [p.strip() for p in line.strip().split(',')]
                
                #check filters
                if student_id and parts[2] != str(student_id):
                    continue
                if course_id and parts[1] != str(course_id):
                    continue
                if date and parts[0] != str(date):
                    continue
                
                records.append(parts)
        return True, records
    except Exception as e:
        return False, f"Error: {e}"

# --- DATA PROVIDERS ---

#get all students to display in the Teacher UI dropdown when marking attendance.
def get_all_students():
    """
    FOR PAULO: Call this to get a list of all students to display in the UI.
    
    Returns:
        list: A list of tuples [(id, name), (id, name)...] or empty list if error.
    """
    students = []
    try:
        if os.path.exists(students_path):
            with open(students_path, 'r') as file:
                for line in file:
                    data = line.strip().split(', ')
                    if len(data) == 2:
                        students.append((data[0].strip(), data[1].strip()))
        return students
    except Exception as e:
        print(f"Error reading students: {e}")
        return []

#get all courses for the Teacher UI to display in the dropdown
def get_all_courses():
    #Returns a list of available courses for the Teacher UI.
    courses = []
    try:
        if os.path.exists(courses_path):
            with open(courses_path, 'r') as file:
                for line in file:
                    courses.append([item.strip() for item in line.split(',')])
        return courses
    except Exception as e:
        return []

#run the setup
setup_database()
