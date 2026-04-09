import csv
import time
import os

class Recorder:
    def __init__(self):
        self.data = []

    def add(self, t, pressure, altitude):
        self.data.append([t, pressure, altitude])

    def save_csv(self, meta):
        filename = f"{meta['aircraft']}_{meta['flight']}_{int(time.time())}.csv"
        
        # 打印保存路径，方便调试
        full_path = os.path.abspath(filename)
        print(f"Saving CSV to: {full_path}")

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["Aircraft", meta["aircraft"]])
            writer.writerow(["Flight", meta["flight"]])
            writer.writerow(["Date", meta["date"]])
            writer.writerow(["StartTime", meta["time"]])
            writer.writerow([])

            writer.writerow(["Time", "Pressure", "Altitude_ft"])
            writer.writerows(self.data)

        print(f"CSV saved successfully: {filename}")
        return filename
