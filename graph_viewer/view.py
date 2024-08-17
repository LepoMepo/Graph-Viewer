import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from . import widgets as w
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd

matplotlib.use('TkAgg')


class ChooseGraphics(w.TopLevelWindow):
    """
    Top level window to choose graphs to display
    Consist of tree with list of transducers and button 'ok'
    """

    def __init__(self, parent, list_of_transducers, selectmode='extended'):
        super().__init__(parent, title='Choose Graphs to Display')
        self._result = list()
        self.geometry('400x400')

        self.tree = ttk.Treeview(self, show='tree', columns='#1', selectmode=selectmode)
        self.tree.column('#1', width=150)
        ysb_tree = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb_tree.set)
        ysb_tree.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        self.tree.pack(fill=tk.BOTH, expand=1)

        for i in range(1, len(list_of_transducers)):
            self.tree.insert('', 'end', text=list_of_transducers[i])

        ttk.Button(self, text='Ok', command=self._on_ok).pack(side=tk.BOTTOM, fill=tk.X, expand=0)

        w.TopLevelWindow.center(self)
        self.protocol('WM_DELETE_WINDOW', self._on_close)
        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def _on_ok(self):
        for iid in self.tree.selection():
            self._result.append(self.tree.item(iid, option='text'))
        self.destroy()

    @property
    def result(self):
        return self._result

    def _on_close(self):
        self._result = ['closed']
        self.destroy()


class ToolBar(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vars_graph = {'Graph title': tk.StringVar(), 'X min': tk.DoubleVar(), 'X max': tk.DoubleVar(),
                            'Y min': tk.DoubleVar(), 'Y max': tk.DoubleVar(), 'Legend': tk.BooleanVar(),
                            'X axis': tk.StringVar(), 'Y axis': tk.StringVar()}
        self._vars_line = {'Choose line': tk.StringVar(), 'Line label': tk.StringVar(), 'Color': tk.StringVar(),
                           'Width': tk.DoubleVar(), 'Line type': tk.StringVar(), 'X scale': tk.StringVar(),
                           'Y scale': tk.StringVar()}
        self._default_colors = ['blue', 'orange', 'green', 'cyan', 'magenta', 'yellow', 'black', 'grey', 'white',
                                'indigo', 'navy', 'slateblue', 'brown', 'peru', 'gold', 'springgreen', 'teal',
                                'chocolate', 'wheat', 'steelblue', 'hotpink', 'orchid', 'lawngreen', 'olive']
        self._default_line_types = ['solid', 'dashed', 'dashdot', 'dotted', 'none']
        self._default_axis_scales = ['linear', 'log', 'symlog', 'logit']
        self._default_font_names = ['DejaVu Sans', 'Times New Roman', 'Helvetica', 'Times', 'Utopia',
                                    'ITC Avant Garde Gothic', 'Courier', 'Symbol', 'Computer Modern']
        self._line_types = list()
        self._colors = list()
        self._width = list()
        self._line_label = list()
        self._x_log = 'linear'
        self._y_log = 'linear'

        line_frame = ttk.LabelFrame(self, text='Line properties')
        line_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.line_label_combobox = w.LabelInput(line_frame, 'Choose line', self._vars_line['Choose line'],
                                                input_class=w.ValidatedCombobox,
                                                input_args={'values': self._line_types},
                                                pad_args={'padx': 2, 'pady': 2})
        self.line_label_combobox.grid(row=0, column=0)
        self.line_label_entry = w.LabelInput(line_frame, 'Line label', self._vars_line['Line label'],
                                             input_class=w.RequiredEntry, pad_args={'padx': 2, 'pady': 2},
                                             disable_var=self._vars_line['Choose line'])
        self.line_label_entry.grid(row=1, column=0)
        self.color_combobox = w.LabelInput(line_frame, 'Color', self._vars_line['Color'],
                                           input_class=w.ValidatedCombobox, input_args={'values': self._default_colors},
                                           disable_var=self._vars_line['Choose line'], pad_args={'padx': 2, 'pady': 2})
        self.color_combobox.grid(row=2, column=0)
        self.width_entry = w.LabelInput(line_frame, 'Width', self._vars_line['Width'], input_class=w.RequiredEntry,
                                        disable_var=self._vars_line['Choose line'], pad_args={'padx': 2, 'pady': 2})
        self.width_entry.grid(row=3, column=0)
        self.line_type_combobox = w.LabelInput(line_frame, 'Line type', self._vars_line['Line type'],
                                               input_class=w.ValidatedCombobox,
                                               input_args={'values': self._default_line_types},
                                               disable_var=self._vars_line['Choose line'],
                                               pad_args={'padx': 2, 'pady': 2})
        self.line_type_combobox.grid(row=4, column=0)
        self.x_scale_combobox = w.LabelInput(line_frame, 'X-axis scale', self._vars_line['X scale'],
                                             input_class=w.ValidatedCombobox,
                                             input_args={'values': self._default_axis_scales},
                                             disable_var=self._vars_line['Choose line'],
                                             pad_args={'padx': 2, 'pady': 2})
        self.x_scale_combobox.grid(row=5, column=0)
        self.y_scale_combobox = w.LabelInput(line_frame, 'Y-axis scale', self._vars_line['Y scale'],
                                             input_class=w.ValidatedCombobox,
                                             input_args={'values': self._default_axis_scales},
                                             disable_var=self._vars_line['Choose line'],
                                             pad_args={'padx': 2, 'pady': 2})
        self.y_scale_combobox.grid(row=6, column=0)

        line_buttons = tk.Frame(line_frame)
        line_buttons.grid(row=7, column=0)
        self.ok_line_button = ttk.Button(line_buttons, text='Ok', command=self.master._on_replot_line)
        self.ok_line_button.pack(side=tk.LEFT)
        self.reset_line_button = ttk.Button(line_buttons, text='Reset', command=self.master._on_reset_line)
        self.reset_line_button.pack(side=tk.RIGHT)
        self._vars_line['Choose line'].trace_add('write', self._on_select_line)

        graph_frame = ttk.LabelFrame(self, text='Graph Properties')
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        w.LabelInput(graph_frame, 'Graph title', self._vars_graph['Graph title'], input_class=ttk.Entry,
                     pad_args={'padx': 2, 'pady': 2}).grid(row=0, column=0)
        w.LabelInput(graph_frame, 'Name of x axis', self._vars_graph['X axis'], input_class=ttk.Entry,
                     pad_args={'padx': 2, 'pady': 2}).grid(row=1, column=0)
        w.LabelInput(graph_frame, 'Name of y axis', self._vars_graph['Y axis'], input_class=ttk.Entry,
                     pad_args={'padx': 2, 'pady': 2}).grid(row=2, column=0)
        w.LabelInput(graph_frame, 'Min x', self._vars_graph['X min'], input_class=w.RequiredEntry,
                     pad_args={'padx': 2, 'pady': 2}).grid(row=3, column=0)
        w.LabelInput(graph_frame, 'Max x', self._vars_graph['X max'], input_class=w.RequiredEntry,
                     pad_args={'padx': 2, 'pady': 2}).grid(row=4, column=0)
        w.LabelInput(graph_frame, 'Min y', self._vars_graph['Y min'], input_class=w.RequiredEntry,
                     pad_args={'padx': 2, 'pady': 2}).grid(row=5, column=0)
        w.LabelInput(graph_frame, 'Max y', self._vars_graph['Y max'], input_class=w.RequiredEntry,
                     pad_args={'padx': 2, 'pady': 2}).grid(row=6, column=0)
        self.legend_checkbutton = w.LabelInput(graph_frame, 'Legend', self._vars_graph['Legend'],
                                               input_class=ttk.Checkbutton, pad_args={'padx': 2, 'pady': 2})
        self.legend_checkbutton.grid(row=7, column=0)
        self._vars_graph['Legend'].trace_add('write', self.master._on_click_legend)

        graph_buttons = tk.Frame(graph_frame)
        graph_buttons.grid(row=8, column=0)
        self.ok_graph_button = ttk.Button(graph_buttons, text='Ok', command=self.master._on_replot_graph)
        self.ok_graph_button.pack(side=tk.LEFT)
        self.reset_graph_button = ttk.Button(graph_buttons, text='Reset', command=self.master._on_reset_graph)
        self.reset_graph_button.pack(side=tk.RIGHT)

    def set(self, line_label, width=1.5, line_type='solid'):
        """
        Setting line properties
        :return: None
        """
        self._line_types.append(line_type)
        self._line_label.append(line_label)
        self._colors.append(self._default_colors[self._line_label.index(line_label)])
        self._width.append(width)
        self.line_label_combobox.input.configure(values=self._line_label)

    def get(self):
        """
        Get line properties
        Not a good decision to make dict like this, but as for now it is the best option
        :return: data dict with properties of line type, line label, color, width
        TODO: remake filling of the dictionary
        """
        data = dict()
        data['Choose line'] = self._line_label
        data['Line label'] = self._line_label
        data['Color'] = self._colors
        data['Width'] = self._width
        data['Line type'] = self._line_types
        data['X scale'] = self._x_log
        data['Y scale'] = self._y_log
        return data

    def get_new_line_properties(self):
        """
        Asking all the label inputs about its values
        :return: data dict with all the values of line properties field
        """
        data = dict()
        for key, variable in self._vars_line.items():
            try:
                data[key] = variable.get()
            except tk.TclError:
                message = f'Error in field: {key}. Data was not saved'
                raise ValueError(message)
        return data

    def get_line_index(self):
        """
        Getting an index of the line which is chosen in combobox
        :return: index of the line
        """
        try:
            index = self._line_label.index(self._vars_line.get('Choose line').get())
        except ValueError:
            return None
        return index

    def set_new_line_properties(self):
        """
        Setting new line properties
        :return: None
        """
        line_properties = self.get_new_line_properties()
        index = self._line_label.index(line_properties['Choose line'])
        if line_properties['Line label']:
            self._line_label[index] = line_properties['Line label']
            self._vars_line.get('Choose line').set(line_properties.get('Line label'))
        self._colors[index] = line_properties['Color']
        self._line_types[index] = line_properties['Line type']
        self._width[index] = line_properties['Width']
        self._x_log = line_properties['X scale']
        self._y_log = line_properties['Y scale']
        self.line_label_combobox.input.configure(values=self._line_label)

    def reset_line_properties(self):
        for key, var in self._vars_line.items():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            else:
                if key != 'Choose line':
                    var.set('')

    def get_new_graph_properties(self):
        """
        Asking all the label inputs about its values
        :return: dict with all the values of graph properties field
        """
        data = dict()
        for key, variable in self._vars_graph.items():
            try:
                data[key] = variable.get()
            except tk.TclError:
                message = f'Error in field: {key}. Data was not saved'
                raise ValueError(message)
        return data

    def get_legend_value(self):
        return self._vars_graph.get('Legend').get()

    def get_font_name(self):
        return self._vars_graph.get('Font').get()

    def reset_graph_properties(self):
        for var in self._vars_graph.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            else:
                var.set('')

    def renew_widgets(self):
        index = self.get_line_index()
        if index is not None:
            data = self.get()
            keys = list(data.keys())
            for var, i in zip(self._vars_line.values(), range(len(keys))):
                if isinstance(var, tk.BooleanVar):
                    var.set(False)
                else:
                    if keys[i] == 'X scale' or keys[i] == 'Y scale':
                        var.set(data.get(keys[i]))
                    else:
                        var.set(data.get(keys[i])[index])

    def get_errors_line(self):
        errors = {}
        for key, var in self._vars_line.items():
            inp = var.label_widget.input
            error = var.label_widget.error
            if hasattr(inp, 'trigger_focusout_validation'):
                inp.trigger_focusout_validation()
            if error.get():
                errors[key] = error.get()
        return errors

    def get_errors_graph(self):
        errors = {}
        for key, var in self._vars_graph.items():
            inp = var.label_widget.input
            error = var.label_widget.error
            if hasattr(inp, 'trigger_focusout_validation'):
                inp.trigger_focusout_validation()
            if error.get():
                errors[key] = error.get()
        return errors

    def _on_select_line(self, *_):
        for key, var in self._vars_line.items():
            var.label_widget.input.config(state=tk.NORMAL)
        self.renew_widgets()


class GraphicWindow(w.TopLevelWindow):
    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, title, *args, **kwargs)
        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.canvas_tkagg = FigureCanvasTkAgg(self.figure, master=self)
        canvas = self.canvas_tkagg.get_tk_widget()
        canvas.pack(fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas_tkagg, self)
        self.toolbar_own = ToolBar(self)
        self.toolbar_own.pack(fill=tk.BOTH, expand=1)
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.grid(True)
        self._data = list()
        self._plots = list()
        self._headings = list()
        ttk.Label(self, text='Status: ')
        w.TopLevelWindow.center(self)

    def set(self, data, label):
        self._data.append(data)
        heading = tuple(data.columns)
        self._headings.append(heading)
        self.toolbar_own.set(label)

    def draw_plot(self):
        line_properties = self.toolbar_own.get()
        self.axes.set_xscale(line_properties.get('X scale'))
        self.axes.set_yscale(line_properties.get('Y scale'))
        for i in range(len(self._data)):
            self._plots.append(self.axes.plot(self._data[i].get(self._headings[i][0]),
                                              self._data[i].get(self._headings[i][1]),
                                              color=line_properties.get('Color')[i],
                                              ls=line_properties.get('Line type')[i],
                                              label=line_properties.get('Choose line')[i],
                                              lw=line_properties.get('Width')[i]))

    def _on_click_legend(self, *_):
        legend = self.toolbar_own.get_legend_value()
        if legend:
            self.axes.legend()
        else:
            try:
                self.axes.get_legend().remove()
            except AttributeError:
                pass
        self.canvas_tkagg.draw()

    def _on_replot_line(self):
        errors = self.toolbar_own.get_errors_line()
        if not errors:
            self._delete_lines()
            self.toolbar_own.set_new_line_properties()
            self.draw_plot()
            try:
                self.axes.get_legend().remove()
                self.axes.legend()
            except AttributeError:
                pass
            self.toolbar_own.renew_widgets()
            self.canvas_tkagg.draw()
        else:
            message = 'Cannot replot line'
            detail = (
                'The following field have errors:'
                '\n * {}'.format(
                    '\n * '.join(errors.keys())
                )
            )
            messagebox.showerror(
                title='Error',
                message=message,
                detail=detail,
                parent=self
            )
            return False

    def _on_replot_graph(self):
        errors = self.toolbar_own.get_errors_graph()
        if not errors:
            graph_properties = self.toolbar_own.get_new_graph_properties()
            name_x = graph_properties['X axis']
            name_y = graph_properties['Y axis']
            name_x = r'$\mathregular{' + name_x + '}$'
            name_y = r'$\mathregular{' + name_y + '}$'

            self.axes.set(ylabel=name_y or '', xlabel=name_x or '')
            if graph_properties['X max'] > graph_properties['X min']:
                self.axes.set_xlim(left=graph_properties['X min'], right=graph_properties['X max'])
            else:
                self.axes.set_xlim(left=self.axes.get_xlim()[0], right=self.axes.get_xlim()[1])
            if graph_properties['Y max'] > graph_properties['Y min']:
                self.axes.set_ylim(bottom=graph_properties['Y min'], top=graph_properties['Y max'])
            else:
                self.axes.set_ylim(bottom=self.axes.get_ylim()[0], top=self.axes.get_ylim()[1])
            self.axes.set_title(graph_properties['Graph title'])
            self.canvas_tkagg.draw()
        else:
            message = 'Cannot replot graph'
            detail = (
                'The following field have errors:'
                '\n * {}'.format(
                    '\n * '.join(errors.keys())
                )
            )
            messagebox.showerror(
                title='Error',
                message=message,
                detail=detail,
                parent=self
            )
            return False

    def _delete_lines(self):
        for i in range(len(self._plots)):
            line = self._plots.pop(0).pop(0)
            line.remove()

    def _on_reset_line(self):
        self.toolbar_own.reset_line_properties()

    def _on_reset_graph(self):
        self.toolbar_own.reset_graph_properties()


class MainWindow(ttk.Frame):
    """
    Main window of the app
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = str()
        # Left frame is for list of tasks
        self.left_frame = ttk.LabelFrame(self, text='List of tasks', padding='5')
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=0)

        self.tree = ttk.Treeview(self.left_frame, show='tree', columns='#1')
        self.tree.column('#1', width=150)
        ysb_tree = ttk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb_tree.set)
        ysb_tree.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        xsb_tree = ttk.Scrollbar(self.left_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=xsb_tree.set)
        xsb_tree.pack(side=tk.BOTTOM, fill=tk.X, expand=0)
        self.tree.pack(fill=tk.BOTH, expand=1)

        self.tree.bind('<Double-1>', self._on_select)
        self.path = str()

        # Right frame is for table with data
        self.right_frame = ttk.LabelFrame(self, text='Tabel data', padding='5')
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.pack(fill=tk.BOTH, expand=1)

        self.table = ttk.Treeview(self.right_frame, show='headings')
        self.table.pack(fill=tk.BOTH, expand=1)
        ysb_table = ttk.Scrollbar(self.table, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=ysb_table.set)
        ysb_table.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        xsb_table = ttk.Scrollbar(self.table, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(xscrollcommand=xsb_table.set)
        xsb_table.pack(side=tk.BOTTOM, fill=tk.X, expand=0)
        self.calc_data = pd.DataFrame()
        self.make_button = ttk.Button(self.right_frame, text='Make graph', command=self._choose_graphics)
        self.make_button.pack(fill=tk.Y, side=tk.LEFT, expand=0)
        self._font = str()
        self.list_of_tasks_and_transducers = dict()

    def _choose_graphics(self):
        self.choose_graph = ChooseGraphics(self, self.calc_data.columns.tolist())
        list_of_graphs = self.choose_graph.result
        if not list_of_graphs or len(list_of_graphs) > 24:
            message = 'Invalid number of transducers'
            detail = (
                'You must choose at least 1 and no more than 24 transducers'
            )
            messagebox.showerror(
                title='Error',
                message=message,
                detail=detail,
                parent=self
            )
            return False
        elif list_of_graphs[0] == 'closed':
            return
        graph_draw = GraphicWindow(self, title=list_of_graphs[0])
        for graph in list_of_graphs:
            graph_data = pd.concat([self.calc_data.get('Time'), self.calc_data.get(graph)], axis=1)
            graph_draw.set(graph_data, label=graph)
        graph_draw.draw_plot()

    def change_directory(self):
        self.tree.delete(*self.tree.get_children())
        self.table.delete(*self.table.get_children())
        self.table.configure(columns=[])
        for key in self.list_of_tasks_and_transducers.keys():
            item = self.tree.insert('', 'end', text=key)
            for values in self.list_of_tasks_and_transducers[key]:
                self.tree.insert(item, 'end', text=values)

    def set_graph_font(self, font):
        self._font = font
        matplotlib.rcParams['font.family'] = self._font

    def _on_select(self, event):
        children_iid = self.tree.selection()[0]
        parent_iid = self.tree.parent(children_iid)

        if parent_iid:
            self.table.delete(*self.table.get_children())
            parent_name = self.tree.item(parent_iid, option='text')
            children_name = self.tree.item(children_iid, option='text')
            self.filename = parent_name + '#' + children_name + '.dia'
            self.event_generate('<<MainWindowSelectTransducer>>')
            columns_calc_data = self.calc_data.columns.tolist()
            columns = ['#1']
            for i in range(len(columns_calc_data)):
                columns.append(str('#' + str(i + 2)))
            self.table.configure(columns=columns)
            self.table.heading(columns[0], text='No.')
            self.table.column(columns[0], stretch=False, width=40, anchor='center')
            for i in range(len(columns_calc_data)):
                self.table.heading(columns[i + 1], text=columns_calc_data[i])
                self.table.column(columns[i + 1], stretch=False, width=90, anchor='center')
            for row in self.calc_data.itertuples():
                self.table.insert('', 'end', values=row)
