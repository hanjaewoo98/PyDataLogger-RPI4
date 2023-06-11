import customtkinter
import settingpage
import obd
from tkdial import ScrollKnob
import pandas as pd
import tkinter as tk
import main
import PIL
import re

is_recording = False


class DrivePage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # obd 초기화
        obd.logger.setLevel(obd.logging.DEBUG)
        self.ports = obd.scan_serial()
        self.connection = obd.OBD(portstr=self.ports[0], baudrate=38400, fast=False, timeout=10)

        # lables 초기화
        self.labels = {}
        # RPM, 속도, 흡기온, 촉매온도, 유온, 공기온, 유압, 엔진가동시간
        self.label_texts = {
            "RPM": "RPM",  # RPM, 가져와짐
            "SPEED": "SPEED",  # 속도, 가져와짐
            "CATALYST_TEMP_B1S1": "CATALYST_TEMP_B1S1",  # 촉매온도, 가져와짐
            # "OIL_TEMP": "OIL_TEMP",  # 유온, 안가져와짐
            "INTAKE_TEMP": "INTAKE_TEMP",  # 흡기온, 가져와짐
            "INTAKE_PRESSURE": "INTAKE_PRESSURE",  # 매니폴드압,가져와짐
            "RUN_TIME": "RUN_TIME",  # 가동시간, 가져와짐
            "COOLANT_TEMP": "COOLANT_TEMP",  # 냉각수온도, 가져와짐
            "THROTTLE_POS": "THROTTLE_POS",  # 스로틀위치, 가져와짐
            "ENGINE_LOAD": "ENGINE_LOAD",  # 엔진부하, 가져와짐
        }

        for key, text in self.label_texts.items():
            label = customtkinter.CTkLabel(self)
            self.labels[key] = label

        # pandas 초기화
        self.df = pd.DataFrame()
        self.is_recording = False

        # configure grid layout (40x40)
        self.grid_columnconfigure(list(range(0, 40)), weight=1)
        self.grid_rowconfigure(list(range(0, 40)), weight=1)
        self.configure(fg_color="transparent", bg_color="transparent")

        # new bottom Frame
        self.bottombar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.bottombar_frame.grid(row=39, column=0, columnspan=40, sticky="news")
        # column_configure는 그리드 내부의 값들에게 영향을 준다.
        self.bottombar_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.bottombar_frame.grid_rowconfigure(0, weight=1)

        self.bottombar_button_1 = customtkinter.CTkButton(self.bottombar_frame, text="주행", corner_radius=0,
                                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bottombar_button_1.grid(row=0, column=0, padx=1, sticky="news")

        self.bottombar_button_2 = customtkinter.CTkButton(self.bottombar_frame, text="랩타임측정", corner_radius=0,
                                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bottombar_button_2.grid(row=0, column=1, padx=1, sticky="news")
        self.bottombar_button_3 = customtkinter.CTkButton(self.bottombar_frame, text="엔진출력", corner_radius=0,
                                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bottombar_button_3.grid(row=0, column=2, padx=1, sticky="news")
        self.bottombar_button_4 = customtkinter.CTkButton(self.bottombar_frame, text="설정", corner_radius=0,
                                                          font=customtkinter.CTkFont(size=20, weight="bold"),
                                                          command=lambda: parent.switch_frame(settingpage.SettingPage))
        self.bottombar_button_4.grid(row=0, column=3, padx=1, sticky="news")

        # 간격
        pad_value = 7
        # # 좌측 값들
        #
        # self.leftbar_frame = customtkinter.CTkFrame(self)
        # self.leftbar_frame.grid(row=0, column=0, rowspan=39, columnspan=2, sticky="news", pady=20, padx=20)
        # self.leftbar_frame.grid_columnconfigure(list(range(0, 2)), weight=1)
        # self.leftbar_frame.grid_rowconfigure(list(range(0, 40)), weight=1)
        #
        # # self.left_label_1_1 = customtkinter.CTkLabel(self.leftbar_frame, text="45℃", width=100,
        # #                                             font=customtkinter.CTkFont(size=40, weight="bold"))
        # self.labels["INTAKE_TEMP"] = customtkinter.CTkLabel(self.leftbar_frame, width=100,
        #                                                     font=customtkinter.CTkFont(size=40, weight="bold"))
        # self.labels["INTAKE_TEMP"].grid(row=10, column=0, padx=10, sticky="nws")
        # self.left_label_1_2 = customtkinter.CTkLabel(self.leftbar_frame, text="흡기온도(℃)", width=50,
        #                                              font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.left_label_1_2.grid(row=10, column=1, padx=10, sticky="ws")
        #
        # self.labels["CATALYST_TEMP_B1S1"] = customtkinter.CTkLabel(self.leftbar_frame, width=100,
        #                                                            font=customtkinter.CTkFont(size=40, weight="bold"))
        # self.labels["CATALYST_TEMP_B1S1"].grid(row=10 + pad_value, column=0, padx=10, sticky="nws")
        # self.left_label_2_2 = customtkinter.CTkLabel(self.leftbar_frame, text="촉매온도(℃)", width=50,
        #                                              font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.left_label_2_2.grid(row=10 + pad_value, column=1, padx=10, sticky="ws")
        #
        #
        #
        # self.left_label_3_1 = customtkinter.CTkLabel(self.leftbar_frame, width=100,
        #                                              font=customtkinter.CTkFont(size=40, weight="bold"))
        # self.left_label_3_1.grid(row=10 + pad_value * 2, column=0, padx=10, sticky="nws")
        #
        #
        #
        #
        # self.labels["COOLANT_TEMP"] = customtkinter.CTkLabel(self.leftbar_frame, width=50,
        #                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.labels["COOLANT_TEMP"].grid(row=10 + pad_value * 2, column=0, padx=10, sticky="nws")
        # self.left_label_3_2 = customtkinter.CTkLabel(self.leftbar_frame, text="냉각수온(℃)", width=50,
        #                                              font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.left_label_3_2.grid(row=10 + pad_value * 2, column=1, padx=10, sticky="ws")

        self.leftbar_frame = customtkinter.CTkFrame(self)
        self.leftbar_frame.grid(row=0, column=0, rowspan=39, columnspan=2, sticky="news", pady=20, padx=20)
        self.leftbar_frame.grid_columnconfigure(list(range(0, 2)), weight=1)
        self.leftbar_frame.grid_rowconfigure(list(range(0, 40)), weight=1)

        self.labels["ENGINE_LOAD"] = customtkinter.CTkLabel(self.leftbar_frame, width=100,
                                                            font=customtkinter.CTkFont(size=40, weight="bold"))
        self.labels["ENGINE_LOAD"].grid(row=10, column=0, padx=10, sticky="nws")
        self.left_label_1_2 = customtkinter.CTkLabel(self.leftbar_frame, text="엔진부하(%)", width=50,
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.left_label_1_2.grid(row=10, column=1, padx=10, sticky="ws")

        self.labels["CATALYST_TEMP_B1S1"] = customtkinter.CTkLabel(self.leftbar_frame, width=100,
                                                                   font=customtkinter.CTkFont(size=40, weight="bold"))
        self.labels["CATALYST_TEMP_B1S1"].grid(row=10 + pad_value, column=0, padx=10, sticky="nws")
        self.left_label_2_2 = customtkinter.CTkLabel(self.leftbar_frame, text="촉매온도(℃)", width=50,
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.left_label_2_2.grid(row=10 + pad_value, column=1, padx=10, sticky="ws")

        self.labels["COOLANT_TEMP"] = customtkinter.CTkLabel(self.leftbar_frame, width=100,
                                                             font=customtkinter.CTkFont(size=40, weight="bold"))
        self.labels["COOLANT_TEMP"].grid(row=10 + pad_value * 2, column=0, padx=10, sticky="nws")
        self.left_label_3_2 = customtkinter.CTkLabel(self.leftbar_frame, text="냉각수온(℃)", width=50,
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.left_label_3_2.grid(row=10 + pad_value * 2, column=1, padx=10, sticky="ws")

        # 우측 값들
        self.rightbar_frame = customtkinter.CTkFrame(self)
        self.rightbar_frame.grid(row=0, column=38, rowspan=39, columnspan=2, sticky="news", pady=20, padx=20)
        self.rightbar_frame.grid_columnconfigure(list(range(0, 2)), weight=1)
        self.rightbar_frame.grid_rowconfigure(list(range(0, 40)), weight=1)

        self.labels["INTAKE_TEMP"] = customtkinter.CTkLabel(self.rightbar_frame, width=100,
                                                            font=customtkinter.CTkFont(size=40, weight="bold"))
        # self.right_label_1_1 = customtkinter.CTkLabel(self.rightbar_frame, width=100,
        #                                              font=customtkinter.CTkFont(size=40, weight="bold"))
        self.labels["INTAKE_TEMP"].grid(row=10, column=0, padx=10, sticky="nes")
        self.right_label_1_2 = customtkinter.CTkLabel(self.rightbar_frame, text="공기온(℃)", width=50,
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.right_label_1_2.grid(row=10, column=1, padx=10, sticky="es")

        # self.right_label_2_1 = customtkinter.CTkLabel(self.rightbar_frame, text="120", width=100,
        #                                              font=customtkinter.CTkFont(size=40, weight="bold"))
        self.labels["INTAKE_PRESSURE"] = customtkinter.CTkLabel(self.rightbar_frame, width=100,
                                                                font=customtkinter.CTkFont(size=40, weight="bold"))
        self.labels["INTAKE_PRESSURE"].grid(row=10 + pad_value, column=0, padx=10, sticky="nes")
        self.right_label_2_2 = customtkinter.CTkLabel(self.rightbar_frame, text="흡기압(kPa)", width=50,
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.right_label_2_2.grid(row=10 + pad_value, column=1, padx=10, sticky="es")

        self.labels["RUN_TIME"] = customtkinter.CTkLabel(self.rightbar_frame, width=100,
                                                         font=customtkinter.CTkFont(size=40, weight="bold"))
        # self.right_label_3_1 = customtkinter.CTkLabel(self.rightbar_frame, text="20.6", width=100,
        #                                              font=customtkinter.CTkFont(size=40, weight="bold"))
        self.labels["RUN_TIME"].grid(row=10 + pad_value * 2, column=0, padx=10, sticky="nes")
        self.right_label_3_2 = customtkinter.CTkLabel(self.rightbar_frame, text="시간(sec)", width=50,
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.right_label_3_2.grid(row=10 + pad_value * 2, column=1, padx=10, sticky="es")

        # 중앙값들
        # self.centerbar_frame = customtkinter.CTkFrame(self)
        # self.centerbar_frame.grid(row = 0, column = 2, rowspan = 39, columnspan = 36, sticky = "news", pady = 20)
        # self.centerbar_frame.grid_columnconfigure(list(range(0,3)), weight=1)
        # self.centerbar_frame.grid_rowconfigure(list(range(0,10)), weight=1)

        # 중앙 다이얼
        self.center_meter = ScrollKnob(self, text="", start=-1, end=9000, steps=1, radius=250, bar_color="#1F6AA5",
                                       progress_color="white", outer_length=0,
                                       border_width=30, start_angle=250, inner_width=0, outer_width=5,
                                       text_font=customtkinter.CTkFont(size=20, weight="bold")
                                       )
        self.meter_bg_change()
        self.center_meter.grid(row=10, column=19)
        # self.center_slider = customtkinter.CTkSlider(self, from_=0, to=9000, number_of_steps=9000)
        # self.center_slider.grid(row=11, column=19)

        self.center_label_frame = customtkinter.CTkLabel(self)
        self.center_label_frame.grid(row=12, column=2, rowspan=24, columnspan=36, sticky="news")
        self.center_label_frame.grid_rowconfigure(list(range(4)), weight=1)
        self.center_label_frame.grid_columnconfigure(list(range(2)), weight=1)

        self.labels["RPM"] = customtkinter.CTkLabel(self.center_label_frame,
                                                    font=customtkinter.CTkFont(size=50, weight="bold"))
        # self.center_label_1_1 = customtkinter.CTkLabel(self.center_label_frame, text="0",
        #                                               font=customtkinter.CTkFont(size=50, weight="bold"))
        self.labels["RPM"].grid(row=0, column=0, sticky="news")
        self.center_label_1_2 = customtkinter.CTkLabel(self.center_label_frame, text="RPM",
                                                       font=customtkinter.CTkFont(size=30, weight="bold"))
        self.center_label_1_2.grid(row=0, column=1, sticky="news")

        self.labels["SPEED"] = customtkinter.CTkLabel(self.center_label_frame,
                                                      font=customtkinter.CTkFont(size=50, weight="bold"))
        # self.center_label_2_1 = customtkinter.CTkLabel(self.center_label_frame, text="30",
        #                                               font=customtkinter.CTkFont(size=50, weight="bold"))
        self.labels["SPEED"].grid(row=1, column=0, sticky="news")
        self.center_label_2_2 = customtkinter.CTkLabel(self.center_label_frame, text="km/h",
                                                       font=customtkinter.CTkFont(size=30, weight="bold"))
        self.center_label_2_2.grid(row=1, column=1, sticky="news")

        # 슬라이더 테스트
        # self.center_slider.configure(command=self.test_label_change)
        # self.bind("<FocusIn>", self.meter_bg_change)

        # after 테스트
        # self.after_test1()
        self.start_recording()

    def test_label_change(self, value):
        self.labels["RPM"].configure(text=round(value))
        self.center_meter.set(value)

    # Custom Tkiner 호환용 함수(배경색 맞추기)
    def meter_bg_change(self):
        print(customtkinter.get_appearance_mode())
        if customtkinter.get_appearance_mode() == "Light":
            self.center_meter.configure(bg="#EBEBEB")
        elif customtkinter.get_appearance_mode() == "Dark":
            self.center_meter.configure(bg="#242424")

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def obd_update(self):
        # Reads OBD-II data and displays it on the labels.
        for key, label in self.labels.items():
            response = self.connection.query(obd.commands[key])
            value = str(response.value)
            value = re.sub(r'[^0-9.]', '', value)  # removes all non-digit and non-dot characters
            if key == "CATALYST_TEMP_B1S1":
                value = value[:3]  # 최대 3글자로 제한
            label.configure(text=value)
            if key == "SPEED":
                if value.isdigit():
                    self.center_meter.set(int(value))
                elif self.is_float(value):
                    self.center_meter.set(float(value))
                else:
                    print("Invalid value for conversion: ", value)
            if key == "RPM":
                if value.isdigit():
                    self.center_meter.set(int(value))
                elif self.is_float(value):
                    self.center_meter.set(int(float(value)))
                else:
                    print("Invalid value for conversion: ", value)
            if key == "ENGINE_LOAD":
                self.convert_to_int(value)

    def convert_to_int(self, value):
        try:
            if value.isdigit():
                return int(value)
            else:
                return int(float(value))
        except ValueError:
            print("Invalid value for conversion: ", value)
            return None

    def start_recording(self):
        self.is_recording = True
        self.recording_loop()

    def stop_recording(self):
        self.is_recording = False

    def recording_loop(self):
        if self.is_recording:
            self.obd_update()
            self.after(50, self.recording_loop)
