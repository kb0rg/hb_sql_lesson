import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM projects WHERE title = ? """
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Project Title: %s
Project Description: %s
Maxium Grade: %s"""%(row[0], row[1], row[2])
    



def get_student_grade_for_project(first_name, last_name, project_title):
    query = """SELECT first_name, last_name, project_title, grade FROM students 
    INNER JOIN grades ON (students.github = grades.student_github) WHERE first_name = ? AND last_name = ? AND
    project_title = ?"""

    DB.execute(query, (first_name, last_name, project_title))
    row = DB.fetchone()
    print """\
Student: %s %s
Project: %s
Grade: %s"""%(row[0], row[1], row[2], row[3])

def get_all_grades_for_student(first_name, last_name):
    query = """SELECT project_title, grade FROM students 
    INNER JOIN grades ON (students.github = grades.student_github) WHERE first_name = ? 
    AND last_name = ? GROUP BY project_title"""

    DB.execute(query, (first_name, last_name))
    results = DB.fetchall()
    
    print "Student: ", first_name, last_name
    for title, score in results:
        print "Project: ", title, "Grade: ", score

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def add_a_project(project_title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade)
    values (?, ?, ?)"""
    DB.execute(query, (project_title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s"%(project_title)
    

def get_that_github(first_name, last_name): 
    query = """SELECT github from students where first_name = ? and 
    last_name = ?"""
    DB.execute(query, (first_name, last_name))
    results = DB.fetchone()
    return results[0]

def assign_student_grade_for_project(first_name, last_name, project_title, grade):
    github_from_db = get_that_github(first_name, last_name)
    query ="""INSERT into Grades (student_github, project_title, grade) 
        VALUES (?, ?, ?)"""
    DB.execute(query, (github_from_db, project_title, grade))
    CONN.commit()
    print """Successfully added grade: %s 
    to Project: %s for Student: %s %s"""%(grade, project_title, first_name, last_name)


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database > ")
        tokens = input_string.split("|")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command =="project":
            get_project_by_title(*args)
        elif command == "project_grade":
            get_student_grade_for_project(*args)
        elif command =="student_grade":
            get_all_grades_for_student(*args)
        elif command =="new_project":
            add_a_project(*args)
        elif command =="assign_grade":
            assign_student_grade_for_project(*args)
        elif command =="get_github":
            get_that_github(*args)

    CONN.close()

if __name__ == "__main__":
    main()
