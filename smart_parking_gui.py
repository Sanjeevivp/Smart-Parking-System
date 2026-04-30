import tkinter as tk
import serial
import time
import threading
from itertools import cycle

# ========== SETTINGS ==========
SERIAL_PORT = 'COM7'   # Change this to your Arduino port
BAUD_RATE = 9600
SLOT_COUNT = 5
# ==============================

root = tk.Tk()
root.title("🚗 Smart Parking System")
root.geometry("620x600")
root.config(bg="#0f172a")

# ---------------------- HEADER ANIMATION ----------------------
title_colors = cycle(["#60a5fa", "#a78bfa", "#f472b6", "#34d399"])
title = tk.Label(root, text="SMART PARKING SYSTEM", font=("Poppins", 26, "bold"),
                 bg="#0f172a", fg="#60a5fa")
title.pack(pady=20)

def animate_title():
    title.config(fg=next(title_colors))
    root.after(400, animate_title)

animate_title()

# ---------------------- GATE DISPLAY ----------------------
gate_frame = tk.Frame(root, bg="#0f172a")
gate_frame.pack(pady=10)

gate_label = tk.Label(gate_frame, text="Gate: CLOSED", font=("Poppins", 20, "bold"),
                      bg="#1e293b", fg="orange", width=18, height=2, relief="ridge", bd=3)
gate_label.pack()

# Animated Gate Bar
canvas = tk.Canvas(root, width=350, height=40, bg="#0f172a", highlightthickness=0)
canvas.pack(pady=10)
gate_bar = canvas.create_rectangle(10, 10, 340, 30, fill="orange", outline="")

def animate_gate(open_gate=True):
    """Animate gate bar open/close"""
    if open_gate:
        for x in range(0, 340, 10):
            canvas.coords(gate_bar, 10 + x, 10, 340, 30)
            canvas.update()
            time.sleep(0.01)
        gate_label.config(text="Gate: OPEN", fg="#34d399")
    else:
        for x in range(340, 0, -10):
            canvas.coords(gate_bar, 10 + x, 10, 340, 30)
            canvas.update()
            time.sleep(0.01)
        gate_label.config(text="Gate: CLOSED", fg="orange")

# ---------------------- SLOT DISPLAY ----------------------
slot_labels = []
slot_colors = ["#dc2626", "#16a34a"]  # red, green

slots_frame = tk.Frame(root, bg="#0f172a")
slots_frame.pack(pady=15)

for i in range(SLOT_COUNT):
    lbl = tk.Label(slots_frame, text=f"Slot {i+1}: ---", font=("Poppins", 18, "bold"),
                   width=25, height=2, bg="#1e293b", fg="white", relief="ridge", bd=3)
    lbl.grid(row=i, column=0, pady=6)
    slot_labels.append(lbl)

# ---------------------- COUNTER DISPLAY ----------------------
count_frame = tk.Frame(root, bg="#0f172a")
count_frame.pack(pady=20)

free_text = tk.Label(count_frame, text="🟢 Free:", font=("Poppins", 18, "bold"),
                     bg="#0f172a", fg="#34d399")
free_text.grid(row=0, column=0, padx=10)

free_value = tk.Label(count_frame, text="0", font=("DS-Digital", 36, "bold"),
                      bg="#0f172a", fg="#34d399")
free_value.grid(row=0, column=1, padx=20)

occ_text = tk.Label(count_frame, text="🔴 Occupied:", font=("Poppins", 18, "bold"),
                    bg="#0f172a", fg="#f87171")
occ_text.grid(row=0, column=2, padx=10)

occ_value = tk.Label(count_frame, text="0", font=("DS-Digital", 36, "bold"),
                     bg="#0f172a", fg="#f87171")
occ_value.grid(row=0, column=3, padx=20)

status_label = tk.Label(root, text="Connecting to Arduino...",
                        font=("Poppins", 12), bg="#0f172a", fg="yellow")
status_label.pack(pady=10)

# ---------------------- FUNCTIONS ----------------------
def update_slots(line):
    line = line.strip()

    if "Gate Open" in line:
        threading.Thread(target=animate_gate, args=(True,), daemon=True).start()
        return
    elif line.startswith("Slots:"):
        threading.Thread(target=animate_gate, args=(False,), daemon=True).start()
    else:
        return

    try:
        parts = line.replace("Slots:", "").strip().split()
        if len(parts) != SLOT_COUNT:
            return

        free_count = 0
        occ_count = 0

        for i, val in enumerate(parts):
            state = int(val)
            if state == 1:
                slot_labels[i].config(text=f"Slot {i+1}: Available",
                                      bg="#16a34a", fg="white")
                free_count += 1
            else:
                slot_labels[i].config(text=f"Slot {i+1}: Occupied",
                                      bg="#dc2626", fg="white")
                occ_count += 1

        free_value.config(text=str(free_count))
        occ_value.config(text=str(occ_count))

        # Flash effect when full
        if free_count == 0:
            flash_full_alert()
    except Exception as e:
        print("Parse error:", e)


def flash_full_alert():
    def blink():
        for _ in range(4):
            title.config(fg="red")
            root.update()
            time.sleep(0.3)
            title.config(fg="white")
            root.update()
            time.sleep(0.3)
    threading.Thread(target=blink, daemon=True).start()

# ---------------------- SERIAL THREAD ----------------------
def serial_reader():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        status_label.config(text=f"Connected to {SERIAL_PORT}", fg="#34d399")

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print("Serial:", line)
                    root.after(0, update_slots, line)
            time.sleep(0.1)

    except serial.SerialException as e:
        status_label.config(text=f"Serial Error: {e}", fg="red")

# ---------------------- START ----------------------
threading.Thread(target=serial_reader, daemon=True).start()
root.mainloop()
