import threading
from gui.UserInterface import UserInterface
from motion.Motion import Motion
from utility.ConnectionManagement import ConnectionManagement
from utility.ApplicationSettings import ApplicationSettings


def main():
    # Start Update Thread
    update_thread = threading.Thread(target=user_interface.update_loop, daemon=True)

    # Tkinter Main Loop
    user_interface.root.after(user_interface.update_loop_time, lambda: user_interface.startup(update_thread))
    user_interface.root.mainloop()


if __name__ == "__main__":
    # Create Global Instances of Class Objects
    connection_manager = ConnectionManagement()
    application_settings = ApplicationSettings()
    motion = Motion()
    user_interface = UserInterface(connection_manager, application_settings, motion)

    main()
