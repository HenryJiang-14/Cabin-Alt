from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime, timedelta, timezone
try:
    from plyer import vibrator, notification
    PLYER_AVAILABLE = True
except:
    PLYER_AVAILABLE = False

from sensors import get_pressure
from recorder import Recorder
from uploader import zip_file, upload
from utils import pressure_to_altitude_ft

def get_beijing_time():
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)

class MainLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rec = Recorder()

    def show_input_popup(self):
        layout = BoxLayout(orientation='vertical')

        self.aircraft_input = TextInput(hint_text="Aircraft B-XXXX")
        self.flight_input = TextInput(hint_text="Flight MU1234")

        now = get_beijing_time()
        self.date_input = TextInput(text=now.strftime("%Y-%m-%d"))
        self.time_input = TextInput(text=now.strftime("%H:%M:%S"))

        btn = Button(text="Confirm")

        layout.add_widget(self.aircraft_input)
        layout.add_widget(self.flight_input)
        layout.add_widget(self.date_input)
        layout.add_widget(self.time_input)
        layout.add_widget(btn)

        self.popup = Popup(title="Flight Info", content=layout, size_hint=(0.8, 0.6))
        btn.bind(on_press=self.confirm_input)

        self.popup.open()

    def confirm_input(self, instance):
        # 验证必填字段
        aircraft = self.aircraft_input.text.strip()
        flight = self.flight_input.text.strip()
        date = self.date_input.text.strip()
        time_val = self.time_input.text.strip()

        if not aircraft or not flight or not date or not time_val:
            # 显示错误提示
            error_popup = Popup(
                title="Error",
                content=Button(text="All fields are required!\n\nTap to close"),
                size_hint=(0.8, 0.4)
            )
            error_popup.content.bind(on_press=error_popup.dismiss)
            error_popup.open()
            return

        self.aircraft = aircraft
        self.flight = flight
        self.date = date
        self.time0 = time_val

        self.popup.dismiss()
        self.start()

    def start(self):
        Clock.schedule_interval(self.loop, 1)
        # 隐藏 Start 按钮,启用 Stop 按钮
        self.ids.start_btn.visible = False
        self.ids.start_btn.disabled = True
        self.ids.stop_btn.disabled = False

    def stop(self):
        Clock.unschedule(self.loop)
        # 显示 Start 按钮,禁用 Stop 按钮
        self.ids.start_btn.visible = True
        self.ids.start_btn.disabled = False
        self.ids.stop_btn.disabled = True

        meta = {
            "aircraft": self.aircraft,
            "flight": self.flight,
            "date": self.date,
            "time": self.time0
        }

        try:
            csv_file = self.rec.save_csv(meta)
            zipname = zip_file(csv_file)
            upload_result = upload(zipname)
            
            # 显示保存成功提示
            if upload_result:
                msg = f"Data saved & uploaded!\nFile: {csv_file}"
            else:
                msg = f"Data saved locally!\nFile: {csv_file}\n(Upload failed)"
            
            success_popup = Popup(
                title="Success",
                content=Button(text=msg + "\n\nTap to close"),
                size_hint=(0.8, 0.5)
            )
            success_popup.content.bind(on_press=success_popup.dismiss)
            success_popup.open()
        except Exception as e:
            # 显示错误提示
            error_popup = Popup(
                title="Error",
                content=Button(text=f"Failed to save data:\n{str(e)}\n\nTap to close"),
                size_hint=(0.8, 0.5)
            )
            error_popup.content.bind(on_press=error_popup.dismiss)
            error_popup.open()

    def loop(self, dt):
        pressure = get_pressure()
        altitude = pressure_to_altitude_ft(pressure)

        t = get_beijing_time().strftime("%H:%M:%S")
        self.rec.add(t, pressure, altitude)

        self.ids.altitude.text = f"{altitude:.0f} ft"
        self.ids.pressure.text = f"{pressure:.1f} hPa"

        if altitude > 8000 and PLYER_AVAILABLE:
            try:
                vibrator.vibrate(0.5)
                notification.notify(
                    title="WARNING",
                    message="Cabin Altitude > 8000 ft"
                )
            except:
                pass

class CabinApp(App):
    def build(self):
        Builder.load_file('main.kv')
        return MainLayout()

CabinApp().run()