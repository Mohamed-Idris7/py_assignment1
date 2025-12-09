courses_available = [
    {
        "code": "SAIA1113",
        "name": "PYTHON PROGRAMMING",
        "credit": 3,
        "slots": {"day": "Monday", "time": "08:00-10:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "SAIA1143",
        "name": "DISCRETE MATHEMATICS",
        "credit": 3,
        "slots": {"day": "Tuesday", "time": "08:00-10:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "SAIA1013",
        "name": "RESPONSIBLE AI AND ETHICS",
        "credit": 3,
        "slots": {"day": "Tuesday", "time": "14:00-16:00"},
        "location": "Seminar Room 3, BATC",
    },
    {
        "code": "SAIA1123",
        "name": "INTRODUCTION TO AI",
        "credit": 3,
        "slots": {"day": "Wednesday", "time": "08:00-10:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "ULRS1032",
        "name": "INTEGRITY AND ANTI-CORRUPTION",
        "credit": 2,
        "slots": {"day": "Wednesday", "time": "10:00-12:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "SAIA1133",
        "name": "DATA MANAGEMENT",
        "credit": 3,
        "slots": {"day": "Wednesday", "time": "12:00-14:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "SAIA1153",
        "name": "MATHEMATICS FOR ML",
        "credit": 3,
        "slots": {"day": "Thursday", "time": "08:00-10:00"},
        "location": "Lecture Room 2, Lvl 15",
    },
]

student = {"name": "", "matric": "", "registered_courses": [], "total_credits": 0}

# ==========================================
#                  BRAD
# ==========================================
# FUNCTIONS:
# 1. display_menu()
# 2. add_course()
# 3. remove_course() (mapped to drop_course)
# 4. check_credit_limit()


def display_menu():
    # display main menu – called every loop
    print("\n" + "=" * 65)
    print("    STUDENT COURSE REGISTRATION & TIMETABLE BUILDER")
    print("=" * 65)
    print("1. Register New Student")
    print("2. Add Course")
    print("3. Drop Course")
    print("4. View Registered Courses")
    print("5. Generate Timetable")
    print("6. Save & Exit")
    print("-" * 65)


def check_credit_limit(current_credits, new_credit):
    # return True if adding course keeps total <= 21
    if current_credits + new_credit > 21:
        print(
            f"Error: Cannot add! Exceeds 21 credits ({current_credits} + {new_credit} = {current_credits + new_credit})"
        )
        return False
    return True


def register_student():
    print("\n--- NEW STUDENT REGISTRATION ---")
    student["name"] = input("Enter Name: ")
    student["matric"] = input("Enter Matric Number: ")
    student["registered_courses"] = []
    student["total_credits"] = 0
    print(f"Student {student['name']} registered successfully!")


def add_course():
    # add course with full validation
    if not student["name"]:
        print("Please register student first (Option 1)!")
        return

    # 1. display list
    print("\nAvailable Courses (Year 1, Sem 1):")
    for c in courses_available:
        print(f"{c['code']} - {c['name']} ({c['slots']['day']} {c['slots']['time']})")

    code = input("\nEnter course code to add: ").strip().upper()

    # 2. find course
    course = None
    for c in courses_available:
        if c["code"] == code:
            course = c
            break

    if not course:
        print("Course not found!")
        return

    # 3. validation: check if already registered
    if course in student["registered_courses"]:
        print("You already added this course!")
        return

    # 4. validation: credits
    if not check_credit_limit(student["total_credits"], course["credit"]):
        return

    # 5. validation: clashes
    # INTEGRATION POINT: This will call the function detect_clash() below
    if detect_clash(course):
        print(f"TIMETABLE CLASH DETECTED! Cannot add {course['code']}.")
        return

    # 6. finalize add
    student["registered_courses"].append(course)
    student["total_credits"] += course["credit"]
    print(f"Course {course['code']} added successfully!")
    print(f"Total credits: {student['total_credits']}/21")


def drop_course():
    # remove registered course
    if not student["registered_courses"]:
        print("No courses registered yet!")
        return

    code = input("\nEnter course code to drop: ").strip().upper()

    found = False
    # range(len(...)) creates a list of indices: [0, 1, 2, etc.]
    for i in range(len(student["registered_courses"])):
        # access the course manually using the index 'i'
        c = student["registered_courses"][i]

        if c["code"] == code:
            removed = student["registered_courses"].pop(i)
            student["total_credits"] -= removed["credit"]
            print(f"Course {code} dropped successfully!")
            print(f"Total credits now: {student['total_credits']}/21")
            found = True
            break

    if not found:
        print("Course not found in your registration!")


def view_registered_courses():
    if not student["registered_courses"]:
        print("\nNo courses registered.")
    else:
        print(f"\nRegistered Courses for {student['name']}:")
        for c in student["registered_courses"]:
            print(f"- {c['code']}: {c['name']} ({c['credit']} credits)")
        print(f"Total Credits: {student['total_credits']}")


def detect_clash(new_course):
    """
    check if new_course time slot overlap with any registered course
    return True if a clash exists.
    """
    new_day = new_course["slots"]["day"]
    new_time = new_course["slots"]["time"]

    for registered in student["registered_courses"]:
        reg_day = registered["slots"]["day"]
        reg_time = registered["slots"]["time"]

        # if day matches AND time matches
        if new_day == reg_day and new_time == reg_time:
            print(
                f"CLASH ALERT: New course conflicts with {registered['code']} ({registered['name']})"
            )
            return True

    return False
