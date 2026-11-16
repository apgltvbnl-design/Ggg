import os
import requests
import time
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

BOT_TOKEN = "9088325911:AAFAY2MJERZKOWedZE2gDrl2BEf6RsPQ0Ng"
CHAT_ID = "8057513929"

class BotApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.status_label = Label(text="Бот остановлен", font_size=20)
        layout.add_widget(self.status_label)
        start_btn = Button(text="Запустить бота", size_hint=(1, 0.3), background_color=(0, 1, 0, 1))
        start_btn.bind(on_press=self.start_bot_thread)
        layout.add_widget(start_btn)
        return layout

    def start_bot_thread(self, instance):
        self.status_label.text = "Бот запущен! Смотри Telegram."
        threading.Thread(target=self.bot_loop, daemon=True).start()

    def send_message(self, text):
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text})
        except: pass

    def bot_loop(self):
        last_update_id = None
        self.send_message("📱 APK Бот запущен!")
        while True:
            try:
                updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"timeout": 100, "offset": last_update_id}).json()
                if "result" in updates:
                    for update in updates["result"]:
                        last_update_id = update["update_id"] + 1
                        if "message" in update and "text" in update["message"]:
                            command = update["message"]["text"].replace("/", "").strip()
                            
                            if command == "ping":
                                self.send_message("Pong! Бот работает.")
                            elif command == "files":
                                try:
                                    files = os.listdir("/sdcard")
                                    self.send_message("Файлы:\n" + "\n".join(files[:10]))
                                except Exception as e:
                                    self.send_message(f"Ошибка: {e}")
                            elif command.startswith("cd "):
                                self.send_message("Команда cd в разработке (нужны права).")
                            elif command != "start":
                                self.send_message("Команды: ping, files")
            except Exception as e:
                print(f"Ошибка: {e}")
            time.sleep(1)

if __name__ == "__main__":
    BotApp().run()
