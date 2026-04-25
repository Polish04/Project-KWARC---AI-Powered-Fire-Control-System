import customtkinter as ctk
from PIL import Image
import cv2
import os
from ultralytics import YOLO

#Database import
try:
    from Database import TARGET_DB
except Exception:
    print("CRITICAL: Database.py not found!")
    TARGET_DB = {}


class KwartzGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("KWARTZ")
        self.geometry("1450x900")
        ctk.set_appearance_mode("dark")

        self.cap = None
        self.is_running = False
        self.frame_count = 0
        self.last_results = None
        self.last_name = "SEARCHING"

        base = os.path.dirname(os.path.abspath(__file__))
        self.detector = YOLO(os.path.join(base, "KWARTZ_Spotter.pt"))
        self.classifier = YOLO(os.path.join(base, "classify_best.pt"))

        self.eastern_bloc_list = [
            "t-72", "t-80", "t-90", "t-14 armata",
            "type 99", "t-72_t-80"
        ]

        #UI
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="KWARTZ", font=("Courier", 32, "bold"), text_color="#00FF00").pack(pady=15)

        self.btn_run = ctk.CTkButton(self.sidebar, text="UPLOAD", fg_color="#1a521a", hover_color="#2d8c2d",
                                     command=self.process_input)
        self.btn_run.pack(pady=5, padx=20)
        self.btn_stop = ctk.CTkButton(self.sidebar, text="CEASE FIRE", fg_color="#721c24", hover_color="#a82835",
                                      command=self.stop_feed)
        self.btn_stop.pack(pady=5, padx=20)

        self.fcs_separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#333333")
        self.fcs_separator.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="FIRE CONTROL", font=("Courier", 16, "bold"), text_color="#00FF00").pack(pady=5)

        self.round_selection = ctk.CTkOptionMenu(self.sidebar, values=["APFSDS (SABOT)", "ALL-PURPOSE (MPAT)"],
                                                 fg_color="#111111", button_color="#1a521a", text_color="#00FF00")
        self.round_selection.pack(pady=5, padx=20)

        self.entry_range = ctk.CTkEntry(self.sidebar, placeholder_text="RANGE (M)", fg_color="#111111",
                                        text_color="#00FF00", border_color="#1a521a", justify="center")
        self.entry_range.pack(pady=5, padx=20)

        self.entry_wind = ctk.CTkEntry(self.sidebar, placeholder_text="WIND (+/- KM/H)", fg_color="#111111",
                                       text_color="#00FF00", border_color="#1a521a", justify="center")
        self.entry_wind.pack(pady=5, padx=20)

        self.entry_speed = ctk.CTkEntry(self.sidebar, placeholder_text="TGT SPEED (KM/H)", fg_color="#111111",
                                        text_color="#00FF00", border_color="#1a521a", justify="center")
        self.entry_speed.pack(pady=5, padx=20)

        self.entry_tilt = ctk.CTkEntry(self.sidebar, placeholder_text="HULL TILT (DEG)", fg_color="#111111",
                                       text_color="#00FF00", border_color="#1a521a", justify="center")
        self.entry_tilt.pack(pady=5, padx=20)

        self.entry_temp = ctk.CTkEntry(self.sidebar, placeholder_text="AIR TEMP (C)", fg_color="#111111",
                                       text_color="#00FF00", border_color="#1a521a", justify="center")
        self.entry_temp.pack(pady=5, padx=20)

        self.entry_pressure = ctk.CTkEntry(self.sidebar, placeholder_text="PRESSURE (hPa)", fg_color="#111111",
                                           text_color="#00FF00", border_color="#1a521a", justify="center")
        self.entry_pressure.pack(pady=5, padx=20)

        self.btn_fcs = ctk.CTkButton(self.sidebar, text="CALC SOLUTION", fg_color="#b8860b", hover_color="#daa520",
                                     text_color="black", font=("Courier", 14, "bold"), command=self.calculate_solution)
        self.btn_fcs.pack(pady=10, padx=20)

        self.fcs_output = ctk.CTkLabel(self.sidebar, text="ELEV: -- MIL\nWIND: -- MIL\nLEAD: -- MIL",
                                       font=("Courier", 16, "bold"), text_color="#00FF00", justify="left")
        self.fcs_output.pack(pady=5)

        self.display_frame = ctk.CTkFrame(self, fg_color="black")
        self.display_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.video_label = ctk.CTkLabel(self.display_frame, text="READY FOR DATA", font=("Courier", 20))
        self.video_label.pack(expand=True, fill="both")

        self.intel_frame = ctk.CTkFrame(self, width=400)
        self.intel_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.data_box = ctk.CTkTextbox(self.intel_frame, width=380, height=780, font=("Courier", 16),
                                       text_color="#00FF00", state="disabled")
        self.data_box.pack(padx=10, pady=10)
    #Balistic Computer
    def calculate_solution(self):
        try:
            target_range = float(self.entry_range.get() or 0)
            wind_speed = float(self.entry_wind.get() or 0)
            tgt_speed = float(self.entry_speed.get() or 0)
            hull_tilt = float(self.entry_tilt.get() or 0)
            air_temp = float(self.entry_temp.get() or 15)
            air_pressure = float(self.entry_pressure.get() or 1013)
            selected_round = self.round_selection.get()

            elevation_mil = (target_range / 1000.0) ** 1.1 * 2.5
            if "ALL-PURPOSE" in selected_round: elevation_mil *= 1.8
            elevation_mil *= (1.0 - (air_temp - 15) * 0.002)
            elevation_mil *= (1.0 + (air_pressure - 1013) * 0.0005)

            raw_windage = (abs(wind_speed) / 10.0) * (target_range / 1000.0) * 1.2
            if hull_tilt != 0:
                raw_windage += (elevation_mil * abs(hull_tilt) * 0.017)
                elevation_mil *= (1.0 - abs(hull_tilt) * 0.005)

            wind_dir = "LEFT" if wind_speed > 0 else "RIGHT" if wind_speed < 0 else "ZERO"
            time_of_flight = target_range / (1100.0 if "ALL-PURPOSE" in selected_round else 1600.0)
            lead_mil = (tgt_speed / 3.6) * time_of_flight

            self.fcs_output.configure(
                text=f"ELEV: +{elevation_mil:.1f} MIL\nWIND:  {raw_windage:.1f} {wind_dir}\nLEAD:  {lead_mil:.1f} MIL")
        except ValueError:
            self.fcs_output.configure(text="ERR: INVALID\nINPUT DATA")

    def stop_feed(self):
        self.is_running = False
        if self.cap: self.cap.release()
        blank_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        self.video_label.configure(image=ctk.CTkImage(blank_img, size=(1, 1)), text="FEED TERMINATED")

    def process_input(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename()
        if not path: return
        self.is_running = False
        if self.cap: self.cap.release()
        try:
            blank_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            self.video_label.configure(image=ctk.CTkImage(blank_img, size=(1, 1)), text="INITIALIZING SYSTEM...")
            self.update_idletasks()
        except:
            pass
        if path.lower().endswith(('.mp4', '.avi', '.mov')):
            self.cap = cv2.VideoCapture(path)
            self.is_running = True
            self.stream_video()
        else:
            frame = cv2.imread(path)
            if frame is not None: self.render(self.analyze(frame, force_ai=True))

    def stream_video(self):
        if self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                frame = self.analyze(frame, force_ai=(self.frame_count % 4 == 0))
                self.render(frame)
                self.after(1, self.stream_video)
            else:
                self.stop_feed()

    def analyze(self, frame, force_ai=False):
        if force_ai: self.last_results = self.detector.predict(frame, conf=0.35, verbose=False)
        if self.last_results:
            for r in self.last_results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    if force_ai:
                        crop = frame[y1:y2, x1:x2]
                        if crop.size > 0:
                            c_res = self.classifier.predict(crop, verbose=False)
                            if c_res[0].probs is not None:
                                p_index = c_res[0].probs.top1
                                p_conf = float(c_res[0].probs.top1conf)
                            elif len(c_res[0].boxes) > 0:
                                p_index = int(c_res[0].boxes.cls[0])
                                p_conf = float(c_res[0].boxes.conf[0])
                            else:
                                continue

                            p_name = c_res[0].names[p_index]
                            self.update_intel_final(p_name, p_conf, p_name.lower() in self.eastern_bloc_list)
                            self.last_name = p_name.upper()

                    red_color, thick, bracket_len = (0, 0, 255), 4, 50
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    cv2.line(frame, (cx - 25, cy), (cx + 25, cy), red_color, 2)
                    cv2.line(frame, (cx, cy - 25), (cx, cy + 25), red_color, 2)
                    for pt in [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]:
                        vx = bracket_len if pt[0] == x1 else -bracket_len
                        vy = bracket_len if pt[1] == y1 else -bracket_len
                        cv2.line(frame, pt, (pt[0] + vx, pt[1]), red_color, thick)
                        cv2.line(frame, pt, (pt[0], pt[1] + vy), red_color, thick)
                    cv2.putText(frame, f"LOCKED: {self.last_name}", (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                red_color, 2)
        return frame

    def render(self, frame):
        h, w, _ = frame.shape
        scale = min(750 / w, 750 / h)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ctk_img = ctk.CTkImage(Image.fromarray(img), size=(int(w * scale), int(h * scale)))
        self.video_label.configure(image=ctk_img, text="")

    def update_intel_final(self, p_name, p_conf, is_eastern):
        self.data_box.configure(state="normal")
        self.data_box.delete("1.0", "end")
        intel = TARGET_DB.get(p_name, {})
        report = f"ID: {intel.get('display_name', p_name.upper())}\nTHREAT: {intel.get('threat_level', 'UNKNOWN')}\nCONF: {p_conf * 100:.1f}%\n"
        report += f"ORIGIN: {intel.get('origin', 'N/A')}\nAMMO: {intel.get('ammo', 'WEAPONS HOLD')}\n"
        if is_eastern: report += "CLASS: EASTERN BLOC DESIGN\n"
        report += "\n--- TECHNICAL SPECS ---\n" + f"CANNON: {intel.get('main_armament', 'N/A')}\nSPEED: {intel.get('top_speed', 'N/A')}\n"
        self.data_box.insert("1.0", report)
        self.data_box.configure(state="disabled")


if __name__ == "__main__":
    app = KwartzGUI()
    app.mainloop()