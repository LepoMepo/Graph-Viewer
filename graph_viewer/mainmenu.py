import tkinter as tk
from tkinter import messagebox


class MainMenu(tk.Menu):

    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        return callback

    fonts = ['DejaVu Sans',
             'Times New Roman',
             'Courier New',
             'Arial',
             'Calibri']

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.font_var = tk.StringVar()
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About...', command=self.show_about)
        settings_menu = tk.Menu(self, tearoff=False)
        font_menu = tk.Menu(settings_menu, tearoff=False)
        settings_menu.add_cascade(label='Graph font', menu=font_menu)
        for font in self.fonts:
            if font == 'DejaVu Sans':
                font_menu.add_radiobutton(label=font, value=font, variable=self.font_var)
            else:
                font_menu.add_radiobutton(label=font, value=font, variable=self.font_var)
        self.font_var.trace_add('write', self._event('<<SelectGraphFont>>'))
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label='Select directory...',
            command=self._event('<<DirectorySelect>>')
        )
        file_menu.add_separator()
        file_menu.add_command(
            label='Quit',
            command=self._event('<<FileQuit>>')
        )
        self.add_cascade(label='File', menu=file_menu)
        self.add_cascade(label='Settings', menu=settings_menu)
        self.add_cascade(label='Help', menu=help_menu)

    def show_about(self):
        about_message = 'Graph Viewer'
        about_detail = (
            'by Pavel Vanyushin\n'
            'For assistance please contact the author.'
        )
        messagebox.showinfo(title='About', message=about_message, detail=about_detail)
