import obd
import customtkinter as ctk
import tkinter as tk
import pandas as pd

obd.logger.setLevel(obd.logging.DEBUG)
ports = obd.scan_serial()
print(ports)
connection = obd.OBD(portstr=ports[0], baudrate=38400, fast=False, timeout=10)

# 엑셀 파일을 저장하기 위한 DataFrame 생성
df = pd.DataFrame()

root = tk.Tk()
root.title("OBD-II Data")

labels = {}
label_texts = {
    "RPM": "RPM: ",
    "SPEED": "SPEED: ",
    "CATALYST_TEMP_B1S1": "CATALYST_TEMP_B1S1: ",
    "OIL_TEMP": "OIL_TEMP: ",
    "INTAKE_TEMP": "INTAKE_TEMP: ",
    "ENGINE_LOAD": "ENGINE_LOAD: ",
    "THROTTLE_POS": "THROTTLE_POS: ",
    "AIR_STATUS": "AIR_STATUS:",
    "RUN_TIME": "RUN_TIME:",
    "AMBIANT_AIR_TEMP": "AMBIANT_AIR_TEMP:",
    "COOLANT_TEMP": "COOLANT_TEMP:",
    "INTAKE_PRESSURE": "INTAKE_PRESSURE:",
}

for key, text in label_texts.items():
    label = ctk.CTkLabel(root, text=text)
    label.pack()
    labels[key] = label

is_recording = False


def start_recording():
    global is_recording
    if not is_recording:
        is_recording = True
        update_labels()


def stop_recording():
    global is_recording
    is_recording = False


def update_labels():
    if is_recording:
        data = {}
        for key, label in labels.items():
            response = connection.query(obd.commands[key])
            value = str(response.value)
            label.configure(text=label_texts[key] + value)
            data[key] = value

        # DataFrame에 현재 데이터 추가
        df_row = pd.DataFrame(data, index=[0])
        df.append(df_row, ignore_index=True)

    # 1초마다 라벨을 업데이트
    root.after(100, update_labels)


def save_data():
    # DataFrame을 엑셀 파일로 저장
    # df.to_excel("obd_data.xlsx", index=False)
    df.to_json("obd_data.json", orient="records")


# 시작 버튼
start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack()

# 종료 버튼
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack()

# 10초 후에 데이터 저장 함수 호출
root.after(10000, save_data)

root.mainloop()
