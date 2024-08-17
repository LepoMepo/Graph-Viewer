import os
import pandas as pd
from pathlib import Path
from fnmatch import fnmatch
import json


class GraphData:
    def __init__(self, path):
        self.path = Path(path)
        dir_readable = os.access(self.path, os.R_OK)
        if not dir_readable:
            msg = f'Permission denied accessing the directory {self.path}'
            raise PermissionError(msg)

    def get_graph_data(self, filename):
        filename = os.path.join(self.path, filename)
        file_exist = os.access(self.path, os.R_OK)
        if not file_exist:
            msg = f'Permission denied accessing the file {filename}'
            raise PermissionError(msg)
        data = pd.read_csv(filename, sep='\s+', skiprows=1, encoding='utf-8')
        return data

    def get_task_list(self):
        tasks = dict()
        list_of_files = os.listdir(self.path)
        pattern = '*.dia'
        for entry in list_of_files:
            if fnmatch(entry, pattern):
                index_start = entry.index('#')
                index_end = entry.index('.dia')
                task_to_add = entry[:index_start]
                if task_to_add not in tasks:
                    tasks[task_to_add] = [entry[index_start + 1:index_end]]
                else:
                    tasks[task_to_add].append(entry[index_start + 1:index_end])
        return tasks


class SettingModel:
    """
    A model for saving settings
    """
    fields = {
        'autofill date': {'type': 'bool', 'value': True},
        'autofill sheet data': {'type': 'bool', 'value': True}
    }

    def __init__(self):
        filename = 'abq_settings.json'
        self.filepath = Path("E:/RX Change/ABQ_Data_Entry") / filename
        print(self.filepath)
        self.load()

    def load(self):
        if not self.filepath.exists():
            return
        with open(self.filepath, 'r') as fh:
            raw_values = json.load(fh)
        for key in self.fields:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.fields[key]['value'] = raw_value

    def save(self):
        with open(self.filepath, 'w') as fh:
            json.dump(self.fields, fh)

    def set(self, key, value):
        if (
            key in self.fields and type(value).__name__ == self.fields[key]['type']
        ):
            self.fields[key]['value'] = value
        else:
            raise ValueError('Bad key or wrong variable type')

