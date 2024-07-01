import subprocess
import os
import platform
import tkinter as tk
from tkinter import ttk

class WifiPasswordViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wi-Fi Password Viewer")
        self.geometry("600x400")
        
        self.tree = ttk.Treeview(self, columns=('SSID', 'Password'), show='headings')
        self.tree.heading('SSID', text='SSID')
        self.tree.heading('Password', text='Password')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.load_wifi_passwords()

    def load_wifi_passwords(self):
        if platform.system() == "Windows":
            self.get_windows_wifi_passwords()
        elif platform.system() == "Linux":
            self.get_linux_wifi_passwords()
        else:
            print("Unsupported OS")

    def get_windows_wifi_passwords(self):
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = [line.split(":")[1].strip() for line in result.stdout.split('\n') if "All User Profile" in line]
        
        for profile in profiles:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            password = ""
            for line in lines:
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
                    break
            self.tree.insert('', 'end', values=(profile, password))

    def get_linux_wifi_passwords(self):
        path = '/etc/NetworkManager/system-connections/'
        try:
            files = os.listdir(path)
            for file in files:
                if file.endswith(".nmconnection") or file.endswith(".conf"):
                    with open(os.path.join(path, file), 'r') as f:
                        ssid, psk = "", ""
                        for line in f:
                            if "ssid=" in line:
                                ssid = line.split('=')[1].strip()
                            if "psk=" in line:
                                psk = line.split('=')[1].strip()
                        if ssid:
                            self.tree.insert('', 'end', values=(ssid, psk))
        except Exception as e:
            print(f"Failed to access NetworkManager configurations: {e}")

if __name__ == "__main__":
    app = WifiPasswordViewer()
    app.mainloop()
