
import json
import os
from datetime import datetime

def save_user_data(student_data):
    with open("student_summary.json", "w") as file:
        json.dump(student_data, file, indent=4)

def load_user_data(add_subject_func, display_profile_func, subject_menu_func):
    filepath = "student_summary.json"
    # returning user?
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as file:
                content = file.read().strip()
                if not content:
                    raise ValueError("")
                data = json.loads(content)
            print(f"Welcome back, {data['name']}!")
            print(f"Last login: {data.get('last_login', 'N/A')}")
            data["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return data, False
        except Exception as e:
            print(f"New User {e}")

    # brand-new user flow
    print("Welcome to Learning Companion!")
    name = input("Enter your name: \n").title()
    print(f"Hello {name}! Let's set up your subjects")

    while True:
        num_input = input("How many subjects are you studying? \n")
        if num_input.isdigit() and int(num_input) > 0:
            num_of_subjects = int(num_input)
            break
        print("Oops! Please enter a positive number.")

    data = {
        "name": name,
        "subjects": [],
        "study_goals": {},
        "grades": {},
        "study_sessions": [],
        "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    for i in range(num_of_subjects):
        add_subject_func(data, i)
    display_profile_func(data)
    subject_menu_func(data)

    return data, True
