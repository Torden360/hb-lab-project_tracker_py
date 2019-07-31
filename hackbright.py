"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """
        INSERT INTO students(first_name, last_name, github)
            VALUES (:first_name, :last_name, :github)
        """
    db_cursor = db.session.execute(QUERY, {'first_name': first_name, 
                                           'last_name': last_name, 
                                           'github': github})
    # commit changes and close transaction
    db.session.commit()

    print(f'Successfully added student: {first_name} {last_name}')



def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """
    SELECT title, description
    FROM projects 
    WHERE title = :title"""

    db_cursor = db.session.execute(QUERY, {'title' :title})

    project = db_cursor.fetchone()

    print(f"Hey, the {project[0]} project is {project[1]}")


def get_grade_by_github_title(student_github, title):
    """Print grade student received for a project."""
    QUERY = """
    SELECT grade, project_title, student_github
    FROM grades
    WHERE (project_title = :titlex) AND (student_github = :student_githubx)
    """
    # :titlex is just a placeholder WITHIN the SQL query string, we pass in the
    # argument from the FN parameter 'title' using the session.execute
    # so, the placeholder from QUERY becomes the key 
    # db.session.execute(QUERY, {'placeholder/key':function parameter})

    db_cursor = db.session.execute(QUERY, {'titlex': title, 
                                           'student_githubx': student_github})
    grade_p = db_cursor.fetchone()
    
    print(f"This is {grade_p[2]} for project {grade_p[1]} grade is {grade_p[0]}")



def get_projects(student_github):
    """Print grade student received for a project."""
    QUERY = """
    SELECT grade, project_title, student_github
    FROM grades
    WHERE (student_github = :student_githubx)
    """
    # getting more than one row with fetchall 
    # now you have a list of tuples of jhack's info :
        # [(10, 'Markov', 'jhacks'), (2, 'Blockly', 'jhacks')]
    # can index in an index to get variable data or can loop and index


    db_cursor = db.session.execute(QUERY, {'student_githubx': student_github})
    grade_p = db_cursor.fetchall()

    print(grade_p)
    
    print(f"This is {grade_p[0][2]} for project {grade_p[0][1]} grade is {grade_p[0][0]}")
    


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    pass


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    # handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
