import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

from main import extract_text_from_pdf, extract_work_details

META_BLUE = '#4267B2'

class PayslipApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Payslip Processor')
        self.configure(bg='white')
        self.geometry('500x300')

        style = ttk.Style(self)
        style.theme_use('default')
        style.configure('TButton', background=META_BLUE, foreground='white', font=('Arial', 11, 'bold'))
        style.map('TButton', background=[('active', META_BLUE)], foreground=[('active', 'white')])

        self.folder_path = tk.StringVar()

        header = tk.Label(self, text='Payslip Processor', bg='white', fg=META_BLUE, font=('Arial', 16, 'bold'))
        header.pack(pady=10)

        choose_btn = ttk.Button(self, text='Choose Payslip Folder', command=self.choose_folder)
        choose_btn.pack(pady=5)

        process_btn = ttk.Button(self, text='Process Payslips', command=self.process)
        process_btn.pack(pady=5)

        self.status = tk.Label(self, text='', bg='white', fg=META_BLUE, font=('Arial', 10))
        self.status.pack(pady=5)

    def choose_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)
            self.status.configure(text=f'Selected: {path}')

    def process(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning('No folder selected', 'Please choose a payslip folder first.')
            return
        if not os.path.isdir(folder):
            messagebox.showerror('Invalid folder', 'The selected folder does not exist.')
            return

        data = []
        for filename in os.listdir(folder):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(folder, filename)
                text = extract_text_from_pdf(pdf_path)
                details = extract_work_details(text)
                details['Filename'] = filename
                data.append(details)

        if not data:
            messagebox.showinfo('No Data', 'No payslip information was extracted.')
            return

        df = pd.DataFrame(data)
        output_path = os.path.join(folder, 'output.csv')
        df.to_csv(output_path, index=False)
        messagebox.showinfo('Done', f'Data saved to {output_path}')


def main():
    app = PayslipApp()
    app.mainloop()


if __name__ == '__main__':
    main()
