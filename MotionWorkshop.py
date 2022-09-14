from gui.UserInterface import UserInterface
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


def main():
    # Tkinter Main Loop
    user_interface.root.after(user_interface.update_loop_time, user_interface.startup)
    user_interface.root.mainloop()


if __name__ == "__main__":
    # Create Global Instances of Class Objects
    connection_manager = ConnectionManagement()
    application_settings = ApplicationSettings()
    motion = Motion()
    user_interface = UserInterface()

    main()
