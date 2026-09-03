students = []

subjects = ("English", "Hindi", "Physics", "Chemistry", "Math")


def add_student():

    y = int(input("Enter Numbers Of Students In Class : "))

    i = 1

    while i <= y:

        print("\nEnter Details Of Student", i)

        name = input("Enter Student Name : ")
        roll_number = input("Enter Student Roll Number : ")

        marks = []

        for subject in subjects:
            mark = int(input("Enter " + subject + " Marks : "))
            marks.append(mark)

        total = 0

        for mark in marks:
            total = total + mark

        percentage = (total / 500) * 100

        if 90 <= percentage <= 100:
            grade = "A+"
            result = "Pass"

        elif 80 <= percentage < 90:
            grade = "A"
            result = "Pass"

        elif 70 <= percentage < 80:
            grade = "B"
            result = "Pass"

        elif 60 <= percentage < 70:
            grade = "C"
            result = "Pass"

        elif 50 <= percentage < 60:
            grade = "D"
            result = "Pass"

        else:
            grade = "F"
            result = "Fail"

        student = {
            "Name": name,
            "Roll Number": roll_number,
            "Marks": marks,
            "Total": total,
            "Percentage": percentage,
            "Grade": grade,
            "Result": result
        }

        students.append(student)

        print("Student Added Successfully!")

        i = i + 1


def show_students():

    if len(students) == 0:
        print("No Students Found.")
        return

    for student in students:

        print("\n-----------------------------")
        print("Roll Number :", student["Roll Number"])
        print("Name :", student["Name"])

        print("Marks:")

        i = 0

        for subject in subjects:
            print(subject, ":", student["Marks"][i])
            i = i + 1

        print("Total :", student["Total"])
        print("Percentage :", student["Percentage"], "%")
        print("Grade :", student["Grade"])
        print("Result :", student["Result"])

        print("-----------------------------")


def search_student():

    if len(students) == 0:
        print("No Students Found.")
        return

    roll = input("Enter Roll Number : ")

    found = False

    for student in students:

        if student["Roll Number"] == roll:

            print("\n==============================")
            print("       STUDENT RESULT")
            print("==============================")

            print("Roll Number :", student["Roll Number"])
            print("Name :", student["Name"])

            i = 0

            for subject in subjects:
                print(subject, ":", student["Marks"][i])
                i = i + 1

            print("Total :", student["Total"])
            print("Percentage :", student["Percentage"], "%")
            print("Grade :", student["Grade"])
            print("Result :", student["Result"])

            found = True

    if found == False:
        print("Student Not Found.")


def find_topper():

    if len(students) == 0:
        print("No Students Found.")
        return

    topper = students[0]

    for student in students:

        if student["Percentage"] > topper["Percentage"]:
            topper = student

    print("\n==============================")
    print("           TOPPER")
    print("==============================")

    print("Roll Number :", topper["Roll Number"])
    print("Name :", topper["Name"])
    print("Total :", topper["Total"])
    print("Percentage :", topper["Percentage"], "%")
    print("Grade :", topper["Grade"])
    print("Result :", topper["Result"])


def count_pass_fail():

    if len(students) == 0:
        print("No Students Found.")
        return

    pass_count = 0
    fail_count = 0

    for student in students:

        if student["Result"] == "Pass":
            pass_count = pass_count + 1

        else:
            fail_count = fail_count + 1

    print("\n==============================")
    print("        PASS / FAIL")
    print("==============================")

    print("Total Students :", len(students))
    print("Total Pass Students :", pass_count)
    print("Total Fail Students :", fail_count)


while True:

    print("\n================================")
    print("   STUDENT RESULT MANAGEMENT")
    print("================================")

    print("1. Add Student")
    print("2. Show All Students")
    print("3. Search Student")
    print("4. Find Topper")
    print("5. Count Pass/Fail")
    print("6. Exit")

    x = int(input("Enter Your Choice : "))

    if x == 1:
        add_student()

    elif x == 2:
        show_students()

    elif x == 3:
        search_student()

    elif x == 4:
        find_topper()

    elif x == 5:
        count_pass_fail()

    elif x == 6:
        print("\nThank You For Using Student Result Management System!")
        break

    else:
        print("Invalid Choice! Please Enter 1 To 6.")