import customtkinter
import drivepage
import settingpage
import PIL

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("RPI-Datalogger Project.py")
        self.geometry(f"{800}x{480}")
        self._frame = None
        self.switch_frame(drivepage.DrivePage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill='both', expand="True")


if __name__ == "__main__":
    app = App()
    # app.after(10000, app.after_test())
    app.mainloop()
