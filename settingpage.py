import customtkinter
import drivepage


class SettingPage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # configure grid layout (4x4)

        self.grid_columnconfigure(list(range(0, 40)), weight=1)
        self.grid_rowconfigure(list(range(0, 40)), weight=1)
        self.configure(fg_color="transparent", bg_color="transparent")

        # create main entry
        self.setting_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.setting_frame.grid(row=0, column=0, rowspan=39, columnspan=40,
                                sticky="nsew")  # row와 column은 frame을 위치시키는 지점
        self.setting_frame.grid_rowconfigure(list(range(0, 24)), weight=1)
        self.setting_frame.grid_columnconfigure(list(range(0, 40)), weight=1)
        self.logo_label = customtkinter.CTkLabel(self.setting_frame, text="Setting",
                                                 font=customtkinter.CTkFont(size=50, weight="bold"))
        self.logo_label.grid(row=0, column=20, padx=0, pady=(20, 10))

        # 다크모드 설정
        self.appearance_mode_label = customtkinter.CTkLabel(self.setting_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=8, padx=0, pady=(10, 0), sticky="n")
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.setting_frame,
                                                                      values=["Light", "Dark"],
                                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.set("Dark")
        self.appearance_mode_optionmenu.grid(row=7, column=8, padx=0, pady=10, sticky="n")

        # UI Scaling
        self.scaling_label = customtkinter.CTkLabel(self.setting_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=15, column=8, padx=0, pady=(10, 0), sticky="n")
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.setting_frame,
                                                              values=["80%", "90%", "100%", "110%", "120%"],
                                                              command=self.change_scaling_event)
        self.scaling_optionmenu.grid(row=17, column=8, padx=0, pady=(10, 20), sticky="n")
        self.scaling_optionmenu.set("100%")

        # 테마 선택
        self.theme_label = customtkinter.CTkLabel(self.setting_frame, text="Select Theme:", anchor="w")
        self.theme_label.grid(row=5, column=24, padx=0, pady=(10, 0), sticky="n")
        self.theme_optionmenu = customtkinter.CTkOptionMenu(self.setting_frame,
                                                            values=["blue", "green"],
                                                            command=self.change_default_color_theme_event)
        self.theme_optionmenu.set("blue")
        self.theme_optionmenu.grid(row=7, column=24, padx=0, pady=10, sticky="n")

        # 폰트 선택
        self.font_label = customtkinter.CTkLabel(self.setting_frame, text="Select Font", anchor="w")
        self.font_label.grid(row=15, column=24, padx=0, pady=(10, 0), sticky="n")
        self.font_optionmenu = customtkinter.CTkOptionMenu(self.setting_frame, dynamic_resizing=False,
                                                           values=["Value 1", "Value 2", "Value"])
        self.font_optionmenu.grid(row=17, column=24, padx=0, pady=(10, 20), sticky="n")

        # new
        self.bottombar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.bottombar_frame.grid(row=39, column=0, columnspan=41, sticky="news")
        self.bottombar_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.bottombar_frame.grid_rowconfigure(0, weight=1)

        self.bottombar_button_1 = customtkinter.CTkButton(self.bottombar_frame, text="주행", corner_radius=0,
                                                          font=customtkinter.CTkFont(size=20, weight="bold"),
                                                          command=lambda: parent.switch_frame(drivepage.DrivePage))
        self.bottombar_button_1.grid(row=0, column=0, padx=1, sticky="news")  # padx 버튼 사이 간격

        self.bottombar_button_2 = customtkinter.CTkButton(self.bottombar_frame, text="랩타임측정", corner_radius=0,
                                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bottombar_button_2.grid(row=0, column=1, padx=1, sticky="news")
        self.bottombar_button_3 = customtkinter.CTkButton(self.bottombar_frame, text="엔진출력", corner_radius=0,
                                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bottombar_button_3.grid(row=0, column=2, padx=1, sticky="news")
        self.bottombar_button_4 = customtkinter.CTkButton(self.bottombar_frame, text="설정", corner_radius=0,
                                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bottombar_button_4.grid(row=0, column=3, padx=1, sticky="news")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def change_default_color_theme_event(self, new_default_color_theme: str):
        customtkinter.set_default_color_theme(new_default_color_theme)
