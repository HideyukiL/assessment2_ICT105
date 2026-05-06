#import your database manager as 'db' for easy typing
import database_manager as db

def run_developer_a_tests():
    #changed this: added a clear header for Task 6 unit testing documentation
    print("--- STARTING SEPARATED UNIT TESTS ---")
    
    #test Automatic Registration [Task 2]
    #registering a student to test the auto-increment logic
    success, message = db.registration_student("Lucas")
    print(f"Registration Test: {message}")
    
    if success:
        #to match the exact string format in database_manager.py
        try:
            #we split by "ID: " and take the part after it, then split by "." to stop at the end of the ID
            new_id = message.split("ID: ")[1].split(".")[0]
            
            #clear separator for the login phase of the test
            print(f"\n--- Testing Auto-Generated Login for ID: {new_id} ---")
            
            #test Login Verification
            #checking if the automatic credentials (ID + default password) work
            is_logged_in = db.verify_login(new_id, "student123", "Student")
            
            if is_logged_in:
                print(f"PASS: Student {new_id} can log in with default password.")
            else:
                print(f"FAIL: Login verification failed for Student {new_id}.")
        
        #error handling to prevent the test script from crashing if the string format changes
        except IndexError:
            print("FAIL: Could not parse ID from the success message. Check the string format!")

    #test Teacher Login to ensure role-based security works
    print("\n--- Testing Teacher Login ---")
    is_teacher_logged_in = db.verify_login("T101", "teacher123", "Teacher")
    if is_teacher_logged_in:
        print("PASS: Teacher T101 logged in successfully.")
    else:
        print("FAIL: Teacher T101 login failed.")
            
    #Test Attendance Format
    #testing if we can save a record in the mandatory format: Date, CourseID, StudentID, Status
    att_success, att_msg = db.save_attendance("ICT105", "1", "P")
    print(f"\nAttendance Test: {att_msg}")

    #Test Relational Filtering (Are students linked to the right teacher?)
    print("\n--- Testing Relational Class Filtering ---")
    students_in_class = db.get_students_for_class("ICT105", "T101")
    if students_in_class:
        print(f"PASS: Found {len(students_in_class)} students enrolled in T101's ICT105 class.")
    else:
        print("FAIL: No students found for this class.")

    #Test Attendance Filtering for Task 4 (Indah's function)
    print("\n--- Testing Attendance Filters ---")
    filter_success, records = db.get_attendance_records(student_id="1")
    if filter_success and len(records) > 0:
        print(f"PASS: Successfully filtered attendance. Found {len(records)} records for Student 1.")
    else:
        print("FAIL: Could not filter attendance for Student 1.")

    #Edge Case / Validation Test
    print("\n--- Testing Edge Cases (Invalid Data) ---")
    #trying to mark attendance with 'X' instead of 'P' or 'A'
    edge_success, edge_msg = db.save_attendance("ICT105", "1", "X")
    if not edge_success:
        print(f"PASS: System safely blocked invalid status. Message: {edge_msg}")
    else:
        print("FAIL: System incorrectly accepted an invalid attendance status!")

#run the tests only when this file is executed directly
if __name__ == "__main__":
    run_developer_a_tests()