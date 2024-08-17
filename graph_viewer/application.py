import tkinter as tk
from tkinter import ttk
from . import view as v
from . import models as m
from tkinter import messagebox, filedialog
from .mainmenu import MainMenu


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Graph Viewer')
        self.state('zoomed')
        self.menu = MainMenu(self)
        self.config(menu=self.menu)
        event_callbacks = {
            '<<DirectorySelect>>': self._on_file_select,
            '<<FileQuit>>': lambda _: self.quit(),
            '<<SelectGraphFont>>': self._on_select_graph_font
        }
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)
        self.main_window = v.MainWindow(self)
        self.main_window.pack(fill=tk.BOTH, expand=1)
        self.main_window.bind('<<MainWindowSelectTransducer>>', self._select_transducer)
        self.graph_data = None

        self.protocol('WM_DELETE_WINDOW', self._on_close)

    def _select_transducer(self, *_):
        self.main_window.calc_data = self.graph_data.get_graph_data(self.main_window.filename)

    def _on_file_select(self, *_):
        directory = filedialog.askdirectory(
            title='Select directory with the results'
        )
        if directory:
            self.graph_data = m.GraphData(directory)
            self.main_window.list_of_tasks_and_transducers = self.graph_data.get_task_list()
            self.main_window.change_directory()

    def _on_select_graph_font(self, *_):
        self.main_window.set_graph_font(self.menu.font_var.get())

    def _on_close(self):
        if messagebox.askokcancel('Exit', 'Are you sure you want to exit?'):
            self.quit()
