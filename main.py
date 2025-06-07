from data_handler import load_user_data, save_user_data
from dashboard import show_dashboard
import mainfunctions as mf

def main():
    student_data, is_new = load_user_data(
        add_subject_func=mf.add_subject,
        display_profile_func=mf.display_profile,
        subject_menu_func=mf.subject_menu
    )

    if is_new:
        # new users: go into the old menu
        mf.main_menu(student_data)
    else:
        # returning users: ONLY show the new dashboard loop
        show_dashboard(student_data)
        

    save_user_data(student_data)

if __name__ == "__main__":
    main()
