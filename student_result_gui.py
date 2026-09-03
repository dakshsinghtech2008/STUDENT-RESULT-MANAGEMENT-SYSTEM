import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# ---------------------------------------------------------
# Persistent storage setup
# ---------------------------------------------------------
DATA_FILE = "students_data.json"

SUBJECTS = ("English", "Hindi", "Physics", "Chemistry", "Math")
MAX_MARKS_PER_SUBJECT = 100
MAX_TOTAL = MAX_MARKS_PER_SUBJECT * len(SUBJECTS)  # 500

students = []


def load_students():
    """Load students from the JSON file if it exists."""
    global students
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                students = json.load(f)
        except (json.JSONDecodeError, IOError):
            students = []
    else:
        students = []


def save_students():
    """Persist the current students list to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)


def calculate_result(marks):
    """marks: list of 5 ints in SUBJECTS order. Returns total, percentage, grade, result."""
    total = sum(marks)
    percentage = round((total / MAX_TOTAL) * 100, 2)

    if 90 <= percentage <= 100:
        grade = "A+"
    elif 80 <= percentage < 90:
        grade = "A"
    elif 70 <= percentage < 80:
        grade = "B"
    elif 60 <= percentage < 70:
        grade = "C"
    elif 50 <= percentage < 60:
        grade = "D"
    else:
        grade = "F"

    result = "Pass" if percentage >= 50 else "Fail"
    return total, percentage, grade, result


# ---------------------------------------------------------
# Add Student Window
# ---------------------------------------------------------
def add_student():
    student_window = tk.Toplevel(window)
    student_window.title("Add Student")
    student_window.geometry("400x550")

    tk.Label(student_window, text="ADD STUDENT", font=("Arial", 16, "bold")).pack(pady=15)

    tk.Label(student_window, text="Student Name").pack()
    name_entry = tk.Entry(student_window)
    name_entry.pack(pady=5)

    tk.Label(student_window, text="Roll Number").pack()
    roll_entry = tk.Entry(student_window)
    roll_entry.pack(pady=5)

    subject_entries = {}
    for subject in SUBJECTS:
        tk.Label(student_window, text=f"{subject} Marks").pack()
        entry = tk.Entry(student_window)
        entry.pack(pady=3)
        subject_entries[subject] = entry

    def save_student():
        student_name = name_entry.get().strip()
        student_roll = roll_entry.get().strip()

        if not student_name or not student_roll:
            messagebox.showerror("Error", "Name and Roll Number are required.")
            return

        if any(s["roll"] == student_roll for s in students):
            messagebox.showerror("Error", f"Roll Number '{student_roll}' already exists.")
            return

        marks = []
        for subject in SUBJECTS:
            value = subject_entries[subject].get().strip()
            if not value.isdigit():
                messagebox.showerror("Error", f"{subject} marks must be a whole number.")
                return
            mark = int(value)
            if not (0 <= mark <= MAX_MARKS_PER_SUBJECT):
                messagebox.showerror("Error", f"{subject} marks must be between 0 and {MAX_MARKS_PER_SUBJECT}.")
                return
            marks.append(mark)

        total, percentage, grade, result = calculate_result(marks)

        students.append({
            "roll": student_roll,
            "name": student_name,
            "marks": dict(zip(SUBJECTS, marks)),
            "total": total,
            "percentage": percentage,
            "grade": grade,
            "result": result
        })

        save_students()
        messagebox.showinfo("Success", f"{student_name} added and saved successfully!")
        student_window.destroy()

    tk.Button(student_window, text="Save Student", command=save_student).pack(pady=20)


# ---------------------------------------------------------
# Edit / Delete Student Window
# ---------------------------------------------------------
def edit_delete_student():
    if not students:
        messagebox.showinfo("No Data", "No students added yet.")
        return

    ed_window = tk.Toplevel(window)
    ed_window.title("Edit / Delete Student")
    ed_window.geometry("650x400")

    tk.Label(ed_window, text="Select a student, then Edit or Delete", font=("Arial", 12, "bold")).pack(pady=10)

    columns = ("roll", "name", "total", "percentage", "grade", "result")
    tree = ttk.Treeview(ed_window, columns=columns, show="headings", height=10)
    headings = ["Roll No", "Name", "Total", "Percentage", "Grade", "Result"]
    for col, head in zip(columns, headings):
        tree.heading(col, text=head)
        tree.column(col, width=100, anchor="center")

    def refresh_tree():
        tree.delete(*tree.get_children())
        for s in students:
            tree.insert("", tk.END, iid=s["roll"], values=(
                s["roll"], s["name"], s["total"], s["percentage"], s["grade"], s["result"]
            ))

    refresh_tree()
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student first.")
            return
        roll = selected[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete student with Roll No {roll}?")
        if confirm:
            students[:] = [s for s in students if s["roll"] != roll]
            save_students()
            refresh_tree()
            messagebox.showinfo("Deleted", "Student deleted successfully.")

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student first.")
            return
        roll = selected[0]
        student = next((s for s in students if s["roll"] == roll), None)
        if not student:
            return

        edit_window = tk.Toplevel(ed_window)
        edit_window.title(f"Edit Student - {roll}")
        edit_window.geometry("400x500")

        tk.Label(edit_window, text="EDIT STUDENT", font=("Arial", 16, "bold")).pack(pady=15)

        tk.Label(edit_window, text="Student Name").pack()
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, student["name"])
        name_entry.pack(pady=5)

        tk.Label(edit_window, text="Roll Number (cannot change)").pack()
        roll_label = tk.Label(edit_window, text=student["roll"], font=("Arial", 10, "italic"))
        roll_label.pack(pady=5)

        subject_entries = {}
        for subject in SUBJECTS:
            tk.Label(edit_window, text=f"{subject} Marks").pack()
            entry = tk.Entry(edit_window)
            entry.insert(0, str(student["marks"][subject]))
            entry.pack(pady=3)
            subject_entries[subject] = entry

        def save_edit():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Name is required.")
                return

            marks = []
            for subject in SUBJECTS:
                value = subject_entries[subject].get().strip()
                if not value.isdigit():
                    messagebox.showerror("Error", f"{subject} marks must be a whole number.")
                    return
                mark = int(value)
                if not (0 <= mark <= MAX_MARKS_PER_SUBJECT):
                    messagebox.showerror("Error", f"{subject} marks must be between 0 and {MAX_MARKS_PER_SUBJECT}.")
                    return
                marks.append(mark)

            total, percentage, grade, result = calculate_result(marks)

            student["name"] = new_name
            student["marks"] = dict(zip(SUBJECTS, marks))
            student["total"] = total
            student["percentage"] = percentage
            student["grade"] = grade
            student["result"] = result

            save_students()
            refresh_tree()
            messagebox.showinfo("Success", "Student updated successfully.")
            edit_window.destroy()

        tk.Button(edit_window, text="Save Changes", command=save_edit).pack(pady=20)

    button_frame = tk.Frame(ed_window)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Edit Selected", width=15, command=edit_selected).pack(side="left", padx=10)
    tk.Button(button_frame, text="Delete Selected", width=15, command=delete_selected).pack(side="left", padx=10)


# ---------------------------------------------------------
# Show All Students
# ---------------------------------------------------------
def show_all_students():
    if not students:
        messagebox.showinfo("No Data", "No students added yet.")
        return

    show_window = tk.Toplevel(window)
    show_window.title("All Students")
    show_window.geometry("750x350")

    columns = ("roll", "name") + SUBJECTS + ("total", "percentage", "grade", "result")
    tree = ttk.Treeview(show_window, columns=columns, show="headings")

    headings = ["Roll No", "Name"] + list(SUBJECTS) + ["Total", "Percentage", "Grade", "Result"]
    for col, head in zip(columns, headings):
        tree.heading(col, text=head)
        tree.column(col, width=70, anchor="center")

    for s in students:
        row = [s["roll"], s["name"]] + [s["marks"][subj] for subj in SUBJECTS] + \
              [s["total"], s["percentage"], s["grade"], s["result"]]
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True, padx=10, pady=10)


# ---------------------------------------------------------
# Search Student
# ---------------------------------------------------------
def search_student():
    search_window = tk.Toplevel(window)
    search_window.title("Search Student")
    search_window.geometry("400x350")

    tk.Label(search_window, text="SEARCH STUDENT", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(search_window, text="Enter Roll Number or Name").pack()
    query_entry = tk.Entry(search_window)
    query_entry.pack(pady=5)

    result_label = tk.Label(search_window, text="", justify="left", font=("Arial", 11))
    result_label.pack(pady=15)

    def do_search():
        query = query_entry.get().strip().lower()
        if not query:
            messagebox.showerror("Error", "Please enter a roll number or name.")
            return

        found = None
        for s in students:
            if s["roll"].lower() == query or s["name"].lower() == query:
                found = s
                break

        if found:
            marks_text = "\n".join(f"{subj}: {found['marks'][subj]}" for subj in SUBJECTS)
            result_label.config(text=(
                f"Name: {found['name']}\n"
                f"Roll No: {found['roll']}\n"
                f"{marks_text}\n"
                f"Total: {found['total']}\n"
                f"Percentage: {found['percentage']}%\n"
                f"Grade: {found['grade']}\n"
                f"Result: {found['result']}"
            ))
        else:
            result_label.config(text="No matching student found.")

    tk.Button(search_window, text="Search", command=do_search).pack(pady=5)


# ---------------------------------------------------------
# Find Topper
# ---------------------------------------------------------
def find_topper():
    if not students:
        messagebox.showinfo("No Data", "No students added yet.")
        return

    topper = max(students, key=lambda s: s["percentage"])
    messagebox.showinfo(
        "Topper",
        f"Topper: {topper['name']} (Roll No: {topper['roll']})\n"
        f"Total: {topper['total']} | Percentage: {topper['percentage']}% | Grade: {topper['grade']}"
    )


# ---------------------------------------------------------
# Count Pass/Fail
# ---------------------------------------------------------
def count_pass_fail():
    if not students:
        messagebox.showinfo("No Data", "No students added yet.")
        return

    pass_count = sum(1 for s in students if s["result"] == "Pass")
    fail_count = len(students) - pass_count

    messagebox.showinfo(
        "Pass/Fail Count",
        f"Total Students: {len(students)}\n"
        f"Pass: {pass_count}\n"
        f"Fail: {fail_count}"
    )


# ---------------------------------------------------------
# Main Window
# ---------------------------------------------------------
load_students()

window = tk.Tk()
window.title("Student Result Management System")
window.geometry("500x480")

heading = tk.Label(window, text="STUDENT RESULT MANAGEMENT", font=("Arial", 18, "bold"))
heading.pack(pady=25)

tk.Button(window, text="Add Student", width=25, command=add_student).pack(pady=5)
tk.Button(window, text="Show All Students", width=25, command=show_all_students).pack(pady=5)
tk.Button(window, text="Search Student", width=25, command=search_student).pack(pady=5)
tk.Button(window, text="Edit / Delete Student", width=25, command=edit_delete_student).pack(pady=5)
tk.Button(window, text="Find Topper", width=25, command=find_topper).pack(pady=5)
tk.Button(window, text="Count Pass/Fail", width=25, command=count_pass_fail).pack(pady=5)
tk.Button(window, text="Exit", width=25, command=window.destroy).pack(pady=5)

data_status = tk.Label(
    window,
    text=f"{len(students)} student(s) loaded from {DATA_FILE}" if students else "No saved data found — starting fresh.",
    font=("Arial", 9), fg="gray"
)
data_status.pack(pady=10)

window.mainloop()