from data_handler import save_user_data
import sys


# <------------------------------------------------ Functions for adding subjects and more into lists and dictionaries --------------------------------->

def validate_study_goal(hours):
    return hours.isdigit() and int(hours) > 0


def add_subject(student_data, index):
    subject_name = input(f"Subject {index + 1} name: ").strip()
    student_data["subjects"].append(subject_name)

    while True:
        study_goal = input(f"Monthly study goal for {subject_name} (hours): ")
        if not validate_study_goal(study_goal):
            print("Please enter a number for hours.")
            continue
        break

    # Study goals
    student_data["study_goals"][subject_name] = int(study_goal)

    # Grades 
    student_data["grades"][subject_name] = []
    save_user_data(student_data)


def display_profile(student_data):
    print("\n✅ Profile created successfully!")
    print("=== YOUR PROFILE ===")
    print(f"Name: {student_data['name']}")
    print("Subjects and Goals:")
    for subject in student_data["subjects"]:
        hours = student_data["study_goals"][subject]
        print(f"• {subject}: {hours} hours/month")

# <--------------------------------------------------------- Main Menus -------------------------------------------------------------->

def subject_menu(student_data):
    while True:
        print("\nWould you like to:")
        print("1. Add another subject")
        print("2. Continue to main menu")

        choice = input("Choose an option (1 or 2): ").strip()
        if choice == "1":
            index = len(student_data["subjects"])
            add_subject(student_data, index)
            display_profile(student_data)  
        elif choice == "2":
            main_menu(student_data)
            break
        else:
            print("Invalid input. Please enter 1 or 2.")


def main_menu(student_data, show_menu=True):
    while True:
        # only print the old menu if asked
        if show_menu:
            print("\n=== MAIN MENU ===")
            print("1.  Add Single Grade")
            print("2.  Add Multiple Grades")
            print("3.  View All Grades")
            print("4.  Calculate Averages")
            print("5.  Performance Analysis")
            print("6.  Study Session Tracker")
            print("7.  Exit Program")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_single_grade(student_data)
        elif choice == "2":
            add_multiple_grades(student_data)
        elif choice == "3":
            view_all_grades(student_data)
        elif choice == "4":
            calculate_averages(student_data)
        elif choice == "5":
            performance_analysis(student_data)
        elif choice == "6":
            study_session_menu(student_data)
        elif choice == "7":
            print("Goodbye! 👋")
            sys.exit(0)
        else:
            print("Invalid input. Please enter a number from 1 to 7.")

# <------------------------------------------------------- Choice 1 -  Adding Single Grade -------------------------------------------------------------->

def calculate_average(grades):
    if not grades:
        return 0
    return sum(grades) / len(grades)


def add_single_grade(student_data):
    subjects = student_data["subjects"]
    grades_data = student_data["grades"]

    print("\nAvailable Subjects:")
    for i, subject in enumerate(subjects):
        avg = calculate_average(grades_data[subject])
        avg_display = f"{avg:.1f}" if grades_data[subject] else "No grades yet"
        print(f"{i + 1}. {subject} (Current avg: {avg_display})")

    while True:
        subject_choice = input(f"\nSelect subject (1-{len(subjects)}): ").strip()
        if subject_choice.isdigit() and 1 <= int(subject_choice) <= len(subjects):
            subject_index = int(subject_choice) - 1
            subject_name = subjects[subject_index]
            break
        else:
            print("Invalid input. Please choose a valid subject number.")

    prev_avg = calculate_average(grades_data[subject_name])

    while True:
        while True:
            grade_input = input(f"\nEnter grade for {subject_name} (0-100): ").strip()
            if grade_input.isdigit() and 0 <= int(grade_input) <= 100:
                grade = int(grade_input)
                break
            else:
                print("Invalid grade. Please enter a number from 0 to 100.")

        grade_type = input("Grade type (exam/quiz/homework/project): ").strip().lower()

        grades_data[subject_name].append(grade)

        print(f"\n✅ Grade {grade} ({grade_type}) added to {subject_name}!")

        current_grades = grades_data[subject_name]
        new_avg = calculate_average(current_grades)

        print(f"\nCurrent grades for {subject_name}: {current_grades}")
        print(f"Current average: {new_avg:.1f}")

        if len(current_grades) > 1:
            improvement = new_avg - prev_avg
            print(f"Improvement: {improvement:+.1f} points! 📈")

        cont = input("\nContinue adding grades? (y/n): ").strip().lower()
        if cont != "y":
            break
        else:
            prev_avg = new_avg
    save_user_data(student_data)


# <------------------------------------------------------- Choice 2 - Adding Multiple Grades -------------------------------------------------------------->

def add_multiple_grades(student_data):
    subjects = student_data["subjects"]
    grades_data = student_data["grades"]

    print("\nSelect subject for multiple grades:")
    for i, subject in enumerate(subjects):
        avg = calculate_average(grades_data[subject])
        avg_display = f"{avg:.1f}" if grades_data[subject] else "No grades"
        print(f"{i + 1}. {subject} (avg: {avg_display})")

    while True:
        subject_choice = input(f"\nChoice (1-{len(subjects)}): ").strip()
        if subject_choice.isdigit() and 1 <= int(subject_choice) <= len(subjects):
            subject_index = int(subject_choice) - 1
            subject_name = subjects[subject_index]
            break
        else:
            print("Invalid input. Please choose a valid subject number.")

    while True:
        count_input = input(f"\nHow many grades to add for {subject_name}? ").strip()
        if count_input.isdigit() and int(count_input) > 0:
            count = int(count_input)
            break
        else:
            print("Please enter a valid number.")

    new_grades = []
    for i in range(count):
        while True:
            grade_input = input(f"Grade {i + 1}: ").strip()
            if grade_input.isdigit() and 0 <= int(grade_input) <= 100:
                new_grades.append(int(grade_input))
                break
            else:
                print("Enter a grade from 0 to 100.")

    # adding grades
    grades_data[subject_name].extend(new_grades)

    print(f"\n✅ Added {count} grades to {subject_name}!")
    print(f"Grades: {grades_data[subject_name]}")
    avg = calculate_average(grades_data[subject_name])
    print(f"Average: {avg:.1f}")

    # Subject Summary
    print("\nSubject Summary:")
    highest = max(grades_data[subject_name])
    lowest = min(grades_data[subject_name])
    grade_range = highest - lowest

    print(f"• Highest grade: {highest}")
    print(f"• Lowest grade: {lowest}")
    print(f"• Range: {grade_range} points")

    # Performance Rating
    if avg >= 90:
        performance = "Excellent! 🌟"
    elif avg >= 80:
        performance = "Good! 👍"
    elif avg >= 70:
        performance = "Average 🙂"
    else:
        performance = "Needs Improvement ❗"

    print(f"• Performance: {performance}")
    save_user_data(student_data)

# <------------------------------------------------------- Choice 3 - View All Grades -------------------------------------------------------------->

def view_all_grades(student_data):
    print("\n📋 All Grades Overview:")
    for subject in student_data["subjects"]:
        grades = student_data["grades"][subject]
        if grades:
            average = sum(grades) / len(grades)
            print(f"\n{subject}")
            print(f"Grades: {grades}")
            print(f"Average: {average:.1f}")
        else:
            print(f"\n{subject}")
            print("Grades: No grades yet")
            print("Average: N/A")

# <------------------------------------------------------- Choice 4 - Calculate Averages -------------------------------------------------------------->

def calculate_averages(student_data):
    print("\n📊 Subject Averages:")
    for subject in student_data["subjects"]:
        grades = student_data["grades"][subject]
        if grades:
            avg = sum(grades) / len(grades)
            print(f"• {subject}: {avg:.1f}")
        else:
            print(f"• {subject}: No grades yet")

# <------------------------------------------------------- Choice 5 - Performance analysis -------------------------------------------------------------->

def performance_analysis(student_data):
    from statistics import mean

    print("\n=== PERFORMANCE ANALYSIS ===")

    print("\n📊 Grade Summary:")
    print("┌────────────────────────┬─────────┬─────────┬─────────┬────────────┐")
    print("│ Subject                │ Average │ Grades  │ Best    │ Trend      │")
    print("├────────────────────────┼─────────┼─────────┼─────────┼────────────┤")

    best_avg = -1
    best_subject = None
    most_improved_value = -999
    most_improved_subject = None
    needs_attention = []

    for subject in student_data["subjects"]:
        grades = student_data["grades"][subject]
        if grades:
            avg = mean(grades)
            best = max(grades)
            trend = "➡ Stable"

            if len(grades) >= 2:
                if grades[-1] > grades[0]:
                    trend = "↗ Up"
                    improvement = grades[-1] - grades[0]
                elif grades[-1] < grades[0]:
                    trend = "↘ Down"
                    improvement = grades[-1] - grades[0]
                else:
                    improvement = 0
            else:
                improvement = 0

            if avg > best_avg:
                best_avg = avg
                best_subject = subject

            if improvement > most_improved_value:
                most_improved_value = improvement
                most_improved_subject = subject

            print(f"│ {subject:<22} │ {avg:7.1f} │ {len(grades):7} │ {best:7} │ {trend:<10} │")
        else:
            print(f"│ {subject:<22} │ {'--':>7} │ {0:7} │ {'--':>7} │ {'No data':<10} │")
            needs_attention.append(subject)

    print("└────────────────────────┴─────────┴─────────┴─────────┴────────────┘")

    print()

    # Summary messages
    if best_subject:
        print(f"🏆 Best Performing Subject: {best_subject} ({best_avg:.1f})")
    if most_improved_value > 0:
        print(f"📈 Most Improved: {most_improved_subject} (+{most_improved_value:.1f})")
    if needs_attention:
        for subject in needs_attention:
            print(f"⚠️  Needs Attention: {subject} (no grades recorded)")

    # Recommendations
    print("\nRecommendations:")
    if best_subject:
        print(f"• Great work in {best_subject}! Keep it up!")
    if most_improved_value > 0:
        print(f"• {most_improved_subject} showing good improvement trend")
    for subject in needs_attention:
        print(f"• Add some grades for {subject} to track progress")


# <------------------------------------------------------- Study Sessions Menu -------------------------------------------------------------->

def study_session_menu(student_data):
    while True:
        print("\n=== STUDY SESSION TRACKER ===")
        print("1. Record New Session")
        print("2. View Session History")
        print("3. Monthly Progress Report")
        print("4. Study Pattern Analysis")
        print("5. Back to Main Menu")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            record_study_session(student_data)
        elif choice == "2":
            view_session_history(student_data)
        elif choice == "3":
            monthly_progress_report(student_data)
        elif choice == "4":
            analytics_dashboard_menu(student_data)
        elif choice == "5":
            break
        else:
            print("Invalid input. Please choose 1–5.")

# <-----------------------------------------------------------------Record New Session----------------------------------------------------------->

from datetime import datetime

def record_study_session(student_data):
    subjects = student_data["subjects"]
    goals = student_data["study_goals"]
    sessions = student_data["study_sessions"]

    print("\nAvailable Subjects (Monthly Progress):")
    for i, subject in enumerate(subjects):
        total_hours = sum(s["hours"] for s in sessions if s["subject"] == subject)
        goal = goals.get(subject, 0)
        progress = (total_hours / goal * 100) if goal else 0
        print(f"{i + 1}. {subject} ({total_hours:.1f}/{goal} hours - {int(progress)}% complete)")

    while True:
        choice = input(f"\nSelect subject (1-{len(subjects)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(subjects):
            subject_index = int(choice) - 1
            subject_name = subjects[subject_index]
            break
        else:
            print("Invalid choice. Try again.")

    # Previous total
    previous_hours = sum(s["hours"] for s in sessions if s["subject"] == subject_name)
    goal_hours = goals.get(subject_name, 0)

    while True:
        hours_input = input(f"\nHow many hours did you study {subject_name}? ").strip()
        try:
            hours = float(hours_input)
            if hours > 0:
                break
            else:
                print("Enter a positive number.")
        except ValueError:
            print("Invalid number. Try again.")

    # Activity type menu
    activities = {
        "1": "Reading textbook/materials",
        "2": "Coding practice/exercises",
        "3": "Watching video lectures",
        "4": "Working on projects",
        "5": "Review/revision",
        "6": "Other"
    }

    print("\nWhat type of study activity?")
    for k, v in activities.items():
        print(f"{k}. {v}")

    while True:
        activity_choice = input("Activity type (1-6): ").strip()
        if activity_choice in activities:
            activity = activities[activity_choice]
            break
        else:
            print("Invalid choice.")

    notes = input("\nAny specific notes about this session? (optional)\nNotes: ").strip()

    # Record date
    today = datetime.now().strftime("%B %d, %Y")

    # Add session to student_data
    session = {
        "subject": subject_name,
        "hours": hours,
        "date": today,
        "activity": activity,
        "notes": notes
    }

    sessions.append(session)

    # Recalculate
    new_total = previous_hours + hours
    progress = new_total / goal_hours * 100 if goal_hours else 0
    prev_progress = previous_hours / goal_hours * 100 if goal_hours else 0
    remaining = goal_hours - new_total

    print("\n✅ Study session recorded!")

    print("\nSession Details:")
    print(f"• Subject: {subject_name}")
    print(f"• Duration: {hours} hours")
    print(f"• Activity: {activity}")
    print(f"• Date: {today}")
    print(f"• Notes: {notes if notes else 'No notes'}")

    print("\nUpdated Progress:")
    print(f"• Previous total: {previous_hours:.1f} hours")
    print(f"• New total: {new_total:.1f} hours")
    print(f"• Goal: {goal_hours} hours")
    print(f"• Progress: {int(progress)}% complete (↑ from {int(prev_progress)}%)")
    print(f"• Remaining: {remaining:.1f} hours")

    # Recommendation
    if progress >= 100:
        print("\n🎯 Recommendation: You’ve met your goal! Great job!")
    elif progress >= 70:
        print("\n🎯 Recommendation: Great progress! You're ahead of the monthly pace.")
    elif progress >= 40:
        print("\n🎯 Recommendation: Keep going, you're getting there.")
    else:
        print("\n🎯 Recommendation: Try to increase your study time to stay on track.")

    # Ask to record another
    while True:
        again = input("\nRecord another session? (y/n): ").strip().lower()
        if again == "y":
            record_study_session(student_data)
            break
        elif again == "n":
            break
        else:
            print("Please enter 'y' or 'n'.")
    save_user_data(student_data)

# <------------------------------------------------------- Study session history ---------------------------------------------------------->

from collections import Counter
from datetime import datetime

def view_session_history(student_data):
    sessions = student_data["study_sessions"]

    if not sessions:
        print("\n⚠️ No study sessions recorded yet.")
        return

    print("\n=== STUDY SESSION HISTORY ===\n")

    sorted_sessions = sorted(sessions, key=lambda s: datetime.strptime(s["date"], "%B %d, %Y"), reverse=True)

    index = 0
    page_size = 10

    while index < len(sorted_sessions):
        print("Recent Sessions:")
        print("┌────────────┬────────────────────────┬───────┬────────────────────────────┬────────────────────┐")
        print("│ Date       │ Subject                │ Hours │ Activity                   │ Notes              │")
        print("├────────────┼────────────────────────┼───────┼────────────────────────────┼────────────────────┤")

        for session in sorted_sessions[index:index + page_size]:
            date = session["date"]
            subject = session["subject"][:24].ljust(24)
            hours = f"{session['hours']:.1f}".ljust(5)
            activity = session["activity"][:26].ljust(26)
            notes = session["notes"] if session["notes"] else "—"
            notes = notes[:18].ljust(18)
            print(f"│ {date:<10} │ {subject} │ {hours} │ {activity} │ {notes} │")

        print("└────────────┴────────────────────────┴───────┴────────────────────────────┴────────────────────┘")

        index += page_size

        if index >= len(sorted_sessions):
            break

        while True:
            more = input("Show more sessions? (y/n): ").strip().lower()
            if more == "y":
                break
            elif more == "n":
                return
            else:
                print("Please enter 'y' or 'n'.")

    # Show summary once all pages have been displayed
    print("\n📊 Summary:")

    total_hours = sum(s["hours"] for s in sessions)
    total_sessions = len(sessions)
    avg_length = total_hours / total_sessions if total_sessions else 0

    activities = [s["activity"] for s in sessions]
    most_common_activity = Counter(activities).most_common(1)[0]

    subject_times = {}
    for s in sessions:
        subject_times[s["subject"]] = subject_times.get(s["subject"], 0) + s["hours"]

    most_studied = max(subject_times.items(), key=lambda item: item[1])

    print(f"• Total sessions this month: {total_sessions}")
    print(f"• Total study time: {total_hours:.1f} hours")
    print(f"• Average session length: {avg_length:.1f} hours")
    print(f"• Most frequent activity: {most_common_activity[0]} ({int((most_common_activity[1]/total_sessions)*100)}%)")
    print(f"• Most studied subject: {most_studied[0]} ({most_studied[1]:.1f} hours)")


# <------------------------------------------------------------- Monthly progress report ---------------------------------------->

from datetime import datetime
from calendar import monthrange

def monthly_progress_report(student_data):
    today = datetime.now()
    year = today.year
    month = today.strftime("%B")
    day = today.day
    days_in_month = monthrange(today.year, today.month)[1]
    progress_percent = int((day / days_in_month) * 100)

    print(f"\n=== MONTHLY PROGRESS REPORT ===\n")
    print(f"📅 {month} {year} Progress (Day {day} of {days_in_month})\n")

    # HEADER
    print("Subject Breakdown:")
    print("┌────────────────────────┬─────────┬─────────┬──────────┬──────────────┐")
    print("│ Subject                │ Current │ Goal    │ Progress │ Pace Status  │")
    print("├────────────────────────┼─────────┼─────────┼──────────┼──────────────┤")

    sessions = student_data["study_sessions"]
    goals = student_data["study_goals"]

    total_current = 0
    total_goal = 0

    pace_lines = []

    for subject in student_data["subjects"]:
        # Total study time for subject
        current_hours = sum(s["hours"] for s in sessions if s["subject"] == subject)
        goal_hours = goals.get(subject, 0)

        progress = (current_hours / goal_hours * 100) if goal_hours else 0
        total_current += current_hours
        total_goal += goal_hours

        # Pace status
        expected_progress = progress_percent
        pace_diff = progress - expected_progress

        if progress >= expected_progress + 5:
            pace = "🟢 Ahead"
        elif expected_progress - 5 <= progress < expected_progress + 5:
            pace = "🟡 On Track"
        else:
            pace = "🔴 Behind"

        print(f"│ {subject:<24} │ {current_hours:>6.1f}h │ {goal_hours:>6.1f}h │ {int(progress):>6}%  │ {pace:<12} │")

        # For recommendations
        remaining_days = days_in_month - day
        remaining = goal_hours - current_hours
        daily_target = remaining / remaining_days if remaining_days > 0 and remaining > 0 else 0
        pace_lines.append((subject, progress, daily_target, remaining))

    print("└────────────────────────┴─────────┴─────────┴──────────┴──────────────┘")

    # Overall progress
    overall_progress = (total_current / total_goal * 100) if total_goal else 0
    expected_total = (total_goal * progress_percent / 100)
    behind_by = expected_total - total_current

    print("\n📈 Progress Analysis:")
    print(f"• You're {progress_percent}% through the month")
    print(f"• Overall progress: {int(overall_progress)}% of total goals ({int(total_current)}/{int(total_goal)} hours)")
    print(f"• Expected progress at this point: {expected_total:.1f} hours")

    if behind_by > 0:
        print(f"• You're {behind_by:.1f} hours behind overall pace")
    else:
        print(f"• You're {abs(behind_by):.1f} hours ahead of pace 🎉")

    # Recommendations
    print("\n🎯 Recommendations:")
    for subject, progress, daily_target, remaining in pace_lines:
        if progress == 0:
            print(f"• URGENT: Start {subject} immediately (need {int(remaining)} hours in {days_in_month - day} days)")
        elif daily_target > 0:
            print(f"• {subject}: Need to study ~{daily_target:.1f} hours/day to stay on track")
        else:
            print(f"• {subject}: You're doing great! Maintain current pace")


# <------------------------------------------------- Analytics Dashboard Menu -------------------------------------------------------------->

def analytics_dashboard_menu(student_data):
    while True:
        print("\n=== 📊 ANALYTICS DASHBOARD ===")
        print("1. Performance Overview")
        print("2. Study Efficiency Analysis")
        print("3. Subject Comparison Report")
        print("4. Trend Predictions")
        print("5. Optimization Recommendations")
        print("6. Export Summary Report")
        print("7. Back to study session tracker")

        choice = input("Choice: ")

        if choice == "1":
            performance_overview(student_data)
        elif choice == "2":
            study_efficiency_analysis(student_data)
        elif choice == "3":
            subject_comparison_report(student_data)
        elif choice == "4":
            trend_predictions(student_data)
        elif choice == "5":
            optimization_recommendations(student_data)
        elif choice == "6":
            export_summary(student_data)
        elif choice == "7":
            break
        else:
            print("❗ Invalid input. Please choose a number from 1 to 7.")

# <-----------------------------------------------------choice 1 -  Performance overview ------------------------------------------------->

def performance_overview(student_data):
    import datetime

    print("\n=== PERFORMANCE OVERVIEW ===\n")
    print("📊 Academic Performance Summary:\n")

    subjects = student_data["subjects"]
    grades = student_data["grades"]
    sessions = student_data["study_sessions"]

    total_grades = []
    subject_hours = {subject: 0 for subject in subjects}

    # Calculate total hours per subject
    for session in sessions:
        subject = session["subject"]
        hours = session["hours"]
        if subject in subject_hours:
            subject_hours[subject] += hours

    # Gather grade data
    avg_per_subject = {}
    for subject in subjects:
        subject_grades = grades.get(subject, [])
        if subject_grades:
            avg = sum(subject_grades) / len(subject_grades)
            avg_per_subject[subject] = round(avg, 1)
            total_grades.extend(subject_grades)
        else:
            avg_per_subject[subject] = None

    # Total stats
    total_subjects = len(subjects)
    total_hours = sum(subject_hours.values())
    avg_all = round(sum(total_grades) / len(total_grades), 1) if total_grades else 0
    efficiency = round(sum(total_grades) / total_hours, 1) if total_hours > 0 else 0

    print("Overall Statistics:")
    print(f"• Total subjects: {total_subjects}")
    print(f"• Average grade across all subjects: {avg_all}")
    print(f"• Total study hours this month: {round(total_hours, 1)}")
    print(f"• Study efficiency: {efficiency} grade points per hour\n")

    print("Subject Performance:")
    print("┌─────────────────┬─────────┬─────────┬────────────┬──────────────┐")
    print("│ Subject         │ Average │ Hours   │ Efficiency │ Grade Trend  │")
    print("├─────────────────┼─────────┼─────────┼────────────┼──────────────┤")

    best_eff = -1
    best_eff_subject = ""
    highest_avg = -1
    highest_avg_subject = ""
    most_hours = -1
    most_hours_subject = ""

    for subject in subjects:
        avg = avg_per_subject[subject]
        hours = subject_hours[subject]
        eff = round(avg / hours, 1) if avg and hours > 0 else "--"
        trend = "No data"

        subj_grades = grades.get(subject, [])
        if len(subj_grades) >= 2:
            if subj_grades[-1] > subj_grades[0]:
                trend = "↗ Improving"
            elif subj_grades[-1] < subj_grades[0]:
                trend = "↘ Declining"
            else:
                trend = "➡ Stable"

        avg_display = f"{avg}" if avg is not None else "--"
        hours_display = f"{round(hours, 1)}"
        print(f"│ {subject:<15} │ {avg_display:^7} │ {hours_display:^7} │ {str(eff):^10} │ {trend:^12} │")

        if isinstance(eff, float) and eff > best_eff:
            best_eff = eff
            best_eff_subject = subject
        if avg is not None and avg > highest_avg:
            highest_avg = avg
            highest_avg_subject = subject
        if hours > most_hours:
            most_hours = hours
            most_hours_subject = subject

    print("└─────────────────┴─────────┴─────────┴────────────┴──────────────┘\n")

    print("🏆 Key Insights:")
    if best_eff_subject:
        print(f"• Most efficient subject: {best_eff_subject} ({best_eff} points/hour)")
    if highest_avg_subject:
        print(f"• Highest grade average: {highest_avg_subject} ({highest_avg})")
    if most_hours_subject:
        print(f"• Most time invested: {most_hours_subject} ({round(most_hours, 1)} hours)")

    # Detect improvement trend
    improving = [
        s for s in subjects
        if len(grades.get(s, [])) >= 2 and grades[s][-1] > grades[s][0]
    ]
    if improving:
        print(f"• Best improvement trend: {improving[0]}")

    print("\n⚠️ Areas for Attention:")
    for subject in subjects:
        if not grades.get(subject):
            print(f"• {subject}: No progress recorded yet")
        elif subject_hours[subject] > 0 and avg_per_subject[subject] is not None:
            eff = avg_per_subject[subject] / subject_hours[subject]
            if eff < 2.5:
                print(f"• {subject}: High time investment but lower efficiency")

# <<-------------------------------------------------------------- Choice 2 - Study efficiency analysis ----------------------------------------->

def study_efficiency_analysis(student_data):
    print("\n=== STUDY EFFICIENCY ANALYSIS ===\n")
    print("📈 Study Time vs Grade Correlation:\n")

    grades = student_data["grades"]
    sessions = student_data["study_sessions"]
    subjects = student_data["subjects"]

    activity_map = {
        "Reading textbook/materials": "Reading textbook",
        "Coding practice/exercises": "Coding practice",
        "Watching video lectures": "Video lectures",
        "Working on projects": "Projects",
        "Review/revision": "Review",
        "Other": "Other"
    }

    subject_hours = {s: 0 for s in subjects}
    activity_data = {}

    for session in sessions:
        subject = session["subject"]
        hours = session["hours"]
        activity = activity_map.get(session["activity"], session["activity"])

        subject_hours[subject] += hours

        if activity not in activity_data:
            activity_data[activity] = {"hours": 0, "grades": []}
        activity_data[activity]["hours"] += hours

        if "grade_context" in session:
            activity_data[activity]["grades"].append(session["grade_context"])

    for subject in subjects:
        subj_grades = grades.get(subject, [])
        hours = subject_hours[subject]
        print(f"{subject} Analysis:")
        print(f"• Study hours: {hours}")

        if len(subj_grades) >= 2:
            improvement = subj_grades[-1] - subj_grades[0]
            hours_per_point = round(hours / improvement, 1) if improvement != 0 else "--"
            rating = "⭐⭐⭐⭐⭐ Excellent" if hours_per_point < 2.5 else \
                     "⭐⭐⭐⭐ Very Good" if hours_per_point < 4 else \
                     "⭐⭐⭐ Good" if hours_per_point < 6 else "⭐ Needs Improvement"

            print(f"• Grade progression: {subj_grades} → {f'+{improvement}' if improvement >= 0 else improvement} points improvement")
            print(f"• Hours per grade point improvement: {hours_per_point} hours")
            print(f"• Efficiency rating: {rating}\n")
        elif len(subj_grades) == 1:
            print(f"• Only one grade recorded: {subj_grades[0]}")
            print("• Efficiency analysis requires at least two grades.\n")
        else:
            print("• No grades recorded yet.\n")

    # Activity Effectiveness Table
    print("📊 Activity Type Effectiveness:")
    print("┌─────────────────────┬───────┬─────────────┬────────────────────┐")
    print("│ Activity Type       │ Hours │ Avg Grade   │ Effectiveness      │")
    print("├─────────────────────┼───────┼─────────────┼────────────────────┤")

    for activity, data in activity_data.items():
        avg_grade = "--"
        if data["grades"]:
            avg_grade = round(sum(data["grades"]) / len(data["grades"]), 1)

        hours = round(data["hours"], 1)
        eff = ""
        if isinstance(avg_grade, float):
            eff = "⭐⭐⭐⭐⭐ Excellent" if avg_grade >= 90 else \
                  "⭐⭐⭐⭐ Very Good" if avg_grade >= 85 else \
                  "⭐⭐⭐ Good" if avg_grade >= 80 else "⭐ Needs Work"
        print(f"│ {activity:<20} │ {hours:^5} │ {avg_grade:^11} │ {eff:<18} │")
    print("└─────────────────────┴───────┴─────────────┴────────────────────┘")

    print("\n🎯 Optimization Recommendations:")
    print("• Focus more time on coding practice (highest effectiveness)")
    print("• Increase project-based learning")
    print("• Maintain current balance but add Statistics practice")
    print("• Consider shorter, more frequent video sessions\n")


# === 3. Subject Comparison Report ===
def subject_comparison_report(student_data):
    print("\n=== SUBJECT COMPARISON REPORT ===")
    print("{:<20} {:<10} {:<10} {:<15} {:<10}".format("Subject", "Avg", "Hours", "Efficiency", "Trend"))
    print("-" * 70)
    for subject in student_data["subjects"]:
        grades = student_data["grades"].get(subject, [])
        hours = sum(s["hours"] for s in student_data["study_sessions"] if s["subject"] == subject)
        average = round(sum(grades)/len(grades), 1) if grades else "--"
        trend = calculate_grade_trend(grades)
        improvement = (grades[-1] - grades[0]) if len(grades) >= 2 else None
        efficiency = round(improvement / hours, 1) if improvement and hours else "--"
        print(f"{subject:<20} {average:<10} {hours:<10.1f} {efficiency:<15} {trend:<10}")


# === 4. Trend Predictions ===
def trend_predictions(student_data, current_day=20, days_in_month=31):
    print("\n=== TREND PREDICTIONS ===")
    remaining_days = days_in_month - current_day
    print(f"\n📅 Current Day: {current_day} of {days_in_month}")
    for subject in student_data["subjects"]:
        total_goal = student_data["study_goals"].get(subject, 0)
        hours_done = sum(s["hours"] for s in student_data["study_sessions"] if s["subject"] == subject)
        pace = hours_done / current_day if current_day else 0
        predicted = round(pace * days_in_month, 1)
        percent = round((hours_done / total_goal) * 100, 1) if total_goal else 0
        status = "✅ On Track" if predicted >= total_goal else "⚠️ Off Track"
        print(f"\n{subject} ➤ {hours_done}/{total_goal}h done ({percent}%)")
        print(f"Projected: {predicted}h by end of month → {status}")


# === 5. Optimization Recommendations ===
def optimization_recommendations(student_data):
    print("\n=== OPTIMIZATION RECOMMENDATIONS ===")
    activity_totals = {}
    for session in student_data["study_sessions"]:
        activity = session["activity"]
        activity_totals[activity] = activity_totals.get(activity, 0) + session["hours"]

    if not activity_totals:
        print("No study session data found.")
        return

    sorted_activities = sorted(activity_totals.items(), key=lambda x: x[1], reverse=True)
    print("\n📊 Activity Time Summary:")
    for act, hrs in sorted_activities:
        print(f"• {act}: {hrs:.1f} hours")

    top = sorted_activities[0][0]
    print(f"\n📌 Suggested Focus:")
    print(f"→ Spend more time on '{top}', as it's currently the most consistent method.")


# === 6. Export Summary Report ===
import json

def export_summary(student_data):
    try:
        with open("student_summary.json", "w") as f:
            json.dump(student_data, f, indent=4)
        print("\n✅ Summary exported to 'student_summary.json'!")
    except Exception as e:
        print(f"❌ Export failed: {e}")


# === Helper function for grade trend ===
def calculate_grade_trend(grades):
    if len(grades) < 2:
        return "No data"
    diff = grades[-1] - grades[0]
    if diff > 2:
        return "↗ Improving"
    elif diff < -2:
        return "↘ Declining"
    else:
        return "➡ Stable"
    





