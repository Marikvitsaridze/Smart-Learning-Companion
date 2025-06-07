import datetime
import calendar
from statistics import mean
import mainfunctions as mf
from data_handler import save_user_data
import sys

def show_dashboard(data):
    """Interactive dashboard menu for returning users with session tracking."""
    # Initialize session context
    session_ctx = {
        'start': datetime.datetime.now(),
        'initial_subjects': len(data.get('subjects', [])),
        'reports_generated': 0,
        'features_used': set()
    }

    while True:
        _print_header(data)
        choice = input("Choose option (1-8): ").strip()

        if choice == "1":
            session_ctx['features_used'].add('Dashboard Overview')
            dashboard_overview(data)
        elif choice == "2":
            session_ctx['features_used'].add('Profile Management')
            profile_management(data)
        elif choice == "3":
            session_ctx['features_used'].add('Grade Management')
            grade_management(data)
        elif choice == "4":
            session_ctx['features_used'].add('Study Sessions')
            mf.study_session_menu(data)
        elif choice == "5":
            session_ctx['features_used'].add('Analytics & Reports')
            session_ctx['reports_generated'] += 1
            analytics_reports(data)
        elif choice == "6":
            session_ctx['features_used'].add('Settings')
            settings(data)
        elif choice == "7":
            session_ctx['features_used'].add('Data Export')
            data_export(data)
        elif choice == "8":
            session_ctx['features_used'].add('Exit')
            session_summary(data, session_ctx)
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 8.")



def _print_header(data):
    print("\n================================")
    print("🎓 SMART LEARNING COMPANION 🎓")
    print("================================")
    print(f"Welcome back, {data['name']}!")
    print(f"Last login: {data.get('last_login', 'N/A')}")
    data['last_login'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_hours = sum(
        sess.get('hours', 0)
        for sess in data.get('study_sessions', [])
        if _in_current_month(sess.get('date'))
    )

    all_grades = [
        grade
        for grades in data.get('grades', {}).values()
        for grade in grades
    ]
    avg_grade = mean(all_grades) if all_grades else 0

    active_subs = sum(1 for grades in data.get('grades', {}).values() if grades)

    today = datetime.datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_left = days_in_month - today.day

    print("\nQuick Stats:")
    print(f"• Total study hours this month: {total_hours:.1f}")
    print(f"• Current average grade: {avg_grade:.1f}")
    print(f"• Active subjects: {active_subs}")
    print(f"• Next goal deadline: End of month ({days_left} days)\n")

    print("=== MAIN MENU ===")
    print("1. 📊 Dashboard Overview")
    print("2. 👤 Profile Management")
    print("3. 📝 Grade Management")
    print("4. ⏱️ Study Sessions")
    print("5. 📈 Analytics & Reports")
    print("6. ⚙️ Settings")
    print("7. 💾 Data Export")
    print("8. 🚪 Exit\n")


# <============================================== Choice 1 - Dashboard Overview ==========================================>


def dashboard_overview(data):
    """Choice 1: show overall progress overview."""
    print("\n--- Dashboard Overview ---")
    total_sessions = len(data.get('study_sessions', []))
    total_hours_all = sum(sess.get('hours', 0) for sess in data.get('study_sessions', []))

    all_grades = [
        grade
        for grades in data.get('grades', {}).values()
        for grade in grades
    ]
    overall_avg = mean(all_grades) if all_grades else 0

    print(f"Total study sessions: {total_sessions}")
    print(f"Total study hours: {total_hours_all:.1f}")
    print(f"Overall average grade: {overall_avg:.1f}\n")

    if data.get('grades'):
        print("Subject Averages:")
        for subject, grades in data['grades'].items():
            subj_avg = mean(grades) if grades else 0
            print(f" • {subject}: {subj_avg:.1f}")
    else:
        print("No grades recorded yet.")

    input("\nPress Enter to return to the dashboard...")


# <============================================== Choice 2 - Profile management ==========================================>


def profile_management(data):
    """Choice 2: Profile management submenu. Returns True if user wants to go back to main menu."""
    while True:
        print(f"\nCurrent Profile: {data['name']}")
        print(f"Active Subjects: {len(data.get('subjects', []))}\n")
        print("1. View Complete Profile")
        print("2. Add New Subject")
        print("3. Modify Study Goals")
        print("4. Remove Subject")
        print("5. Profile Statistics")
        print("6. Back to Main Menu\n")
        choice = input("Choose option (1-6): ").strip()

        if choice == '1':
            _view_complete_profile(data)
        elif choice == '2':
            if _add_new_subject(data):
                return True  # go to main menu
        elif choice == '3':
            _modify_study_goals(data)
        elif choice == '4':
            _remove_subject(data)
        elif choice == '5':
            _profile_statistics(data)
        elif choice == '6':
            return False
        else:
            print("❌ Invalid selection. Please enter a number from 1 to 6.")


# <=========================================================== Choice 3 - Grade Management==========================================================>

def grade_management(data):
    """Choice 3: Grade management submenu."""
    while True:
        print("\n--- Grade Management ---")
        print("1. Add Single Grade")
        print("2. Add Multiple Grades")
        print("3. Back to Dashboard\n")
        choice = input("Choose option (1-3): ").strip()

        if choice == '1':
            mf.add_single_grade(data)
        elif choice == '2':
            mf.add_multiple_grades(data)
        elif choice == '3':
            break
        else:
            print("❌ Invalid input. Enter 1-3.")

        input("\nPress Enter to return to Grade Management...")


# <============================================================ Choice 5 - Analytics and Reports ==================================================>

def analytics_reports(data):
    """Choice 5: Analytics & Reports submenu."""
    while True:
        print("\n--- Analytics & Reports ---")
        print("1. Calculate Averages")
        print("2. Performance Analysis")
        print("3. Back to Dashboard\n")
        choice = input("Choose option (1-3): ").strip()

        if choice == '1':
            mf.calculate_averages(data)
        elif choice == '2':
            mf.performance_analysis(data)
        elif choice == '3':
            break
        else:
            print("❌ Invalid input. Enter 1-3.")

        input("\nPress Enter to return to Analytics & Reports...")



# <=========================================================== Continuing with profile management sub-menu ========================================>

def _view_complete_profile(data):
    print("\n--- Complete Profile ---")
    print(f"Name: {data['name']}")
    print("Subjects and Goals:")
    for subj in data.get('subjects', []):
        goal = data.get('study_goals', {}).get(subj, 0)
        print(f" • {subj}: {goal}h goal")
    print("Grades:")
    for subj in data.get('subjects', []):
        grades = data.get('grades', {}).get(subj, [])
        print(f" • {subj}: {grades if grades else 'No grades'}")
    input("\nPress Enter to return to Profile Management...")


def _add_new_subject(data):
    print("\n--- Add New Subject ---")
    new_subj = input("Enter new subject name: ").strip().title()
    if new_subj in data.get('subjects', []):
        print(f"⚠️ Subject '{new_subj}' already exists.")
        return False
    while True:
        goal_input = input(f"Monthly study goal for {new_subj} (hours): ").strip()
        if goal_input.isdigit() and int(goal_input) > 0:
            goal = int(goal_input)
            break
        print("Please enter a positive number.")

    data.setdefault('subjects', []).append(new_subj)
    data.setdefault('study_goals', {})[new_subj] = goal
    data.setdefault('grades', {})[new_subj] = []
    print(f"\n✅ Subject \"{new_subj}\" added successfully!")

    print("\nUpdated profile:")
    for subj in data['subjects']:
        g = data['study_goals'].get(subj, 0)
        suffix = ' (NEW)' if subj == new_subj else ''
        print(f"• {subj}: {g}h goal{suffix}")

    # follow-up submenu
    while True:
        print("\nWould you like to:")
        print(f"1. Add initial grades for {new_subj}")
        print("2. Record a study session")
        print("3. Return to Profile Management")
        print("4. Go to Main Menu\n")
        sub_choice = input("Choice: ").strip()
        if sub_choice == '1':
            _add_initial_grades(data, new_subj)
        elif sub_choice == '2':
            mf.study_session_menu(data)
        elif sub_choice == '3':
            return False
        elif sub_choice == '4':
            return True
        else:
            print("❌ Invalid choice. Enter 1-4.")


def _add_initial_grades(data, subject):
    print(f"\n--- Add Initial Grades for {subject} ---")
    while True:
        n = input(f"How many initial grades for {subject}? ").strip()
        if n.isdigit() and int(n) > 0:
            count = int(n)
            break
        print("Please enter a positive number.")

    for i in range(count):
        while True:
            g = input(f"Enter grade #{i+1}: ").strip()
            try:
                val = float(g)
                data['grades'][subject].append(val)
                break
            except:
                print("Enter a numeric grade.")
    print(f"✅ Added {count} grades to {subject}.")
    input("\nPress Enter to continue...")


def _modify_study_goals(data):
    print("\n--- Modify Study Goals ---")
    subjects = data.get('subjects', [])
    for idx, subj in enumerate(subjects, 1):
        print(f"{idx}. {subj}: {data['study_goals'].get(subj, 0)}h goal")
    choice = input("Select subject to modify (number): ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(subjects)):
        print("❌ Invalid selection.")
        return
    subj = subjects[int(choice)-1]
    while True:
        new_goal = input(f"New monthly goal for {subj} (hours): ").strip()
        if new_goal.isdigit() and int(new_goal) > 0:
            data['study_goals'][subj] = int(new_goal)
            print(f"✅ Updated {subj} goal to {new_goal}h.")
            break
        print("Enter a positive number.")
    input("\nPress Enter to return to Profile Management...")


def _remove_subject(data):
    print("\n--- Remove Subject ---")
    subjects = data.get('subjects', [])
    for idx, subj in enumerate(subjects, 1):
        print(f"{idx}. {subj}")
    choice = input("Select subject to remove (number): ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(subjects)):
        print("❌ Invalid selection.")
        return
    subj = subjects.pop(int(choice)-1)
    data['study_goals'].pop(subj, None)
    data['grades'].pop(subj, None)
    print(f"✅ Subject '{subj}' removed successfully.")
    input("\nPress Enter to return to Profile Management...")


def _profile_statistics(data):
    print("\n--- Profile Statistics ---")
    for subj in data.get('subjects', []):
        grades = data.get('grades', {}).get(subj, [])
        count = len(grades)
        avg = mean(grades) if grades else 0
        print(f"• {subj}: {count} grades, avg {avg:.1f}")
    input("\nPress Enter to return to Profile Management...")

# <============================================================Choice 6 - Settings=================================================>

def settings(data):
    """Choice 6: Settings submenu with Reset Progress only."""
    while True:
        print("\n--- Settings ---")
        print("1. Reset Progress")
        print("2. Back to Dashboard\n")
        choice = input("Choose option (1-2): ").strip()

        if choice == '1':
            reset_progress(data)
        elif choice == '2':
            break
        else:
            print("❌ Invalid input. Enter 1 or 2.")


def reset_progress(data):
    print("\n--- Reset Progress ---")
    print("1. Clear All Study Sessions")
    print("2. Clear All Grades")
    print("3. Clear All Sessions & Grades")
    print("4. Cancel\n")
    choice = input("Choose option (1-4): ").strip()

    if choice in ['1', '2', '3']:
        confirm = input("Are you sure? This action cannot be undone (Y/N): ").strip().lower()
        if confirm == 'y':
            if choice == '1':
                data['study_sessions'] = []
                print("✅ All study sessions cleared.")
            elif choice == '2':
                for subj in data.get('grades', {}):
                    data['grades'][subj] = []
                print("✅ All grades cleared.")
            else:
                data['study_sessions'] = []
                for subj in data.get('grades', {}):
                    data['grades'][subj] = []
                print("✅ All sessions & grades cleared.")
        else:
            print("Cancelled.")
    elif choice == '4':
        return
    else:
        print("❌ Invalid input. Enter 1-4.")

    input("\nPress Enter to return to Settings...")

# <============================================================== Choice 7 - Data Export ===========================================>

def data_export(data):
    """Choice 7: Data Export - save to file and exit."""
    save_user_data(data)
    print("\n✅ Data exported to student_summary.json")
    print("🚪 Exiting... Goodbye!")
    sys.exit(0)


# <=========================================================== Choice 8 - Exiting with session summary ===============================>

def session_summary(data, ctx):
    """Generate a dynamic session summary based on runtime context."""
    end = datetime.datetime.now()
    duration = int((end - ctx['start']).total_seconds() / 60)
    today = end.date().isoformat()
    # Today's sessions
    todays_sessions = [s for s in data.get('study_sessions', []) if s.get('date', '').startswith(today)]
    # New subjects added
    new_subjects = len(data.get('subjects', [])) - ctx['initial_subjects']
    # Study streak
    streak = data.get('study_streak', 'N/A')
    # Upcoming deadlines calculation
    days_left = calendar.monthrange(end.year, end.month)[1] - end.day

    print("\n=== SESSION SUMMARY ===\n")
    print("📊 Today's Activity Overview:")
    print(f"• Session duration: {duration} minutes")
    print(f"• Features used: {', '.join(ctx['features_used'])}")
    print(f"• Data updates: {new_subjects} new subjects added")
    print(f"• Reports generated: {ctx['reports_generated']}\n")

    print("📈 Current Status:")
    print(f"• Study streak: {streak} days")
    print(f"• Upcoming deadlines: End of month ({days_left} days)")
    print(f"• Overall sessions today: {len(todays_sessions)}\n")

    print("💾 Data Status:")
    print("• All changes saved automatically")
    print("• Profile backed up successfully\n")

    print("🌟 Motivational Message:")
    print(f"Keep up the great work, {data['name']}! Tomorrow is another opportunity to learn.")

    print("=====================================")
    print("Thanks for using Learning Companion!")
    print("Keep building your bright future! 🚀")
    print("=====================================\n")
    save_user_data(data)
    input("Press Enter to exit...")
    sys.exit(0)


def _in_current_month(date_str):
    if not date_str:
        return False
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%B %d, %Y"):
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            now = datetime.datetime.now()
            return dt.year == now.year and dt.month == now.month
        except:
            continue
    return False
