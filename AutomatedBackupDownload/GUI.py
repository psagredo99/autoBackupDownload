import tkinter as tk
from tkinter import filedialog
from main import loadConfig, login, headers, getFileLink, downloadFile
from settings import Result

class SalesforceBackupDownloaderGUI:

    def __init__(self, root):
        self.CONFIG = None
        self.RESULT = None
        self.root = root
        self.root.title("Salesforce Backup Downloader")
        self.root.geometry("500x400")  # Set initial window size

        self.info_text = tk.Text(root, wrap="word", height=10, width=60)
        self.info_text.pack(pady=10)

        self.run_export_button = tk.Button(root, text="Run Export", command=self.run_export)
        self.run_export_button.pack()

    def append_info(self, info):
        self.info_text.insert(tk.END, info + "\n")
        self.info_text.see(tk.END)

    def run_export(self):
        # Clear the text widget before starting a new process
        self.info_text.delete(1.0, tk.END)

        # Run the export process
        self.load_config()
        self.login()
        self.get_file_link()
        self.download_file()

    def load_config(self):
        CONFIG = loadConfig()
        self.CONFIG = CONFIG
        self.append_info("#-Carga de configuracion...")

    def login(self):
        RESP = login(self.CONFIG)
        self.RESULT = Result(RESP.text)
        self.append_info("#-LOGIN -- OK")

    def get_file_link(self):
        LINK = getFileLink(self.RESULT, self.CONFIG)
        self.LINK = LINK
        self.append_info("#-Obteniendo enlace del archivo...")

    def download_file(self):
        self.append_info("#-Iniciando descarga...")
        FILE = downloadFile(self.LINK, self.RESULT, self.CONFIG)
        self.append_info("#-DESCARGA COMPLETA")
        self.append_info("#-ARCHIVOS EXPORTADOS EN: " + FILE)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesforceBackupDownloaderGUI(root)
    root.mainloop()
