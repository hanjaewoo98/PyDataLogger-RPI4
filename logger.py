import obd
import customtkinter as ctk
import tkinter as tk

obd.logger.setLevel(obd.logging.DEBUG)
ports = obd.scan_serial()
print(ports)
connection = obd.OBD(portstr=ports[0], baudrate=38400, fast=False, timeout=10)

root = tk.Tk()
root.title("OBD-II Data")

labels = {}
label_texts = {
    "RPM": "RPM: ",
    "SPEED": "SPEED: ",
    "CATALYST_TEMP_B1S1": "CATALYST_TEMP_B1S1: ",
    "OIL_TEMP": "OIL_TEMP: ",
    "INTAKE_TEMP": "INTAKE_TEMP: ",
}

for key, text in label_texts.items():
    label = ctk.CTkLabel(root, text=text)
    label.pack()
    labels[key] = label


def update_labels():
    for key, label in labels.items():
        response = connection.query(obd.commands[key])
        label.configure(text=label_texts[key] + str(response.value))

    root.after(100, update_labels)


update_labels()

root.mainloop()
