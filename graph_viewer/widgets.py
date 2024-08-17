import tkinter as tk
from tkinter import ttk


class ValidateMixin:
    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)
        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)
        self.configure(validate='all', validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
                       invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d'))

    def _toggle_error(self, on=False):
        self.configure(foreground=('red' if on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        self.error.set('')
        self._toggle_error()
        valid = True
        state = str(self.configure('state')[-1])
        if state == tk.DISABLED:
            return valid
        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(proposed=proposed, current=current, char=char, event=event, index=index,
                                       action=action)
        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event == 'key':
            self._key_invalid(proposed=proposed, current=current, char=char, event=event, index=index, action=action)

    def _focusout_invalid(self, **kwargs):
        """
        Handle invalid data on a focus event
        """
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        """
        Handle invalid data on a key event. By default, we want to do nothing
        """
        pass

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid


class RequiredEntry(ValidateMixin, ttk.Entry):
    """
    An entry that requires a value
    """

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


class ValidatedCombobox(ValidateMixin, ttk.Combobox):
    """
    A combobox that only take values from its string list
    """

    def _key_validate(self, proposed, action, **kwargs):
        valid = True
        if action == '0':
            self.set('')
            return True
        values = self.cget('values')
        matching = [x for x in values if x.lower().startswith(proposed.lower())]
        if len(matching) == 0:
            valid = False
        elif len(matching) == 1:
            self.set(matching[0])
            self.icursor(tk.END)
            valid = False
        return valid

    def _focusout_validate(self, **kwargs):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


class TopLevelWindow(tk.Toplevel):
    """
    This class just sets the title and has static method center, which centers the window
    It was made to prevent repeating of center method in TopLevel widgets.
    There was a try to make focus, but it can not be done.
    """

    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title(title)
        self.after(10, self.lift)
        self.focus_set()

    @staticmethod
    def center(window):
        window.update_idletasks()
        width = window.winfo_width()
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2 * frm_width
        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = window.winfo_screenwidth() // 2 - win_width // 2
        y = window.winfo_screenheight() // 2 - win_height // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.deiconify()


class LabelInput(tk.Frame):
    """
    A widget containing a label and input together
    """

    def __init__(self, parent, label, var, input_class=ttk.Entry, input_args=None, label_args=None, pad_args=None,
                 disable_var=None, **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        pad_args = pad_args or {}
        self.variable = var
        self.variable.label_widget = self
        if disable_var:
            self.disable_var = disable_var
            self.disable_var.trace_add('write', self._check_disable)
        if input_class in (ttk.Checkbutton, ttk.Button):
            input_args['text'] = label
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.E + tk.W), **pad_args)
        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args['variable'] = self.variable
        else:
            input_args['textvariable'] = self.variable
        if input_class == ttk.Radiobutton:
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                button = ttk.Radiobutton(self.input, value=v, text=v, **input_args)
                button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x', **pad_args)
        else:
            self.input = input_class(self, **input_args)
            self.input.grid(row=0, column=1, sticky=(tk.W + tk.E), **pad_args)
            self.columnconfigure(0, weight=1)

        self.error = getattr(self.input, 'error', tk.StringVar())

    def _check_disable(self, *_):
        if not hasattr(self, 'disable_var'):
            return
        if not self.disable_var.get():
            self.input.configure(state=tk.DISABLED)
            self.variable.set('')
            self.error.set('')
        else:
            self.input.configure(state=tk.NORMAL)

    def grid(self, sticky='we', **kwargs):
        """
        Override grid to add default sticky values
        """

        super().grid(sticky=sticky, **kwargs)
